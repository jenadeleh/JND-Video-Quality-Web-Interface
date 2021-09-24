from django.utils import timezone

from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.models import VideoGroupObj, Experiment, Participant, InterfaceText, Assignment, EncodedRefVideoObj
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
            avl_encoded_ref_videos  = select_encoded_ref_videos(cur_exp_obj, recv_data["workerid"])

            if avl_encoded_ref_videos:
                cur_p = Participant.objects.filter(workerid=recv_data["workerid"])[0]
                finished_assignment_num = len(Assignment.objects.filter(workerid=recv_data["workerid"], exp=cur_exp_obj))

                if cur_p.ongoing == True:# ongoing, return current videos      
                    videos = ast.literal_eval(cur_p.videos)

                    cur_p.ref_videos_remain.items()

                    random.shuffle(videos)
                    cur_p.start_date  = timezone.now()
                    cur_p.save() # update start date 
                    _response = {
                        "videos":videos, 
                        "wait_time":cur_exp_obj.wait_time,
                        "download_time":cur_exp_obj.download_time
                    }


                    return {"status":"successful", "restype": "req_videos", "data":_response}

                elif cur_p.ongoing == False:# not ongoing, return new videos
                    _response = {}
                    videos_info = _extract_info_avl_videos(exp_config, 
                                                            recv_data["pname"], 
                                                            recv_data["workerid"], 
                                                            avl_encoded_ref_videos)
                    
                    if not cur_p.start_date:
                        cur_p.start_date  = timezone.now()
                    cur_p.ongoing  = True
                    cur_p.videos = str(videos_info)
                    cur_p.save()

                    _response["videos"] =  videos_info
                    _response["wait_time"] =  cur_exp_obj.wait_time
                    _response["download_time"] =  cur_exp_obj.download_time
                    _response["finished_assignment_num"] = finished_assignment_num

                    return {"status":"successful", "restype": "req_videos", "data":_response}
            else:
                return {"status":"failed", "restype": "req_videos", "data":interface_text.text_end_exp}
        else:
            return {"status":"failed", "restype": "req_videos", "data":interface_text.no_available_exp}
    else:
        return {"status":"failed", "restype": "req_videos", "data":"experiment is not exist"}
    
def select_encoded_ref_videos(cur_exp_obj:object, _workerid:str) -> list:
    exp_config = cur_exp_obj.configuration
    removed_encoded_ref_videos = [] # for a worker, encoded_reference videos whose 
                                    # number of annotated reaches maximum should be removed for this worker
    
    if _workerid !="": # chrome has worker record
        cur_p = Participant.objects.filter(workerid=_workerid, exp=cur_exp_obj)
        if cur_p:
            cur_p = cur_p[0]
            for encoded_ref_video,remain_num in cur_p.ref_videos_remain.items():
                if remain_num >= cur_exp_obj.max_ref_per_worker:
                    removed_encoded_ref_videos.append(encoded_ref_video)

    # filter encoded reference videos that are not finished and not ongoing
    avl_encoded_ref_videos = EncodedRefVideoObj.objects.filter(
                                                exp=cur_exp_obj
                                            ).filter(
                                                is_finished=False
                                            ).filter(
                                                ongoing=False
                                            )
    
    # available encoded reference videos for this worker
    avl_encoded_ref_videos = [
        encoded_ref_videos for encoded_ref_videos in avl_encoded_ref_videos \
            if encoded_ref_videos not in removed_encoded_ref_videos
    ]

    if len(avl_encoded_ref_videos) >= exp_config["MAX_REF_VIDEO_PER_HIT"]:
        selected_encoded_ref_videos = random.sample(avl_encoded_ref_videos, exp_config["MAX_REF_VIDEO_PER_HIT"])
        return selected_encoded_ref_videos
    else:
        # if number of available videos is less than MAX_REF_VIDEO_PER_HIT, continue to return avl_encoded_ref_videos
        return avl_encoded_ref_videos

def _extract_info_avl_videos(exp_config:dict, pname:str, workerid:str, avl_videos:list) -> list:
    output = []
    for video_obj in avl_videos:
        # update video
        _add_p_to_video(video_obj, pname, workerid)
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

def _add_p_to_video(video_obj:object, pname:str, workerid:str) -> None:
    video_obj.ongoing = True
    video_obj.cur_participant = pname
    video_obj.cur_participant_uid = workerid
    video_obj.save()
