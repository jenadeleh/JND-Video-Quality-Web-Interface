from videoJnd.models import Instruction

def get_instruction(recv_data:dict) -> dict:
    instruction = Instruction.objects.all()[0]

    
    _response =  {"status":"successful", 
                "restype": "get_instruction", 
                "data":{"instruction":instruction.description}}

    return _response