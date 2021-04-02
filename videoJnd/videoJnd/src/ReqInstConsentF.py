from videoJnd.models import Instruction, ConsentForm, InterfaceText, Participant, Experiment

def req_inst_cf(pname:str) -> dict:
    try:
        active_exps = Experiment.objects.filter(active=True)
        if active_exps:
            #TODO: p exist in a the current exp
            cur_p = Participant.objects.filter(name=pname)
            if cur_p:
                isPExist = True
            else:
                isPExist = False

            instruction = Instruction.objects.all()[0]
            consent_form = ConsentForm.objects.all()[0]
            interface_text = InterfaceText.objects.all()[0]

            _response =  {"status":"successful", 
                        "restype": "req_inst_cf", 
                        "data":{"ispexist": isPExist, 
                                "instruction":instruction.description, 
                                "consent_form": consent_form.description,
                                "question": interface_text.question,
                                "text_end_hit": interface_text.text_end_hit,
                                "text_end_exp": interface_text.text_end_exp,
                                "btn_text_end_hit": interface_text.btn_text_end_hit,
                                "timeout_msg": interface_text.timeout_msg}}

            return _response
        else:
            return {"status":"failed", "data":"no active experiment", "restype": "req_inst_cf",}
    except Exception as e:
        print("req_inst_cf error: %s" % str(e))
        return {"status":"failed", "data":"system error", "restype": "req_inst_cf",}