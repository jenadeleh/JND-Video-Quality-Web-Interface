from videoJnd.models import Instruction, ConsentForm, InterfaceText

def req_inst_cf() -> dict:
    instruction = Instruction.objects.all()[0]
    consent_form = ConsentForm.objects.all()[0]
    interface_text = InterfaceText.objects.all()[0]

    _response =  {"status":"successful", 
                "restype": "req_inst_cf", 
                "data":{"instruction":instruction.description, 
                        "consent_form": consent_form.description,
                        "question": interface_text.question,
                        "text_end_exp": interface_text.text_end_exp,
                        "btn_text_end_exp": interface_text.btn_text_end_exp,
                        "warning_msg": interface_text.warning_msg}}

    return _response