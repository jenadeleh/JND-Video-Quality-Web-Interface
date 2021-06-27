from django.utils import timezone

from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.models import VideoObj, Experiment, Participant, InterfaceText
from videoJnd.src.GenUrl import gen_video_url, random_side


import random
import ast

qp_obj = QuestPlusJnd()

def req_videos(recv_data:dict) -> dict:
    cur_exp_obj = Experiment.objects.filter(euid=recv_data["euid"])
    interface_text = InterfaceText.objects.all()[0]
    if cur_exp_obj:
        cur_exp_obj = cur_exp_obj[0]
        exp_config = cur_exp_obj.configuration

        if cur_exp_obj.active == True:
            avl_videos  = select_videos(cur_exp_obj)

        
            if avl_videos:
                cur_p = Participant.objects.filter(puid=recv_data["puid"])[0]

                if cur_p.ongoing == True:# ongoing, return current videos      
                    videos = ast.literal_eval(cur_p.videos)
                    random.shuffle(videos)
                    cur_p.start_date  = timezone.now()
                    cur_p.save() # update start date 
                    _response = {
                        "videos":videos, 
                        "wait_time":cur_exp_obj.wait_time,
                        "download_time":cur_exp_obj.download_time
                    }

                    print("+++++++")
                    print(cur_p.ongoing)

                    return {"status":"successful", "restype": "req_videos", "data":_response}

                elif cur_p.ongoing == False:# not ongoing, return new videos
                    _response = {}
                    videos_info = _extract_info_avl_videos(exp_config, 
                                                            recv_data["pname"], 
                                                            recv_data["puid"], 
                                                            avl_videos)
                    
                    if not cur_p.start_date:
                        cur_p.start_date  = timezone.now()
                    cur_p.ongoing  = True
                    cur_p.videos = str(videos_info)
                    cur_p.save()

                    _response["videos"] =  videos_info
                    _response["wait_time"] =  cur_exp_obj.wait_time
                    _response["download_time"] =  cur_exp_obj.download_time

                    return {"status":"successful", "restype": "req_videos", "data":_response}
            else:
                return {"status":"failed", "restype": "req_videos", "data":interface_text.text_end_exp}
        else:
            return {"status":"failed", "restype": "req_videos", "data":interface_text.no_available_exp}
    else:
        return {"status":"failed", "restype": "req_videos", "data":"experiment is not exist"}
    
def select_videos(cur_exp_obj:object) -> list:
    exp_config = cur_exp_obj.configuration

    # filter videos that are not finished and not ongoing
    avl_videos_pool = VideoObj.objects.filter(
                                        exp=cur_exp_obj
                                    ).filter(
                                        is_finished=False
                                    ).filter(
                                        ongoing=False
                                    )

    
    # filter videos that have different content
    avl_src = exp_config["SRC_NAME"]
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

        if len(avl_videos) == exp_config["MAX_VIDEO_NUM_PER_HIT"]:
            return avl_videos

    # if number of available videos is less than MAX_VIDEO_NUM_PER_HIT, continue to return avl_videos
    return avl_videos

def _extract_info_avl_videos(exp_config:dict, pname:str, puid:str, avl_videos:list) -> list:
    output = []
    for video_obj in avl_videos:
        # update video
        _add_p_to_video(video_obj, pname, puid)
        video_uuid, source_video, codec, frame_rate, crf, side, qp_count, qp, url = _gen_video_url(exp_config, video_obj)

        output.append({"vuid":str(video_uuid), 
                        "source_video":source_video, 
                        "codec": codec,
                        "frame_rate": frame_rate, 
                        "crf": crf,
                        "side":side, 
                        "qp":str(qp), 
                        "qp_count": qp_count,
                        "url":url})
    
    return output

def _gen_video_url(exp_config:object, video_obj:object) -> tuple:
    if video_obj.result_code:
        result_code = video_obj.result_code.split(",")
    else:
        result_code = []

    # generate qp value
    qp = qp_obj.update_params(qp_obj.gen_qp_param(video_obj.codec), result_code)

    # generate url
    side  = random_side()
    url = gen_video_url(exp_config["URL_PREFIX"], 
                        exp_config["URL_POSTFIX"],
                        video_obj.codec, 
                        video_obj.source_video, 
                        video_obj.frame_rate, 
                        video_obj.crf, 
                        qp, 
                        side)

    return (str(video_obj.vuid), 
            video_obj.source_video, 
            video_obj.codec, 
            video_obj.frame_rate, 
            video_obj.crf, 
            side,
            video_obj.qp_count, 
            qp, 
            url)

def _add_p_to_video(video_obj:object, pname:str, puid:str) -> None:
    video_obj.ongoing = True
    video_obj.cur_participant = pname
    video_obj.cur_participant_uid = puid
    video_obj.save()
