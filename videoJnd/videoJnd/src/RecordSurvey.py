from django.utils import timezone
from videoJnd.models import Survey, Experiment
import uuid

def record_survey(recv_data:dict) -> dict:
    exp_obj = Experiment.objects.filter(euid=recv_data["euid"])[0]

    Survey(
        suid = uuid.uuid4()
        , exp = exp_obj
        , workerid = recv_data["workerid"]
        , result = {"result": recv_data["result"]}
    ).save()