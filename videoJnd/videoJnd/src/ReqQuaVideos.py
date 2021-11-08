from django.utils import timezone

from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.models import Experiment, StudyParticipant, InterfaceText, StudyAssignment, EncodedRefVideoObj
from videoJnd.src.GenUrl import gen_video_url, random_side
import random
from videoJnd.src.GetConfig import get_config

qp_obj = QuestPlusJnd()


def req_videos(recv_data:dict) -> dict:
    cur_exp_obj = Experiment.objects.filter(euid=recv_data["euid"])
    interface_text = InterfaceText.objects.all()[0]
    if cur_exp_obj:
        cur_exp_obj = cur_exp_obj[0]

        if cur_exp_obj.active == True:
            cur_p = StudyParticipant.objects.filter(puid=recv_data["puid"])[0]

            finished_assignment_num = len(
                StudyAssignment.objects.filter(
                    workerid=recv_data["workerid"]
                    , exp=cur_exp_obj
                )
            ) 

            if cur_p.ongoing == True:# ongoing, return current videos      
                ongoing_videos_pairs = cur_p.ongoing_videos_pairs
                distortion_videos_pairs = _shuffle_videos_pairs(ongoing_videos_pairs["distortion"])
                flickering_videos_pairs = _shuffle_videos_pairs(ongoing_videos_pairs["flickering"])

                ongoing_videos_pairs = {
                    "distortion":distortion_videos_pairs
                    , "flickering":flickering_videos_pairs
                }

                cur_p.ongoing_videos_pairs = ongoing_videos_pairs
                cur_p.start_date  = timezone.now()
                cur_p.save() 

                response_data = {
                    "videos_pairs": ongoing_videos_pairs
                    , "wait_time": cur_exp_obj.wait_time # TODO: remove in the future
                    , "download_time": cur_exp_obj.download_time # TODO: remove in the future
                    , "finished_assignment_num": finished_assignment_num
                }

                return {"status":"successful", "restype": "req_videos", "data":response_data}

            elif cur_p.ongoing == False:# not ongoing, return new videos
                avl_encoded_ref_videos_objs  = select_encoded_ref_videos(cur_exp_obj, recv_data["puid"])

                if len(avl_encoded_ref_videos_objs) > 0:
                    (
                        distortion_videos_pairs
                        , flickering_videos_pairs
                    ) = _output_videos_pairs(
                        recv_data["workerid"],
                        recv_data["puid"], 
                        avl_encoded_ref_videos_objs
                    )

                    ongoing_videos_pairs = {
                        "distortion":distortion_videos_pairs
                        , "flickering":flickering_videos_pairs
                    }

                    if not cur_p.start_date:
                        cur_p.start_date  = timezone.now()

                    cur_p.ongoing  = True
                    cur_p.ongoing_encoded_ref_videos = {
                        "ongoing_encoded_ref_videos":[
                            obj.ref_video for obj in avl_encoded_ref_videos_objs
                        ]
                    }
                    cur_p.ongoing_videos_pairs = ongoing_videos_pairs
                    cur_p.save()

                    response_data = {
                        "videos_pairs": ongoing_videos_pairs
                        , "wait_time": cur_exp_obj.wait_time # TODO: remove in the future
                        , "download_time": cur_exp_obj.download_time # TODO: remove in the future
                        , "finished_assignment_num": finished_assignment_num
                    }

                    return {"status":"successful", "restype": "req_videos", "data":response_data}
                else: # no encoded reference videos are available
                    return {"status":"failed", "restype": "req_videos", "data":interface_text.text_end_exp}
        else:
            return {"status":"failed", "restype": "req_videos", "data":interface_text.no_available_exp}
    else:
        return {"status":"failed", "restype": "req_videos", "data":"experiment is not exist"}
    
def select_encoded_ref_videos(cur_exp_obj:object, puid:str) -> list:

    exp_config = cur_exp_obj.configuration
    removed_encoded_ref_videos = [] # for a worker, encoded_reference videos whose 
                                    # number of annotated reaches maximum should be removed for this worker
    
    if puid !="": # chrome has worker record
        cur_p = StudyParticipant.objects.filter(puid=puid, exp=cur_exp_obj)
        if cur_p:
            cur_p = cur_p[0]
            for encoded_ref_video,rating_num in cur_p.finished_ref_videos.items():
                if rating_num >= cur_exp_obj.max_ref_per_worker * 2: # flickering + distortion
                    removed_encoded_ref_videos.append(encoded_ref_video)

    # filter encoded reference videos that are not finished and not ongoing
    avl_encoded_ref_videos_objs = EncodedRefVideoObj.objects.filter(
                                                exp=cur_exp_obj
                                            ).filter(
                                                is_finished=False
                                            ).filter(
                                                ongoing=False
                                            )

    # available encoded reference videos for this worker
    avl_encoded_ref_videos_objs = [
        obj for obj in avl_encoded_ref_videos_objs \
            if obj.ref_video not in removed_encoded_ref_videos
    ]

    if len(avl_encoded_ref_videos_objs) >= exp_config["MAX_ENCODED_REF_VIDEO_PER_HIT"]:
        selected_encoded_ref_videos = random.sample(
            avl_encoded_ref_videos_objs, 
            exp_config["MAX_ENCODED_REF_VIDEO_PER_HIT"]
        )
        return selected_encoded_ref_videos
    else:
        # if number of available videos is less than MAX_ENCODED_REF_VIDEO_PER_HIT, continue to return avl_encoded_ref_videos_objs
        return avl_encoded_ref_videos_objs

