from typing import Text
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.utils import timezone


from videoJnd.src.ProcessRequest import process_request
from videoJnd.src.ResourceMonitor import wait_release_resources

# studyhit page
def studyhit(request):
    return render(request,'studyhit.html')

def quahit(request):
    return render(request,'quahit.html')

wait_release_resources()

@csrf_exempt
def scheduler(request):
    return JsonResponse(process_request(request), safe=False)