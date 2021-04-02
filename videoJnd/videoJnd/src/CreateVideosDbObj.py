from videoJnd.models import VideoObj, Experiment
import uuid

def createVideosDbObj(exp_db_obj:object) -> bool:
    if _doesExpVideosExist(exp_db_obj) == False:
        _create_videos_db(exp_db_obj)
        exp_db_obj.has_created_videos = True
        exp_db_obj.save()
        return True
    else:
        return False

def _doesExpVideosExist(exp_db_obj) -> bool:
    exp_videos = VideoObj.objects.filter(exp=exp_db_obj)
    if exp_videos.exists():
        return True
    else:
        return False

def _create_videos_db(exp_db_obj) -> None:
    config = exp_db_obj.configuration
    source_video = config["SRC_NAME"]
    rating = config["RATING_PER_SRC"]
    frame_rate = config["FRAME_RATE"]
    crf = config["CRF"]
    codec = config["CODEC"]
    f_24_videos = frame_rate["24"]
    f_30_videos = frame_rate["30"]

    for _source_video in source_video:
        if _source_video in f_24_videos:
            _frame_rate = 24
        elif _source_video in f_30_videos:
            _frame_rate = 30

        for _crf in crf:
            for _codec in codec:
                for _rating in range(rating):
                    VideoObj(vuid = uuid.uuid4()
                            , exp = exp_db_obj
                            , source_video = _source_video
                            , codec = _codec
                            , frame_rate = _frame_rate
                            , crf = ("0"+_crf)[-2:]
                            , rating = _rating+1).save()




