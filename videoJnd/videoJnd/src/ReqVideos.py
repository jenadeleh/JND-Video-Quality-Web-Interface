from django.utils import timezone

from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.models import VideoObj, Experiment, Participant
from videoJnd.src.GetConfig import get_config
from videoJnd.src.GenUrl import gen_video_url, random_side


import random
import uuid
import copy
import ast

config = get_config()
VIDEO_NUM_PER_HIT = config["VIDEO_NUM_PER_HIT"]
RATING_PER_SRC = config["RATING_PER_SRC"]
URL_PREFIX = config["URL_PREFIX"]
SRC_NAME = config["SRC_NAME"]

qp_obj = QuestPlusJnd()

#TODO: threading blocking
#TODO: Class

def req_videos(recv_data:dict) -> dict:
    """
    select <VIDEO_NUM_PER_HIT> videos which are not ongoing(ongoing=False).
    """
    cur_exp_obj = Experiment.objects.all()[0]
    avl_videos  = _select_videos(cur_exp_obj)

    if avl_videos:
        cur_p = Participant.objects.filter(puid=recv_data["puid"])
        
        if cur_p:
            cur_p = cur_p[0]
            if cur_p.ongoing == True:# ongoing, return current videos      
                        
                videos = ast.literal_eval(cur_p.videos)
                random.shuffle(videos)
                _response = {"videos":videos}

                return {"status":"successful", "restype": "req_videos", "data":_response}

            elif cur_p.ongoing == False:# not ongoing, return new videos
                _response = {"videos":[]}
                _p_start_date = str(timezone.now())
                videos_info = _extract_info_avl_videos(recv_data["pname"], 
                                                        recv_data["puid"], 
                                                        _p_start_date, 
                                                        avl_videos)
                
                cur_p.start_date = _p_start_date
                cur_p.ongoing = True
                cur_p.videos = str(videos_info)
                cur_p.save()

                _response["videos"] =  {"videos":videos_info}

                return {"status":"successful", "restype": "req_videos", "data":_response}
        else:
            return {"status":"failed", "restype": "req_videos", "data":"participant is not exist"}
    else:
        return {"status":"failed", "restype": "req_videos", "data":"no videos are available"}
    
def _select_videos(cur_exp_obj:object) -> list:
    # filter videos that are not finished and not ongoing
    avl_videos_pool = VideoObj.objects.filter(
                                        exp=cur_exp_obj
                                    ).filter(
                                        is_finished=False
                                    ).filter(
                                        ongoing=False
                                    )

    
    # filter videos that have different content
    avl_src = copy.deepcopy(SRC_NAME)
    avl_videos = []

    # select the videos randomly
    select_idx = list(range(avl_videos_pool.count()))
    random.shuffle(select_idx)

    for idx in select_idx:
        video = avl_videos_pool[idx]
        src_name = video.source_video
        if src_name in avl_src:
            avl_videos.append(video)
            avl_src.remove(src_name)

        if len(avl_videos) == VIDEO_NUM_PER_HIT:
            return avl_videos

    # if number of available videos is less than VIDEO_NUM_PER_HIT, then return []
    return []

def _extract_info_avl_videos(pname:str, puid:str, pstart_date:str, avl_videos:list) -> list:
    output = []
    for video_obj in avl_videos:
        # update video
        _add_p_to_video(video_obj, pname, puid, pstart_date)
        video_uuid, side, qp, url = _gen_video_url(video_obj)
        output.append({"vuid":str(video_uuid), "side":side, "qp":str(qp), "url":url})
    
    return output

def _gen_video_url(video_obj:object) -> tuple:
    if video_obj.result_code:
        result_code = video_obj.result_code.split(",")
    else:
        result_code = []

    # generate qp value
    qp = qp_obj.update_params(qp_obj.gen_qp_param(video_obj.codec), result_code)
    # generate url
    side  = random_side()
    url = gen_video_url(video_obj.codec, 
                        video_obj.source_video, 
                        video_obj.frame_rate, 
                        video_obj.crf, 
                        qp, 
                        side)

    return (str(video_obj.vuid), side, qp, url)

def _add_p_to_video(video_obj:object, pname:str, puid:str, pstart_date:str) -> None:
    video_obj.ongoing = True
    video_obj.cur_participant = pname
    video_obj.cur_participant_uid = puid
    video_obj.participant_start_date = pstart_date
    video_obj.save()