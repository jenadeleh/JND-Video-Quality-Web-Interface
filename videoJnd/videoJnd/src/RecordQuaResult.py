from django.utils import timezone
from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.models import EncodedRefVideoObj, Experiment, QuaAssignment
from videoJnd.src.GetConfig import get_config
from videoJnd.src.ResourceMonitor import add_idle_thread
import uuid


config = get_config()

def record_qua_result(recv_data:dict) -> dict:
	try:
		_result = recv_data["data"]["result"]
		cali_info = recv_data["data"]["cali_info"]
		os_info = recv_data["data"]["os_info"]
		exp_obj = Experiment.objects.filter(euid=recv_data["euid"])[0]

		auid = uuid.uuid4()
		QuaAssignment(
			auid = auid
			, exp = exp_obj
			, workerid = recv_data["workerid"]
			, result = {"result": _result}
			, calibration = cali_info
			, operation_system = os_info
		).save()

		exp_obj.qua_hit_count = exp_obj.qua_hit_count + 1
		exp_obj.save()

		return {"status":"successful", "restype": "record_result", "code":auid}
	
	except Exception as e:
		return {"status":"failed", "restype": "record_result", "error":"record_result error"}


def _encode_decision(side_of_reference:str, decision:str) -> str:
    if decision == "R" or decision == "L":
        if decision == side_of_reference:
            return "1"
        elif decision != side_of_reference:
            return "2"
    elif decision == "not sure":
        return "3"
    elif decision == "no decision":
        return "4"
