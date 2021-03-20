from videoJnd.models import Instruction, ConsentForm

def req_inst_cf() -> dict:
    instruction = Instruction.objects.all()[0]
    consent_form = ConsentForm.objects.all()[0]

    _response =  {"status":"successful", 
                "restype": "req_inst_cf", 
                "data":{"instruction":instruction.description, "consent_form": consent_form.description}}

    return _response