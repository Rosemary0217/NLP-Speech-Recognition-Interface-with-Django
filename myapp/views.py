from fileinput import filename
import re
import site
import time
from turtle import goto, left
from urllib import response
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
#from django.http import JsonResponse
import requests
import json
import pyaudio
import wave
import numpy as np
import pylab as plt
#from requests.exceptions import HTTPError
from django.http import JsonResponse
from django.shortcuts import render
import time
 
 
num_progress = 0 
recordflag = False
time_monitor=3
# app主页
def index_in(request):
    print("index")
    global time_monitor
    time_monitor=3
    return render(request, "myapp/index.html")

# 加载文件上传表单
def upload(request):
    print("upload")
    return render(request, "myapp/upload.html",{"timeget":time_monitor})

# 执行文件上传处理
def doupload(request):
    global recordflag
    print("output")
    # 接收
    if not recordflag:
        myfile = request.FILES.get("doc", None)
        if not myfile:
            return HttpResponse("file not find")

        filename = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/docs/"+filename, "wb+")
    # 将文件流分块读取文件内容并写入目标文件
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close

    else:
        recordflag = False
        filename = "input.wav"

    host = "http://10.108.17.152:"
    endpoint = "5000"
    url = ''.join([host, endpoint])

    # r = requests.post(url, json=json.dumps(address))
    # response = r.json()
    # print(response)

    # print("________________________________________________________________________")
    # print(filename)
    with open("./static/docs/"+filename, 'rb') as f:
        resp = requests.post(url, files={'voice_file': f})
    response = resp.json()
    # print(response)
    # print("________________________________________________________________________")

    # 将json存入 session 中传递
    jdata = {"data":"data", "img_src":"img_src"}
    jdata = response
    # jdata = { "mention_data": [{"offset": "19","mention": "nasa","kb_id": "Q23548","wikidata_url": "https://www.wikidata.org/wiki/Q23548", "description": "independent agency of the United States Federal Government"},{"offset": "42", "mention": "new york city","kb_id": "Q60","wikidata_url": "https://www.wikidata.org/wiki/Q60", "description": "largest city in the United States"}], "text": "BrittaRiley _ 2011X 1 BrittaRiley _ 2011X 261.89 271.48 < NA > what we ' re doing is what nasa or a large corporation would call r & d < unk > or research and development but what we call it is r new york city"}
    
    request.session['jdata'] = json.dumps(jdata)


    return redirect('/output')


def monitor(request):
    global recordflag
    recordflag = True
    input_filename = "input.wav"               # 麦克风采集的语音输入
    input_filepath = "./static/docs/"              # 输入文件的path
    # filiname=str(time.time())+"."+input_filename
    in_path = input_filepath +input_filename
    CHUNK = 1024  # 每个缓冲区的帧数
    FORMAT = pyaudio.paInt16  # 采样位数
    CHANNELS = 1  # 单声道
    RATE = 44100  # 采样频率
    """ 录音功能 """
    p = pyaudio.PyAudio()  # 实例化对象
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # 打开流，传入响应参数
    wf = wave.open(in_path, 'wb')  # 打开 wav 文件。
    wf.setnchannels(CHANNELS)  # 声道设置
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
    wf.setframerate(RATE)  # 采样频率设置

    for _ in range(0, int(RATE * time_monitor / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)  # 写入数据
    stream.stop_stream()  # 关闭流
    stream.close()
    p.terminate()
    wf.close()
    return render(request,"myapp/monitor.html",{"timeget":time_monitor})

def monitors(request):
    global recordflag
    recordflag = True
    input_filename = "input.wav"               # 麦克风采集的语音输入
    input_filepath = "./static/docs/"              # 输入文件的path
    # filiname=str(time.time())+"."+input_filename
    in_path = input_filepath +input_filename
    CHUNK = 1024  # 每个缓冲区的帧数
    FORMAT = pyaudio.paInt16  # 采样位数
    CHANNELS = 1  # 单声道
    RATE = 44100  # 采样频率
    """ 录音功能 """
    p = pyaudio.PyAudio()  # 实例化对象
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # 打开流，传入响应参数
    wf = wave.open(in_path, 'wb')  # 打开 wav 文件。
    wf.setnchannels(CHANNELS)  # 声道设置
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
    wf.setframerate(RATE)  # 采样频率设置
    iver="录音结束"
    for _ in range(0, int(RATE * time_monitor / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)  # 写入数据
    stream.stop_stream()  # 关闭流
    stream.close()
    p.terminate()
    wf.close()
    print("monitors")
    return render(request,"myapp/monitor.html",{"timeget":time_monitor,"over":iver,"change":1})

def settime(request):
    global time_monitor
    ssq=request.POST.get('mytime')
    if(ssq==""):
        print(ssq+"123")
        ssq=3
    print(ssq+"123")
    time_monitor=int(ssq)       
    print(time_monitor) 
    # time_monitor=mytime
    return render(request,'myapp/upload.html',{"timeget":time_monitor})

def start_end(request):
    global recordflag
    
    recordflag=True
    input_filename = "input.wav"               # 麦克风采集的语音输入
    input_filepath = "./static/docs/"              # 输入文件的path
    # filiname=str(time.time())+"."+input_filename
    in_path = input_filepath +input_filename
    CHUNK = 1024  # 每个缓冲区的帧数
    FORMAT = pyaudio.paInt16  # 采样位数
    CHANNELS = 1  # 单声道
    RATE = 44100  # 采样频率
    """ 录音功能 """
    p = pyaudio.PyAudio()  # 实例化对象
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # 打开流，传入响应参数
    wf = wave.open(in_path, 'wb')  # 打开 wav 文件。
    wf.setnchannels(CHANNELS)  # 声道设置
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
    wf.setframerate(RATE)  # 采样频率设置

    for _ in range(0, int(RATE * 10 / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)
    stream.stop_stream()  # 关闭流
    stream.close()
    p.terminate()
    wf.close()
    return render(request,"myapp/monitor.html",{"start":"录音完成"})


        

        

