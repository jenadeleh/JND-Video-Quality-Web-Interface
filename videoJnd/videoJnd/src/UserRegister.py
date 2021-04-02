from django.utils import timezone

from videoJnd.models import Participant, Experiment
import uuid

def user_register(recv_data:dict) -> dict:
    try:
        cur_exp_obj = Experiment.objects.all()[0]
        _puid = uuid.uuid4()

        Participant(puid = _puid
            , name = recv_data["pname"]
            , email = recv_data["pemail"]
            , exp = cur_exp_obj).save()
        return {"status":"successful", "data":{"exp":cur_exp_obj.name, "puid":_puid}}
    except Exception as e:
        print("user_register error: %s" % str(e))
        return {"status":"failed", "data":"system error"}
        


    
