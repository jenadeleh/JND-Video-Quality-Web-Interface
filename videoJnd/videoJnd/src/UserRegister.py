from django.utils import timezone

from videoJnd.models import Participant, Experiment
import uuid

def user_register(recv_data:dict) -> dict:
    cur_exp_obj = Experiment.objects.all()[0]
    _puid = uuid.uuid4()

    Participant(puid = _puid
        , name = recv_data["pname"]
        , email = recv_data["pemail"]
        , exp = cur_exp_obj).save()

    return {"status":"successful", "restype": "user_register", "data":{"puid":_puid, "exp":cur_exp_obj.name}}
