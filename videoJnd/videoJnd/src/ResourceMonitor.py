
from videoJnd.models import VideoObj, Experiment, Participant, InterfaceText
from django.utils import timezone
import ast
import _thread
import time
import calendar

from videoJnd.src.Log import logger


monitor_threads = []
expire_msg = InterfaceText.objects.all().first().expire_msg


def resource_monitor(recv_data:dict) -> dict:
    p_obj = Participant.objects.filter(puid=recv_data["puid"]).first()

    if not p_obj.start_date:
        p_obj.start_date  = timezone.now()
    p_obj.ongoing  = True
    p_obj.save()


    if recv_data["puid"] not in monitor_threads:
        _thread.start_new_thread(_release_videos, (p_obj,))

    return {"status":"successful", "data":{"start_date":int(1000 * p_obj.start_date.timestamp()), "expire_msg":expire_msg}}


def _release_videos(p_obj:object) -> None:
    videos = ast.literal_eval(p_obj.videos)
    videos_uid = [v["vuid"]for v in videos]
    duration = p_obj.exp.duration + 3 # compensation for network delay 
    monitor_threads.append(str(p_obj.puid))

    if p_obj.ongoing:
        start_date = p_obj.start_date
        time_diff = (timezone.now() - start_date).total_seconds()

        if time_diff >= duration:
            _config_released_resource(p_obj, videos_uid)
        else:
            time.sleep(duration - time_diff)
            _config_released_resource(p_obj, videos_uid)

def _config_released_resource(p_obj:object, videos_uid:list) -> None:
    p_obj.ongoing = False
    p_obj.videos = ""
    p_obj.start_date = None
    p_obj.save()

    ongoing_videos_obj = VideoObj.objects.filter(ongoing=True)
    for v in ongoing_videos_obj:
        if str(v.vuid) in videos_uid:
            v.ongoing = False
            v.cur_participant = ""
            v.cur_participant_uid = ""
            v.save()

    monitor_threads.remove(str(p_obj.puid))

    logger.info("--- Release videos from participant: %s ---" % (p_obj.name))

def wait_release_resources():
    logger.info("--- Release videos ---")
    ongoing_p_obj = Participant.objects.filter(ongoing=True)

    for p_obj in ongoing_p_obj:
        monitor_threads.append(str(p_obj.puid))
        _thread.start_new_thread(_release_videos, (p_obj,))

            

    