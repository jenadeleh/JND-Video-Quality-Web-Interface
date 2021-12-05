from typing import Text
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.utils import timezone


from videoJnd.src.ProcessRequest import process_request
from videoJnd.src.ResourceMonitor import wait_release_resources

def studyhit(request):
    # context = {}
    # context_items = [
    #   "availHeight", 
    #   "availWidth", 
    #   "browser_height_cm", 
    #   "browser_width_cm", 
    #   "cali_time", 
    #   "devicePixelRatio", 
    #   "didTraining", 
    #   "euid", 
    #   "hasCalibrated", 
    #   "outerHeight", 
    #   "outerWidth", 
    #   "px_cm_rate", 
    #   "puid",
    #   "workerid"
    # ]

    # cali_info = request.GET.get('info', None).split("-")
    # for idx, key in enumerate(context_items):
    #     context[key] = cali_info[idx]

    return render(request,'studyhit.html')
    # return render(request,'studyhit.html', context)

def quahit(request):
    return render(request,'quahit.html')

wait_release_resources()

@csrf_exempt
def scheduler(request):
    return JsonResponse(process_request(request), safe=False)