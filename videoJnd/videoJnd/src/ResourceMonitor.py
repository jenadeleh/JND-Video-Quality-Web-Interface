
from videoJnd.models import VideoObj, Experiment, Participant, InterfaceText
from django.utils import timezone
import ast
import threading
import time
import calendar

from videoJnd.src.Log import logger


monitor_threads = []
idle_threads = [] # when user start the exp. before expiration, threading does nothing

def resource_monitor(recv_data:dict) -> dict:
    p_obj = Participant.objects.filter(puid=recv_data["puid"]).first()

    # if not p_obj.start_date:
    #     p_obj.start_date  = timezone.now()
    # p_obj.ongoing  = True
    # p_obj.save()

    if recv_data["puid"] not in monitor_threads and recv_data["puid"] not in idle_threads:
        _start_thread(p_obj)

    waiting_timeout_msg = InterfaceText.objects.all().first().waiting_timeout_msg
    download_timeout_msg = InterfaceText.objects.all().first().download_timeout_msg

    _response = {
        "status":"successful", 
        "data":{
            "start_date":int(1000 * p_obj.start_date.timestamp()), 
            "waiting_timeout_msg":waiting_timeout_msg,
            "download_timeout_msg":download_timeout_msg
            }
    }
    
    return _response

def _start_thread(p_obj):
    puid = str(p_obj.puid)
    thread = threading.Thread(target=_release_videos, name=puid, args=(monitor_threads, idle_threads, p_obj,))
    thread.start()
    monitor_threads.append(puid)

def _release_videos(monitor_threads:list, idle_threads:list, p_obj:object) -> None:
    videos = ast.literal_eval(p_obj.videos)
    videos_uid = [v["vuid"]for v in videos]
    duration = p_obj.exp.download_time +  p_obj.exp.wait_time# compensation for network delay 



    if p_obj.ongoing:
        start_date = p_obj.start_date
        time_diff = (timezone.now() - start_date).total_seconds()

        if time_diff >= duration:
            _config_released_resource(monitor_threads, idle_threads, p_obj, videos_uid)
        else:
            counter = int((duration - time_diff)*1000)
            for _ in range(counter):
                if str(p_obj.puid) in idle_threads:
                    break
                else:
                    time.sleep(0.001)
            # logger.info("++++ %s ++++" % str(idle_threads))
            _config_released_resource(monitor_threads, idle_threads, p_obj, videos_uid)

def _config_released_resource(monitor_threads:list, idle_threads:list, p_obj:object, videos_uid:list) -> None:
    # logger.info("_____release %s _______" % p_obj.puid)
    # logger.info(str(monitor_threads) + str(idle_threads))
    puid = str(p_obj.puid)
    if puid not in idle_threads:
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

        # logger.info("--- Release videos from participant: %s ---" % (p_obj.name))
    else:
        if puid in idle_threads:
            idle_threads.remove(puid)
    if puid in monitor_threads:
        monitor_threads.remove(puid)

    # logger.info(str(monitor_threads) + str(idle_threads))


def add_idle_thread(puid:str) -> None:
    if puid not in idle_threads:
        idle_threads.append(puid)

    # logger.info("===== new %s ====" % str(idle_threads))

def wait_release_resources():
    logger.info("--- Release videos ---")
    ongoing_p_obj = Participant.objects.filter(ongoing=True)

    for p_obj in ongoing_p_obj:
        _start_thread(p_obj)


def release_resource(recv_data:dict) -> None:

    try:
        if recv_data["puid"] in monitor_threads:
            add_idle_thread(recv_data["puid"])

        # logger.info("===== release_resource ====" )
        p_obj = Participant.objects.filter(puid=recv_data["puid"]).first()

        if p_obj and p_obj.videos:
            videos = ast.literal_eval(p_obj.videos)
            videos_uid = [v["vuid"]for v in videos]

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
    except Exception as e:
        logger.error(str(e))





            

    