from videoJnd.models import VideoGroupObj, Experiment, EncodedRefVideoObj
import uuid

def createVideoGroupObj(exp_db_obj:object) -> bool:
    exp_videos = VideoGroupObj.objects.filter(exp=exp_db_obj)
    if not exp_videos.exists():
        _create_videos_db(exp_db_obj)
        return True
    else:
        return False


def _create_videos_db(exp_db_obj:object) -> None:
    config = exp_db_obj.configuration

    for source_video in config["SRC_NAME"]:
        if source_video in config["FRAME_RATE"]["24"]:
            frame_rate = 24
        elif source_video in config["FRAME_RATE"]["30"]:
            frame_rate = 30

        codec_list = []
        if source_video in config["CODEC"]["264"]:
            codec_list.append("264")
        
        if source_video in config["CODEC"]["266"]:
            codec_list.append("266")

        for codec in codec_list:
            ref_video = f"src-{source_video}_codec-{codec}"

            EncodedRefVideoObj(
                ref_video = ref_video
                , exp = exp_db_obj
                , target_cnt = config["RATING_PER_REF_VIDEO"]
            ).save()

            for crf in config["CRF"]:
                ref_video_url = config["URL_PREFIX"] + config["REF_URL_POSTFIX"].format(
                    codec = codec
                    , src_name = source_video
                    , frame_rate = frame_rate
                    , crf = crf
                )

                distorted_url = config["URL_PREFIX"] + config["DIS_URL_POSTFIX"].format(
                    codec = codec
                    , src_name = source_video
                    , frame_rate = frame_rate
                    , crf = crf
                    , qp = "{qp}"
                )

                flickering_url = config["URL_PREFIX"] + config["FLK_URL_POSTFIX"].format(
                    codec = codec
                    , src_name = source_video
                    , frame_rate = frame_rate
                    , crf = crf
                    , qp = "{qp}"
                )

                VideoGroupObj(
                    exp = exp_db_obj
                    , ref_video = ref_video
                    , crf = crf
                    , codec = codec
                    , reference_url = ref_video_url
                    , distortion_url = distorted_url
                    , flickering_url = flickering_url  
                ).save()


    return None



