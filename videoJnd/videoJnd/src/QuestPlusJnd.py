import questplus as qp
import numpy as np
import copy

class QuestPlusJnd():
    def __init__(self) -> None:
        self.QpParam266 = self._qp_obj("266")
        self.QpParam264 = self._qp_obj("264")

    def _qp_obj(self, codec:str):
        # Stimulus domain.
        intensities = np.arange(start=1, stop=self._intensities_max(codec), step=1)
        stim_domain = {"intensity":intensities}

        # Parameter domain.
        param_domain = {"threshold": intensities
                        , "slope": np.linspace(1.1, 5, 40)
                        , "lower_asymptote": 0.5 #np.linspace(0.01, 0.5, 5)
                        , "lapse_rate":0.01}

        # Outcome (response) domain.
        outcome_domain = {"response": ['Yes', 'No']}

        # Initialize the QUEST+ staircase.
        param = qp.QuestPlus(stim_domain = stim_domain,
                    func = 'weibull',
                    stim_scale = 'log10', #'linear' #'dB'
                    param_domain = param_domain,
                    outcome_domain = outcome_domain,
                    stim_selection_method = 'min_entropy',
                    param_estimation_method = 'mean')

        return param

    def _intensities_max(self, codec:str) -> int:
        return {"264":51, "266":63}[codec]

    def gen_qp_param(self, codec:str):
        qp_param_dict = {"264":self.QpParam264, "266":self.QpParam266}
        return copy.deepcopy(qp_param_dict[codec])

    def update_params(self, qp_param: object, decisions:list) -> str:
        for d in decisions:
            next_stim = qp_param.next_stim

            if d == '1': # left side
                qp_param.update(stim = next_stim, outcome = {"response":"No"})
                qp_param.update(stim = next_stim, outcome = {"response":"No"})

            elif d == '2': # right side
                qp_param.update(stim = next_stim, outcome = {"response":"Yes"})
                qp_param.update(stim = next_stim, outcome = {"response":"Yes"})

            elif d == '3': # not sure
                qp_param.update(stim = next_stim, outcome = {"response":"Yes"})
                qp_param.update(stim = next_stim, outcome = {"response":"No"})

            elif d == '4': # no decision
                pass
            
            # print(d, qp_param.next_stim)

        return qp_param.next_stim["intensity"]


if __name__ == "__main__":
    import time
    from random import randint
    import copy

    decisions = [str(randint(1,3)) for _ in range(30)]
    # decisions = ['1', '3', '2']

    qp_obj = QuestPlusJnd()

    codec = "264"

    t1 = time.process_time()
    for _ in range(10):
        next_stim = qp_obj.update_params(qp_obj.gen_qp_param(codec), decisions)
    # print(next_stim)
    t2 = time.process_time()
    print((t2-t1)*1000)
