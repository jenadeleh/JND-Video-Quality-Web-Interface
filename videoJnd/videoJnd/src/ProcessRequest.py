from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.http import JsonResponse
from django.utils import timezone

import random
import json
import sys
import logging
import uuid
import copy
import ast


from videoJnd.src.ReqVideos import req_videos
from videoJnd.src.RecordResult import record_result
from videoJnd.src.ReqInstConsentF import req_inst_cf
from videoJnd.src.UserRegister import user_register
from videoJnd.src.ResourceMonitor import resource_monitor

from videoJnd.src.Log import logger

def process_request(request):
    # try:
    if request.method == "POST":
        if request.body:
                recv_data = json.loads(request.body)
                logger.info("\n---------------------\n%s\n---------------------" % str(recv_data))

                if recv_data["action"] == "req_inst_cf":
                    response = req_inst_cf(recv_data["puid"])
                
                elif recv_data["action"] == "user_register":
                    response = user_register(recv_data)

                elif recv_data["action"] == "req_videos":
                    response = req_videos(recv_data)

                elif recv_data["action"] == "resource_monitor":
                    response = resource_monitor(recv_data)

                elif recv_data["action"] == "record_result":
                    response = record_result(recv_data)
        else:
            response = {"status":"failed", "restype":"request-body", "data":"empty request body"}
    else:
        response = {"status":"failed", "restype":"request-method", "data":"bad method"}

    # except Exception as e:
    #     print(str(e))
    #     response = {"status":"failed", "restype":"request-send", "data":"errors"}

    return response






