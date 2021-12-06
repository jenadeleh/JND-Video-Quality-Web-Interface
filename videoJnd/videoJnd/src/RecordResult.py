from django.utils import timezone
from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.models import EncodedRefVideoObj, Experiment, StudyParticipant, StudyAssignment
from videoJnd.src.GetConfig import get_config
from videoJnd.src.ResourceMonitor import add_idle_thread
import uuid


config = get_config()

def record_study_result(recv_data:dict) -> dict:
    p_obj = StudyParticipant.objects.filter(puid=recv_data["puid"])
    if p_obj:
        p_obj = p_obj[0]
        _result = recv_data["data"]["result"]
        cali_info = recv_data["data"]["cali_info"]
        os_info = recv_data["data"]["os_info"]
        
        exp_obj = Experiment.objects.filter(euid=recv_data["euid"])[0]

        auid = uuid.uuid4()
        StudyAssignment(
            auid = auid
            , exp = exp_obj
            , workerid = recv_data["workerid"]
            , puid = recv_data["puid"]
            , result = {"result": _result}
            , calibration = cali_info
            , operation_system = os_info
        ).save()

        exp_obj.study_hit_count = exp_obj.study_hit_count + 1
        exp_obj.save()

        finished_ref_videos = p_obj.finished_ref_videos
        process_count = {k["refuid"]:0 for k in _result}
        for video_result in _result:
            presentation = video_result["presentation"]

            ref_video_obj = EncodedRefVideoObj.objects.filter(refuid=video_result["refuid"])
            if ref_video_obj:
                ref_video_obj = ref_video_obj[0]

                # record the number of specific ref_video that participant has finished
                if ref_video_obj.ref_video in finished_ref_videos:
                    finished_ref_videos[ref_video_obj.ref_video] += 1
                else:
                    finished_ref_videos[ref_video_obj.ref_video] = 1

                _update_video_db(presentation, video_result, ref_video_obj, str(auid))

                process_count[video_result["refuid"]] += 1
                if process_count[video_result["refuid"]] == 2*config["RATING_PER_ENCODED_REF_VIDEO"]: #???
                    # record result of distortion and flicerking
                    ref_video_obj.ongoing = False
                    ref_video_obj.save()

            else:
                return {
                    "status": "failed", 
                    "restype": "record_result",
                    "data": "video %s is not exist" % recv_data["puid"]
                }

        _set_p_onging_false(p_obj)

        p_obj.finished_ref_videos = finished_ref_videos
        p_obj.save()


        return {"status":"successful", "restype": "record_result", "code":auid}
    else:
        return {"status":"failed", "restype": "record_result", "data":"participant is not exist"}

def _update_video_db(
    presentation: str,
    video_result:dict, 
    ref_video_obj:object, 
    auid:str
) -> None:
    # update videoGroupsResult
    refuid = video_result["refuid"]
    presentation = video_result["presentation"]

    # update qp sequence
    flickering_qp = ref_video_obj.flickering_qp
    distortion_qp = ref_video_obj.distortion_qp

    flickering_response = ref_video_obj.flickering_response
    distortion_response = ref_video_obj.distortion_response

    if presentation == "flickering":
        decision_code = _encode_decision_flickering(
            video_result["side_of_reference"], 
            video_result["decision"]
        )

        flickering_qp["flickering_qp_seq"].append(video_result["qp"])
        ref_video_obj.flickering_qp = flickering_qp

        flickering_response["flickering_response"].append(decision_code)
        ref_video_obj.flickering_response = flickering_response

    elif presentation == "distortion":
        decision_code = _encode_decision_distortion(
            video_result["side_of_reference"], 
            video_result["decision"]
        )
        distortion_qp["distortion_qp_seq"].append(video_result["qp"])
        ref_video_obj.distortion_qp = distortion_qp

        distortion_response["distortion_response"].append(decision_code)
        ref_video_obj.distortion_response = distortion_response

    videoGroupsResult = ref_video_obj.videoGroupsResult

    videoGroupsResult[video_result["crf"]][
        f"ori_{presentation}_decision"
    ].append(video_result["decision"])

    videoGroupsResult[video_result["crf"]][
        f"side_of_reference_{presentation}"
    ].append(video_result["side_of_reference"])

    videoGroupsResult[video_result["crf"]][
        f"proc_{presentation}_d_code"
    ].append(decision_code)

    ref_video_obj.videoGroupsResult = videoGroupsResult



    # update assigments sequence
    assigments_sequence = ref_video_obj.assigments_sequence
    assigments_sequence["sequence"].append(auid)
    ref_video_obj.assigments_sequence = assigments_sequence

    # decide ref_video_obj is finished or not
    if decision_code != "4": # exclude decision code 4
        ref_video_obj.curr_qp_cnt = ref_video_obj.curr_qp_cnt + 1

    if ref_video_obj.curr_qp_cnt == 2 * ref_video_obj.target_qp_num:
        ref_video_obj.is_finished = True
    
    # set some status
    ref_video_obj.ongoing = False
    ref_video_obj.cur_workerid = None
    ref_video_obj.cur_worker_uid = None
    ref_video_obj.worker_start_date = None
    ref_video_obj.save()

def _set_p_onging_false(p_obj: object) -> None:
    p_obj.ongoing = False
    p_obj.ongoing_videos_pairs = {"distortion":[], "flickering":[]}
    p_obj.ongoing_encoded_ref_videos = {"ongoing_encoded_ref_videos":[]}
    p_obj.start_date = None
    p_obj.save()


def _encode_decision_flickering(side_of_reference:str, decision:str) -> str:
    if decision == "R" or decision == "L":
        if decision == side_of_reference:
            return "1"
        elif decision != side_of_reference:
            return "2"
    elif decision == "not sure":
        return "3"
    elif decision == "no decision":
        return "4"

def _encode_decision_distortion(side_of_reference:str, decision:str) -> str:
    if decision == "R" or decision == "L":
        if decision == side_of_reference:
            return "2"
        elif decision != side_of_reference:
            return "1"
    elif decision == "not sure":
        return "3"
    elif decision == "no decision":
        return "4"

