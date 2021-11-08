from django.utils import timezone

from videoJnd.models import StudyParticipant, Experiment
from videoJnd.src.Log import logger
import uuid

def user_register(recv_data:dict) -> dict:
    try:
        active_exps = Experiment.objects.filter(active=True)
        if active_exps:
            active_exp = active_exps[0]
            p_obj = StudyParticipant.objects.filter(workerid=recv_data["workerid"])

            if p_obj:
              puid = p_obj[0].puid

            else:
              puid = uuid.uuid4()
              StudyParticipant(
                  puid = puid
                  , workerid = recv_data["workerid"]
                  , exp = active_exp
              ).save()
            
            return {"status":"successful", "data":{"euid":active_exp.euid, "puid":puid}}
        else:
            return {"status":"failed", "data":"no active experiment"}

    except Exception as e:
        logger.info("user_register error: %s" % str(e))
        return {"status":"failed", "data":"system error"}