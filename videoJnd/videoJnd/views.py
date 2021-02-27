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

from videoJnd.src.QpObjsRecord import QpObjsRecord


# home page
def home(request):
    return render(request,'index.html')

# ----- init -----
qp_objs = QpObjsRecord()


@csrf_exempt
def scheduler(request):
    if request.method == "POST":
        if request.body:
            try:
                recv_data = json.loads(request.body)
                print(recv_data)
                if recv_data["action"] == "init":
                    # TODO: uuid
                    # TODO: update database
                    response = qp_objs.get_gp_next_stim()

                elif recv_data["action"] == "decision":
                    decision = recv_data["decision"]
                    start_time = recv_data["start_time"]
                    end_time = recv_data["end_time"]

                    # TODO: update database
                    qp_objs.update_gp_qp_params(decision)
                    response = qp_objs.get_gp_next_stim()

                return JsonResponse(response, safe=False)
                
            except Exception as e:
                print(e)
                return JsonResponse({"status":"failed"}, safe=False)

    return HttpResponseRedirect('/')




