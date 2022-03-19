from time import sleep
from django.shortcuts import render
from wikidata.client import Client
import json as simplejson
import ssl
import urllib.request
import os
import threading
 
# to prevent [Winerror 10060]
ssl._create_default_https_context = ssl._create_unverified_context


def showResult(request):

    data = {"mention_data": [{"offset": "36", "mention": "strawberries", "kb_id": "Q745", 
    "wikidata_url": "https://www.wikidata.org/wiki/Q745", "description": "genus of plants"}], 
    "text": "BrittaRiley _ 2011X 1 BrittaRiley _ 2011X 289.38 303.82 < NA > tony in chicago has been taking " 
    "on growing experiments like lots of other window farmers and he's been able to get his strawberries to "
    "fruit for nine months of the year in low light conditions by simply changing out the organic nutrients"
    }

    json_str = simplejson.dumps(data, ensure_ascii=False)
    json_dict = simplejson.loads(json_str)

    info_list=json_dict["mention_data"]
    info_dict=info_list[0]
    kb_id=info_dict["kb_id"]

    # if the entity can be found in WikiData, fetch the main image
    if kb_id != "NULL":
        prepareImage(kb_id)

    return render(request,'result.html',{"json_dict":json_dict,"kb_id":kb_id})

   
def prepareImage(kb_id):
    filepath = 'static\images\\' + kb_id + '.jpg'
    #if the image already exists(the entity has been parsed before), there's no need to download again
    if os.path.isfile(filepath):
        return None
    else:
        downloadingThread = myThreadClass()
        downloadingThread.start(filepath,kb_id)

       
# a self-defined class to download the main image from Wikidata, using multithreads to improve the speed
class myThreadClass():
    # the attribute finish acts as a flag showing whether the download has finished
    def __init__(self):
        self.finish = False
     
    # task of threads
    def download(self,image_url,f):
        try:
            f.write(urllib.request.urlopen(image_url).read())
            f.close()  
            # if the file is closed, download finishes, then change the flag to True
            #print("finish")
            self.finish = True
            return None
        except Exception as e:
            print(e)
            return None

    def start(self,filepath,kb_id):
        # list for threads
        threadslist=[]
        # get the url of the main image
        client = Client()  
        entity = client.get(kb_id)
        image_prop = client.get('P18')
        image = entity[image_prop]
        image_url = image.image_url
        # create the image file
        f = open(filepath,'wb')
        # create multiple threads
        for i in range(0,5):
            newthread=threading.Thread(target=self.download,args=(image_url,f))
            threadslist.append(newthread)
            sleep(1)
        # start them
        for t in threadslist:
            t.start()
        # keep checking every 3 secs to see whether the procedure needs to be ended
        # mechanism: when the parent thread is killed, so are its child threads
        while True:
            sleep(3)
            if self.finish:
                break
