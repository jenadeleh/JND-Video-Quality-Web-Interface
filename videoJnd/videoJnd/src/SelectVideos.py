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

def select_videos(recv_data:dict) -> dict:
    """
    select <VIDEO_NUM_PER_HIT> videos which are not ongoing(ongoing=False).
    """

    curr_exp_obj = Experiment.objects.filter(name=recv_data["exp"])[0]

    avl_videos  = _select_videos(curr_exp_obj)

    if avl_videos:
        if recv_data["puid"] == "": # new participant

            _response = {"puid":"", "videos":[]}
            _puid = uuid.uuid4()
            _p_start_date = str(timezone.now())

            _response["puid"] = _puid

            videos_info = _extract_info_avl_videos(recv_data["pname"]
                                                , _puid
                                                , _p_start_date
                                                , avl_videos)

            _response["videos"] = videos_info
                
            # add a new participant
            Participant(puid = _puid
                , name = recv_data["pname"]
                , exp = curr_exp_obj
                , start_date = _p_start_date
                , ongoing = True
                , videos = str(_response["videos"])).save()

            return {"status":"successful", "data":_response}

        else: # not a new user
            _puid = recv_data["puid"]
            curr_p = Participant.objects.filter(puid=_puid)
            
            if curr_p:
                curr_p = curr_p[0]
                if curr_p.ongoing == True:# ongoing, return current videos      
                            
                    videos = ast.literal_eval(curr_p.videos)
                    random.shuffle(videos)
                    _response = {"videos":videos}
                    return {"status":"successful", "data":_response}

                elif curr_p.ongoing == False:# not ongoing, return new videos
                    _response = {"videos":[]}
                    _p_start_date = str(timezone.now())
                    videos_info = _extract_info_avl_videos(recv_data["pname"], 
                                                            recv_data["puid"], 
                                                            _p_start_date, 
                                                            avl_videos)
                    
                    curr_p.start_date = _p_start_date
                    curr_p.ongoing = True
                    curr_p.videos = str(videos_info)
                    curr_p.save()

                    _response["videos"] = videos_info
                    return {"status":"successful", "data":_response}
            else:
                return {"status":"failed", "data":"participant is not exist"}
    else:
        return {"status":"failed", "data":"no videos are available"}
    
def _select_videos(curr_exp_obj:object) -> list:
    # filter videos that are not finished and not ongoing
    avl_videos_pool = VideoObj.objects.filter(
                                        exp=curr_exp_obj
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
    video_obj.curr_participant = pname
    video_obj.curr_participant_uid = puid
    video_obj.participant_start_date = pstart_date
    video_obj.save()