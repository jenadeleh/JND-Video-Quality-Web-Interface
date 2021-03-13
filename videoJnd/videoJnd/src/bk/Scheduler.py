import json
from videoJnd.src.QpObjsRecord import QpObjsRecord
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse

# ----- init -----
qp_objs = QpObjsRecord()
print("\n-- Initialization Done --\n")

def main(request):
    if request.method == "POST":
        if request.body:
            try:
                recv_data = json.loads(request.body)
                print(recv_data)
                if recv_data["action"] == "init":
                    # TODO: uuid
                    # TODO: update database
                    response = qp_objs.get_gp_next_stim()

                elif recv_data["action"] == "decision":
                    decision = recv_data["decision"]
                    start_time = recv_data["start_time"]
                    end_time = recv_data["end_time"]

                    # TODO: update database
                    qp_objs.update_gp_qp_params(decision)
                    response = qp_objs.get_gp_next_stim()

                return JsonResponse(response, safe=False)
                
            except Exception as e:
                print("Error! " + e)
                return JsonResponse({"status":"failed"}, safe=False)

    return HttpResponseRedirect('/')