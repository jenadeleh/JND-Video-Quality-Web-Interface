from typing import Text
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.utils import timezone

from videoJnd.src.InitDB import init_db
from videoJnd.src.ProcessRequests import process_requests

# home page
def home(request):
    return render(request,'index.html')

# ----- init -----
init_db()
print("\n-- Initialization Done --\n")

@csrf_exempt
def scheduler(request):
    return JsonResponse(process_requests(request), safe=False)


        
