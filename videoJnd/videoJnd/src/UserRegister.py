from django.utils import timezone

from videoJnd.models import Participant, Experiment
from videoJnd.src.Log import logger
import uuid

def user_register(recv_data:dict) -> dict:
    try:
        active_exps = Experiment.objects.filter(active=True)
        if active_exps:
            active_exp = active_exps[0]
            _puid = uuid.uuid4()

            Participant(puid = _puid
                , name = recv_data["pname"]
                , email = recv_data["pemail"]
                , exp = active_exp).save()
            return {"status":"successful", "data":{"euid":active_exp.euid, "puid":_puid}}
        else:
            return {"status":"failed", "data":"no active experiment"}

    except Exception as e:
        logger.info("user_register error: %s" % str(e))
        return {"status":"failed", "data":"system error"}