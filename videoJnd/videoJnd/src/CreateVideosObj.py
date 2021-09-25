from videoJnd.models import Experiment, EncodedRefVideoObj
import uuid

def createEncodedRefVideosDB(exp_db_obj:object) -> bool:
    exp_videos = EncodedRefVideoObj.objects.filter(exp=exp_db_obj)
    if not exp_videos.exists():
        _create_encoded_ref_videos_db(exp_db_obj)
        return True
    else:
        return False
 
def _create_encoded_ref_videos_db(exp_db_obj:object) -> None:
    config = exp_db_obj.configuration

    for source_video in config["SRC_NAME"]:

        frame_rate_list = []
        for _frame_rate, src_list in config["FRAME_RATE"].items():
            if source_video in src_list:
                frame_rate_list.append(_frame_rate)

        codec_list = []
        for _codec, src_list in config["CODEC"].items():
            if source_video in src_list:
                codec_list.append(_codec)

        for frame_rate in frame_rate_list:
            for codec in codec_list:
                for ratingIdx in range(config["RATING_PER_ENCODED_REF_VIDEO"]):

                    ref_video = f"src-{source_video}_codec-{codec}_ratingIdx-{ratingIdx+1}"

                    videoGroups = {}

                    for crf in config["CRF"]:
                        reference_url = config["URL_PREFIX"] + \
                            config["REF_URL_POSTFIX"].format(
                                codec = codec
                                , src_name = source_video
                                , frame_rate = frame_rate
                                , crf = crf
                            )

                        distortion_url = config["URL_PREFIX"] + \
                            config["DIS_URL_POSTFIX"].format(
                                codec = codec
                                , src_name = source_video
                                , frame_rate = frame_rate
                                , crf = crf
                                , qp = "{qp}"
                            )

                        flickering_url = config["URL_PREFIX"] + \
                            config["FLK_URL_POSTFIX"].format(
                                codec = codec
                                , src_name = source_video
                                , frame_rate = frame_rate
                                , crf = crf
                                , qp = "{qp}"
                            )

                        videoGroups[crf] = {
                            "reference_url": reference_url
                            , "distortion_url": distortion_url
                            , "flickering_url": flickering_url
                            , "proc_distortion_d_code": []
                            , "proc_flickering_d_code": []
                            , "ori_distortion_d_code": []
                            , "ori_flickering_d_code": []
                            , "ori_distortion_decision": []
                            , "ori_flickering_decision": []
                        }

                    EncodedRefVideoObj(
                        ref_video = ref_video
                        , exp = exp_db_obj
                        , videoGroups = videoGroups
                        , ratingIdx = ratingIdx + 1
                        , codec = codec
                    ).save()

    return None