def _shuffle_videos_pairs(videos_pairs_list:list) -> list:
    videos_pairs_list = videos_pairs_list
    for idx, pair in enumerate(videos_pairs_list):
        videos_pair = pair["videos_pair"]
        side_of_reference = pair["side_of_reference"]
        reference_url = videos_pair[{"L":0, "R":1}[side_of_reference]]
        random.shuffle(videos_pair)
        side_of_reference = ["L", "R"][videos_pair.index(reference_url)]
        videos_pairs_list[idx]["videos_pair"] = videos_pair
        videos_pairs_list[idx]["side_of_reference"] = side_of_reference

    random.shuffle(videos_pairs_list)
    return videos_pairs_list

def _output_videos_pairs(
    workerid:str, 
    puid:str, 
    avl_encoded_ref_videos_objs:list
) -> tuple:

    output_distortion_videos_pairs = []
    output_flickering_videos_pairs = []

    for encoded_ref_video_obj in avl_encoded_ref_videos_objs:
        _add_worker_to_obj(encoded_ref_video_obj, workerid, puid)
        distortion_videos_pairs, flickering_videos_pairs = _gen_videos_pairs(encoded_ref_video_obj)
        output_distortion_videos_pairs += distortion_videos_pairs
        output_flickering_videos_pairs += flickering_videos_pairs
    
    random.shuffle(output_distortion_videos_pairs)
    random.shuffle(output_flickering_videos_pairs)

    return (output_distortion_videos_pairs, output_flickering_videos_pairs)

def _add_worker_to_obj(encoded_ref_video_obj:object, workerid:str, puid:str) -> None:
    encoded_ref_video_obj.ongoing = True
    encoded_ref_video_obj.cur_workerid = workerid
    encoded_ref_video_obj.cur_participant_uid = puid
    encoded_ref_video_obj.save()

def _gen_videos_pairs(encoded_ref_video_obj:object) -> tuple:

    refuid = str(encoded_ref_video_obj.refuid)
    ref_video = encoded_ref_video_obj.ref_video
    videoGroupsResult = encoded_ref_video_obj.videoGroupsResult
    codec = encoded_ref_video_obj.codec

    distortion_videos_pairs = []
    flickering_videos_pairs = []
    
    for crf, crf_group in videoGroupsResult.items():
        prev_distortion_qp = crf_group["proc_distortion_d_code"]
        prev_flickering_qp = crf_group["proc_flickering_d_code"]

        if encoded_ref_video_obj.curr_qp_cnt == 0: 
            # initial qp value, codec264=30, codec266=37
            prev_distortion_qp = [0]
            prev_flickering_qp = [0]

        next_distortion_qp = qp_obj.update_params(
                                qp_obj.gen_qp_param(codec)
                                , prev_distortion_qp
                            )

        next_flickering_qp = qp_obj.update_params(
                                qp_obj.gen_qp_param(codec)
                                , prev_flickering_qp
                            )
        
        reference_url = crf_group["reference_url"].format()
        distortion_url = crf_group["distortion_url"].format(qp=next_distortion_qp)
        flickering_url = crf_group["flickering_url"].format(qp=next_flickering_qp)

        distortion_pair = [reference_url, distortion_url]
        random.shuffle(distortion_pair)
        distortion_side_of_reference = ["L", "R"][distortion_pair.index(reference_url)]

        flickering_pair = [reference_url, flickering_url]
        random.shuffle(flickering_pair)
        flickering_side_of_reference = ["L", "R"][flickering_pair.index(reference_url)]

        distortion_videos_pairs.append({
            "refuid":refuid
            , "ref_video":ref_video
            , "presentation": "distortion"
            , "crf": crf
            , "qp": next_distortion_qp
            , "videos_pair":distortion_pair
            , "side_of_reference":distortion_side_of_reference
        })

        flickering_videos_pairs.append({
            "refuid": refuid
            , "ref_video": ref_video
            , "presentation": "flickering"
            , "crf": crf
            , "qp": next_flickering_qp
            , "videos_pair": flickering_pair
            , "side_of_reference":flickering_side_of_reference
        })

    return (distortion_videos_pairs, flickering_videos_pairs)

