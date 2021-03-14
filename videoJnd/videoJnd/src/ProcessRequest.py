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


from videoJnd.src.SelectVideos import select_videos
from videoJnd.src.RecordResult import record_result


def process_request(request):
    try:
        if request.method == "POST":
            if request.body:
                    recv_data = json.loads(request.body)
                    print("---------------------")
                    print(recv_data)
                    print("---------------------")

                    if recv_data["action"] == "select_videos":
                        response = select_videos(recv_data)

                    elif recv_data["action"] == "record_result":
                        response = record_result(recv_data)
            else:
                response = {"status":"failed", "data":"empty request body"}
        else:
            response = {"status":"failed", "data":"bad method"}

    except Exception as e:
        print(str(e))
        response = {"status":"failed", "data":"errors"}

    return response





