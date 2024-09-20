from datetime import datetime
from time import sleep
from django.shortcuts import render
from wikidata.client import Client
from enum import Enum
from django.template.defaulttags import register
import json as simplejson
import ssl
import urllib.request
import os
import threading

#防止10060错误
ssl._create_default_https_context = ssl._create_unverified_context

@register.filter
def get_range(value):
    return range(value)

def index_out(request):
    # 从session 中取出 str json
    data = request.session.pop('jdata',False)
    # print("session11111", data, type(data))

    # str json 转为 json 对象
    json_dict = simplejson.loads(data)
    # data = jdata['mention_data']
    # img_src = jdata['text']

    # json_str = simplejson.dumps(data, ensure_ascii=False)
    # json_dict = simplejson.loads(json_str)

    info_list = json_dict["mention_data"]
    for entity in info_list:
        if entity['description'] is not None:
            entity['description'] = ' '.join(entity['description'].split()[:50]) + ' ...'
    # print("info_list:", info_list)
    kb_id = []
    offset = []
    for entity in info_list:
        if entity["kb_id"] != '':
            entity["wikidata_url"] = "https://www.wikidata.org/wiki/" + str(entity["kb_id"])
        else:
            entity["wikidata_url"] = "NULL"
        kb_id.append(entity["kb_id"])
        offset.append(int(entity["asr_offset"]))
        
    offset.sort()
    # print("kb_id list: ",kb_id)
    # print("offset list: ",offset)

    # if the entity can be found in WikiData, fetch the main image
    img_src={}
    for id in kb_id:
        if id != '':
            file_type = loadImage(id)
            if file_type != FileType.NO:
                img_path = '..\static\images\\' + str(id) + file_type.value
                img_src[id] = img_path
            else:
                img_src[id] = 'NULL'
        else:
            img_src[id] = 'NULL'

    # print(img_src)
    data = simplejson.dumps(json_dict)

    return render(request,'output.html',{"data":data,"img_src":img_src})


class FileType(Enum):
    JPG = '.jpg'
    PNG = '.png'
    SVG = '.svg'
    NO  = None


def loadImage(kb_id):
    filepath_jpg = 'static\images\\' + kb_id + '.jpg'
    filepath_png = 'static\images\\' + kb_id + '.png'
    filepath_svg = 'static\images\\' + kb_id + '.svg'
    if os.path.isfile(filepath_jpg):
        return FileType.JPG
    elif os.path.isfile(filepath_png):
        return FileType.SVG
    elif os.path.isfile(filepath_svg):
        return FileType.SVG
    else:
        # get the url of the main image
        client = Client()  
        entity = client.get(kb_id)
        image_prop = client.get('P18')
        image = entity[image_prop]
        image_url = image.image_url
        downloadingThread = myThreadClass()
        # print(image_url)
        if(image_url.endswith('.jpg')):
            downloadingThread.start(filepath_jpg,image_url)
            return FileType.JPG
        elif(image_url.endswith('.png')):
            downloadingThread.start(filepath_png,image_url)
            return FileType.PNG
        elif(image_url.endswith('.svg')):
            downloadingThread.start(filepath_svg,image_url)
            return FileType.SVG
        else:
            return FileType.NO

#views.py
class myThreadClass():
    def __init__(self):
        self.finish = False

    def download(self,image_url,f):
        # print("start: "+ str(datetime.now()))
        try:
            f.write(urllib.request.urlopen(image_url).read())
            f.close()  
            print("finish: "+ str(datetime.now()))
            self.finish = True
            return None
        except Exception as e:
            print(e)
            return None

    def start(self,filepath,image_url):
        # list for threads
        threadslist=[]
        # create the file
        f = open(filepath,'wb')
        # create multiple threads
        for i in range(0,5):
            newthread=threading.Thread(target=self.download,args=(image_url,f))
            threadslist.append(newthread)
            sleep(1)
        #start them
        for t in threadslist:
            t.start()
        #keep checking every 1 sec to see whether the procedure needs to be ended
        while True:
            sleep(1)
            if self.finish:
                break

