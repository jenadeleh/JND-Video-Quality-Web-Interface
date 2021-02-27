from typing import Tuple
import uuid
import random
from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.src.GetConfig import get_config


# from QuestPlusJnd import QuestPlusJnd
# from GetConfig import get_config


class QpObjsRecord():
    def __init__(self) -> None:
        self.calc_upper_num, self.group_num, self.src_video_num = get_config()
        self.qp_objs = {}
        self.gp_isAvailable = [True for _ in range(self.group_num)]
        self.gp_info = {}

        self._initialze()

    def _initialze(self)-> None:
        """
        Each qp_obj represents one source video of one group.
        Totally, group_num*src_video_num qp_obj will be created

        qp_objs = {"g-s":obj}, g:group, s:source video
        """
        for g in range(self.group_num):
            srcs = [str(i) for i in range(self.src_video_num)]
            random.shuffle(srcs)
            self.gp_info[str(g)] = {"avbl_count":self.calc_upper_num, "src":srcs}

            for s in range(self.src_video_num):
                self.qp_objs["%d-%d" % (g, s)] = QuestPlusJnd(self.calc_upper_num, g, s)
        
        return None

    def _select_avbl_group(self) -> str:
        if True in self.gp_isAvailable:
            g = self.gp_isAvailable.index(True)
            self.gp_isAvailable[g] = False
            return str(g)
        
        else:
            # TODO: end exp
            return None

    def _select_src_video(self, g:str) -> list:
        return self.gp_info[g]["src"]

    def _get_qp_obj(self, g:str, s:str) -> object:
        return self.qp_objs["%s-%s" % (g, s)]

    def _update_qp_params(self, g:str, s:str, decision:str) -> int:
        qp_obj = self._get_qp_obj(g, s)
        qp_obj.update_params(decision)

    def _process_decision(self, gp_decision:str) -> list:
        """
        gp_decision = "0-0-1_0-1-2" -> [("0", "0", "1"), ("0", "1", "2"), ...]
        """
        gp_decision = [d.split("-") for d in gp_decision.split("_")]

        return gp_decision

    def _update_gp_info(self, g) -> None:
        # shuffle src list
        srcs = [str(i) for i in range(self.src_video_num)]
        random.shuffle(srcs)
        self.gp_info[str(g)]["src"] = srcs 

        # reduce available count for this group
        self.gp_info[str(g)]["avbl_count"] = self.gp_info[str(g)]["avbl_count"] - 1

        # set group is available the avbl_count != 0
        if self.gp_info[str(g)]["avbl_count"] >0:
            self.gp_isAvailable[int(g)] = True

    def get_gp_next_stim(self) -> list:
        g = self._select_avbl_group()
        if g:
            srcs = self._select_src_video(g)
            output = []
            for s in srcs:
                qp_obj = self._get_qp_obj(g, s)
                next_stim = str(qp_obj.next_stim["intensity"])
                output.append((g,s,next_stim))
            
            return output
        else:
            return "no experiment is available"

    def update_gp_qp_params(self, gp_decision:list) -> None:
        gp_decision = self._process_decision(gp_decision)
        for gd in gp_decision:
            self._update_qp_params(gd[0], gd[1], gd[2])

        self._update_gp_info(gp_decision[0][0])
    

if __name__ == "__main__":
    qpr = QpObjsRecord()
    print("-- init video --")
    print(qpr.get_gp_next_stim())

    print("-- 1st update --")
    gp_decision = [("0-0", "1"), ("0-1", "1"), ("0-2", "2")]
    qpr.update_gp_qp_params(gp_decision)
    print(qpr.get_gp_next_stim())

    print("-- 2nd update --")
    gp_decision = [("0-0", "2"), ("0-1", "1"), ("0-2", "1")]
    qpr.update_gp_qp_params(gp_decision)
    print(qpr.get_gp_next_stim())

    print("-- 3rd update --")
    gp_decision = [("0-0", "1"), ("0-1", "2"), ("0-2", "1")]
    qpr.update_gp_qp_params(gp_decision)
    print(qpr.get_gp_next_stim())

    print("-- 4th update --")
    gp_decision = [("0-0", "3"), ("0-1", "1"), ("0-2", "1")]
    qpr.update_gp_qp_params(gp_decision)
    print(qpr.get_gp_next_stim())

    print("-- 5th update --")
    gp_decision = [("1-0", "3"), ("1-1", "1"), ("1-2", "1")]
    qpr.update_gp_qp_params(gp_decision)
    print(qpr.get_gp_next_stim())

