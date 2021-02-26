from typing import Text
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.utils import timezone

import json
import sys
import logging



# home page
def home(request):
    return render(request,'index.html')

# ----- init -----
# try:
#     [gp_src_uuid, qp_calculators] = initQpCalculators(GROUP_NUM, SRC_VIDEO_NUM)
#     gp_isAvailable = [True for _ in range(GROUP_NUM)]
# except Exception as e:
#     sys.exit("-- initial failed! -- \nerror: %s\n" % str(e))

@csrf_exempt
def scheduler(request):
    if request.method == "POST":
        if request.body:
            try:
                recv_data = json.loads(request.body)
                print(recv_data)
                if recv_data["action"] == "init":
                    pass

                elif recv_data["action"] == "decision":

                    # decision = recv_data["decision"]
                    # start_time = recv_data["start_time"]
                    # end_time = recv_data["end_time"]
                    
                    return JsonResponse({"video_url":"new video url"}, safe=False)
                
            except Exception as e:
                return JsonResponse({"status":"failed"}, safe=False)

    return HttpResponseRedirect('/')




