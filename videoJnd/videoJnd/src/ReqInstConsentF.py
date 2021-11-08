from videoJnd.models import Instruction, ConsentForm, InterfaceText, StudyParticipant, Experiment
from videoJnd.src.ReqVideos import select_encoded_ref_videos
from videoJnd.src.Log import logger

def req_inst_cf(puid:str) -> dict:
    try:
        active_exps = Experiment.objects.filter(active=True)
        interface_text = InterfaceText.objects.all()[0]

        if len(active_exps)>0:
            exp_obj = active_exps[0]
            
            if puid:
                avl_encoded_ref_videos_objs  = select_encoded_ref_videos(exp_obj, puid)
            else: 
                avl_encoded_ref_videos_objs  = select_encoded_ref_videos(exp_obj, "")

            if len(avl_encoded_ref_videos_objs)>0:
                isPExist = False
                if puid:
                    cur_p = StudyParticipant.objects.filter(puid=puid, exp=exp_obj)
                    if cur_p:
                        isPExist = True

                instruction = Instruction.objects.all()[0]
                consent_form = ConsentForm.objects.all()[0]
                
                response_data =  {
                    "status":"successful", 
                    "restype": "req_inst_cf", 
                    "data":{
                        "ispexist": isPExist, 
                        "instruction":instruction.description, 
                        "consent_form": consent_form.description,
                        "question": interface_text.question,
                        "text_end_hit": interface_text.text_end_hit,
                        "text_end_exp": interface_text.text_end_exp,
                        "btn_text_end_hit": interface_text.btn_text_end_hit,
                        "decision_timeout_msg": interface_text.decision_timeout_msg,
                        "instruction_btn_text": interface_text.instruction_btn_text,
                        "consent_btn_text": interface_text.consent_btn_text,
                        "training_description": interface_text.training_description,
                        "quiz_description": interface_text.quiz_description,
                        "flickering_test_description": interface_text.flickering_test_description,
                        "quality_test_description": interface_text.quality_test_description,
                    }
                }

                return response_data
            else:
                return {"status":"failed", "data":interface_text.no_available_exp, "restype": "req_inst_cf"}
        else:
            return {"status":"failed", "data":interface_text.no_available_exp, "restype": "req_inst_cf"}

    except Exception as e:
        logger.info("req_inst_cf error: %s" % str(e))
        return {"status":"failed", "data":"system error", "restype": "req_inst_cf"}