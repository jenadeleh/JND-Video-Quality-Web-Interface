from videoJnd.models import VideoObj, Experiment
from videoJnd.src.GetConfig import get_config
import uuid

config = get_config()

exp_name = config["EXP"]
source_video = config["SRC_NAME"]
rating = config["RATING_PER_SRC"]
frame_rate = config["FRAME_RATE"]
crf = config["CRF"]
codec = config["CODEC"]
f_24_videos = frame_rate["24"]
f_30_videos = frame_rate["30"]

    
def init_db() -> None:
    if _isNewExpExists() == False:
        exp_db_obj = _create_exp_db()
        _create_videos_db(exp_db_obj)

def _create_videos_db(exp_db_obj) -> None:
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

def _create_exp_db() -> object:
    exp_db_obj = Experiment(euid = uuid.uuid4()
                , name = exp_name
                , source_video = source_video
                , rating = rating)
    exp_db_obj.save()
    
    return exp_db_obj

def _isNewExpExists() -> bool:
    new_exp = Experiment.objects.filter(name=exp_name)
    if new_exp.exists():
        return True
    else:
        return False

