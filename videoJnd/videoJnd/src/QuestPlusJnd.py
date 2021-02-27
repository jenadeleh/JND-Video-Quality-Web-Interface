import questplus as qp
import numpy as np

class QuestPlusJnd():
    def __init__(self
                , calc_upper_num:int
                , group:int
                , src_video:int) -> None:

        self.param = self._construct_parameters_obj()
        self.next_stim = self.param.next_stim
        self.isActive = True
        self.calc_upper_num = calc_upper_num
        self.count = 0
        self.gp_src_id = "%d-%d" % (group, src_video)

    def _construct_parameters_obj(self):
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
        param = qp.QuestPlus(stim_domain = stim_domain,
                    func = func,
                    stim_scale = stim_scale,
                    param_domain = param_domain,
                    outcome_domain = outcome_domain,
                    stim_selection_method = stim_selection_method,
                    param_estimation_method = param_estimation_method)
        
        param.answer_history = []

        return param

    def update_params(self, decision:str) -> None:
        """ 
        decision = 1, left side
        decision = 2, right side
        decision = 3, not sure
        decision = 4, no decistion
        """

        if self.isActive == True:
            

            self.param.answer_history.append(dict(answer=decision))

            if decision == '1':
                outcome = dict(response='No')
                self.param.update(stim = self.next_stim, outcome = outcome)
                self.param.update(stim = self.next_stim, outcome = outcome)

            elif decision == '2':
                outcome = dict(response='Yes')
                self.param.update(stim = self.next_stim, outcome = outcome)

            elif decision == '3':
                outcome = dict(response = 'Yes')
                self.param.update(stim = self.next_stim, outcome = outcome)
                outcome = dict(response='No')
                self.param.update(stim = self.next_stim, outcome = outcome)

            elif decision == '4':
                None

            self.next_stim = self.param.next_stim
            
            self.count += 1
            if self.count > self.calc_upper_num:
                self.isActive = False

        return None     


if __name__ == "__main__":
    qp_obj = QuestPlusJnd(3,2,2)

    print(qp_obj.next_stim)
    qp_obj.update_params("2")
    print(qp_obj.next_stim)
    qp_obj.update_params("2")
    print(qp_obj.next_stim)
    qp_obj.update_params("2")
    print(qp_obj.next_stim)
    qp_obj.update_params("1")
    print(qp_obj.next_stim)
    qp_obj.update_params("2")
    print(qp_obj.next_stim)
    qp_obj.update_params("1")
    print(qp_obj.next_stim)