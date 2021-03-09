from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.http import JsonResponse

from random import randint
import json
import json
import sys
import logging


from videoJnd.src.QuestPlusJnd import QuestPlusJnd

qp_obj = QuestPlusJnd()


def process_requests(request):
    try:
        if request.method == "POST":
            if request.body:
                    recv_data = json.loads(request.body)

                    if recv_data["action"] == "init":
                        response =_init_gui()

                    elif recv_data["action"] == "decision":
                        response = _process_decision(recv_data)
            else:
                response = {"status":"failed", "data":"empty"}
        else:
            response = {"status":"failed", "data":"badcmd"}

    except Exception as e:
        response = {"status":"failed", "data":"errors"}

    return response

def _init_gui() -> dict:
    codec = "264"
    decisions = [str(randint(1,3)) for _ in range(5)]

    print(codec, decisions)
    next_stim = qp_obj.update_params(qp_obj.gen_qp_param(codec), decisions)
    response = {"next_stim":next_stim}
    
    return response

def _process_decision(recv_data:dict) -> dict:
    decision = recv_data["decision"]
    start_time = recv_data["start_time"]
    end_time = recv_data["end_time"]

    response = {}
    return response


