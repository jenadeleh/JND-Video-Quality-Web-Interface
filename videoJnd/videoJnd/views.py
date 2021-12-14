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
    return render(request,'studyhit.html')
    # return render(request,'studyhit.html', context)

def quahit(request):
    return render(request,'quahit.html')

try:
    wait_release_resources()
except:
    pass
    
@csrf_exempt
def scheduler(request):
    return JsonResponse(process_request(request), safe=False)