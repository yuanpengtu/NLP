from django.shortcuts import render
from django.http import HttpResponse
from Sentiment_Analysis.api.lstm_test import *
import json


# Create your views here.
def index(request):
    return render(request, 'index.html')  # 上传index.html文件到templates目录下


def sentiment_analysis(request):
    if request.method == 'POST':  # 请求方法为POST时，进行处理
        input = request.POST.get('input')  # 获取输入的文本
        msg = lstm_predict(input)
        dict = {}
        dict['message'] = msg
        data = json.dumps(dict)
        return HttpResponse(data)
