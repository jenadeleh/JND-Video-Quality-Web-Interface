from videoJnd.models import Instruction, ConsentForm, InterfaceText, Participant, Experiment
from videoJnd.src.ReqVideos import select_videos
from videoJnd.src.Log import logger

def req_inst_cf(_puid:str) -> dict:
    try:
        active_exps = Experiment.objects.filter(active=True)
        interface_text = InterfaceText.objects.all()[0]
        if active_exps:
            exp_obj = active_exps[0]
            avl_videos  = select_videos(exp_obj)

            if avl_videos:
                if _puid:
                    cur_p = Participant.objects.filter(puid=_puid, exp=exp_obj)
                    if cur_p:
                        isPExist = True
                    else:
                        isPExist = False
                else:
                    isPExist = False

                instruction = Instruction.objects.all()[0]
                consent_form = ConsentForm.objects.all()[0]
                
                _response =  {"status":"successful", 
                            "restype": "req_inst_cf", 
                            "data":{"ispexist": isPExist, 
                                    "instruction":instruction.description, 
                                    "consent_form": consent_form.description,
                                    "question": interface_text.question,
                                    "text_end_hit": interface_text.text_end_hit,
                                    "text_end_exp": interface_text.text_end_exp,
                                    "btn_text_end_hit": interface_text.btn_text_end_hit,
                                    "decision_timeout_msg": interface_text.decision_timeout_msg,
                                    "instruction_btn_text": interface_text.instruction_btn_text}}

                return _response
            else:
                return {"status":"failed", "data":interface_text.no_available_exp, "restype": "req_inst_cf"}
        else:
            return {"status":"failed", "data":interface_text.no_available_exp, "restype": "req_inst_cf"}
    except Exception as e:
        logger.info("req_inst_cf error: %s" % str(e))
        return {"status":"failed", "data":"system error", "restype": "req_inst_cf"}