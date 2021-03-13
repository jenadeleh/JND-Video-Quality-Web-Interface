from django.utils import timezone

from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.models import VideoObj, Experiment, Participant
from videoJnd.src.GetConfig import get_config
from videoJnd.src.GenUrl import gen_video_url


import random
import uuid
import copy
import ast


def record_decisions(recv_data:dict) -> dict:
    decision = recv_data["decision"]
    start_time = recv_data["start_time"]
    end_time = recv_data["end_time"]

    response = {}
    return response
