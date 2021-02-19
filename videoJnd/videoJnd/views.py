from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.utils import timezone
from django.core.exceptions import SuspiciousFileOperation
from django.core.exceptions import PermissionDenied
from django.http import Http404


import json
import datetime
import os
import uuid
import threading
import queue

import questplus as qp
import numpy as np

trial_count = 4
threading_list = ["LoopThread"]

# home page
def home(request):
    return render(request,'index.html')

@csrf_exempt
def scheduler(request):
    if request.method == "POST":
        if request.body:
            try:
                recv_data = json.loads(request.body)
                print(recv_data)
                if recv_data["action"] == "decision":
                    decision = recv_data["decision"]

                    print(len(threading.enumerate()))
                    if 'LoopThread' not in threading_list:
                        t = threading.Thread(target=quest_plus_jns, name='LoopThread')
                        t.start()
                        threading_list.append('LoopThread')
                    return JsonResponse({"video_url":"new video url"}, safe=False)

            except Exception as e:
                return JsonResponse({"status":"failed"}, safe=False)

    return HttpResponseRedirect('/')



def quest_plus_jns(trial_count):
    # Stimulus domain.
    intensities = np.arange(start=1, stop=51, step=1)
    stim_domain = dict(intensity=intensities)

    # Parameter domain.
    thresholds = intensities.copy()
    slopes = np.linspace(1.1, 10, 90)
    lower_asymptotes = 0.5#np.linspace(0.01, 0.5, 5)
    lapse_rate = 0.01

    param_domain = dict(threshold=thresholds,
                        slope=slopes,
                        lower_asymptote=lower_asymptotes,
                        lapse_rate=lapse_rate)

    # Outcome (response) domain.
    responses = ['Yes', 'No']
    outcome_domain = dict(response=responses)
    # Further parameters.
    func = 'weibull'
    stim_scale = 'log10'#'linear' #'dB'
    stim_selection_method = 'min_entropy'
    param_estimation_method = 'mean'

    # Initialize the QUEST+ staircase.
    q = qp.QuestPlus(stim_domain=stim_domain,
                    func=func,
                    stim_scale=stim_scale,
                    param_domain=param_domain,
                    outcome_domain=outcome_domain,
                    stim_selection_method=stim_selection_method,
                    param_estimation_method=param_estimation_method)

    q.answer_history = list()



    for current_trial_number in range(trial_count):
        next_stim = q.next_stim
        #print(f'Please present stimulus {next_stim}.')% assume the right side is flickeing 
        """ 
        type 1  if you seee noticieable flickering on the left half,
        type 2 if you see flickering in the right side, 
        type 3 for the case of "not sure" for  stimulus
        type 4 for "no decistion" 
        """
        print(next_stim)
        outcome = input(f'Please input your decision:')

        # Retrieve response
        q.answer_history.append(dict(answer=outcome))

        if outcome=='1':
            outcome = dict(response='No')  
            q.update(stim=next_stim, outcome=outcome)
            q.update(stim=next_stim, outcome=outcome)

        elif outcome=='2':
            outcome = dict(response='Yes')
            q.update(stim=next_stim, outcome=outcome)

        elif outcome=='3':
            outcome = dict(response='Yes')
            q.update(stim=next_stim, outcome=outcome)
            outcome = dict(response='No')
            q.update(stim=next_stim, outcome=outcome)

        elif outcome=='4':
            None