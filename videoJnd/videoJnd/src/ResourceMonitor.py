
from videoJnd.models import EncodedRefVideoObj, Participant, InterfaceText
from django.utils import timezone
import threading
import time


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
    thread = threading.Thread(
        target=_release_videos, 
        name=puid, 
        args=(
            monitor_threads, 
            idle_threads, 
            p_obj,
        )
    )
    thread.start()
    monitor_threads.append(puid)

def _release_videos(
    monitor_threads:list, 
    idle_threads:list, 
    p_obj:object
) -> None:

    ref_video = p_obj.ongoing_encoded_ref_videos["ongoing_encoded_ref_videos"] 
    #  ['src-006_codec-266_ratingIdx-2', 'src-001_codec-266_ratingIdx-2', 'src-121_codec-266_ratingIdx-1']
    duration = p_obj.exp.download_time +  p_obj.exp.wait_time# compensation for network delay 

    if p_obj.ongoing:
        start_date = p_obj.start_date
        time_diff = (timezone.now() - start_date).total_seconds()

        if time_diff >= duration:
            _config_released_resource(monitor_threads, idle_threads, p_obj, ref_video)
        else:
            counter = int((duration - time_diff)*1000)
            for _ in range(counter):
                if str(p_obj.puid) in idle_threads:
                    break
                else:
                    time.sleep(0.001)
            # logger.info("++++ %s ++++" % str(idle_threads))
            _config_released_resource(monitor_threads, idle_threads, p_obj, ref_video)

def _config_released_resource(
    monitor_threads:list, 
    idle_threads:list, 
    p_obj:object, 
    ref_video:list
) -> None:

    # logger.info("_____release %s _______" % p_obj.puid)
    # logger.info(str(monitor_threads) + str(idle_threads))
    puid = str(p_obj.puid)
    if puid not in idle_threads:
        p_obj.ongoing = False
        p_obj.ongoing_videos_pairs = {"distortion":[], "flickering":[]}
        p_obj.ongoing_encoded_ref_videos = {"ongoing_encoded_ref_videos":[]}
        p_obj.start_date = None
        p_obj.save()

        ongoing_ref_videos_obj = EncodedRefVideoObj.objects.filter(ongoing=True)

        for ref_video_obj in ongoing_ref_videos_obj:
            if str(ref_video_obj.ref_video) in ref_video:
                ref_video_obj.ongoing = False
                ref_video_obj.cur_workerid = None
                ref_video_obj.cur_worker_uid = None
                ref_video_obj.worker_start_date = None
                ref_video_obj.save()


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

    logger.info("===== new %s ====" % str(idle_threads))

def wait_release_resources():
    logger.info("--- Release videos ---")
    ongoing_p_obj = Participant.objects.filter(ongoing=True)

    if ongoing_p_obj:
        for p_obj in ongoing_p_obj:
            _start_thread(p_obj)


def release_resource(recv_data:dict) -> None:

    try:
        if recv_data["puid"] in monitor_threads:
            add_idle_thread(recv_data["puid"])

        # logger.info("===== release_resource ====" )
        p_obj = Participant.objects.filter(puid=recv_data["puid"]).first()

        if p_obj and p_obj.videos:
            ref_video = p_obj.ongoing_encoded_ref_videos["ongoing_encoded_ref_videos"] 
            p_obj.ongoing = False
            p_obj.ongoing_videos_pairs = {"distortion":[], "flickering":[]}
            p_obj.ongoing_encoded_ref_videos = {"ongoing_encoded_ref_videos":[]}
            p_obj.start_date = None
            p_obj.save()

            ongoing_ref_videos_obj = EncodedRefVideoObj.objects.filter(ongoing=True)

            for ref_video_obj in ongoing_ref_videos_obj:
                if str(ref_video_obj.ref_video) in ref_video:
                    ref_video_obj.ongoing = False
                    ref_video_obj.cur_workerid = None
                    ref_video_obj.cur_worker_uid = None
                    ref_video_obj.worker_start_date = None
                    ref_video_obj.save()

    except Exception as e:
        logger.error(str(e))





            

    