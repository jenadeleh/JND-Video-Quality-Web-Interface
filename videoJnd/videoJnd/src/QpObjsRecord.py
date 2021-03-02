from typing import Tuple
import uuid
import random
from videoJnd.src.QuestPlusJnd import QuestPlusJnd
from videoJnd.src.GetConfig import get_config
from videoJnd.src.GenUrl import gen_src_urls
import sys

# from QuestPlusJnd import QuestPlusJnd
# from GetConfig import get_config

class QpObjsRecord():
    def __init__(self) -> None:
        config = get_config()
        self.src_urls = gen_src_urls() # qpV should be replaced for the final url
        self.src_video_num = len(self.src_urls)
        self.calc_upper_num = config["CALC_UPPER_NUM"]
        self.video_per_group = config["VIDEO_PER_GROUP"]
        self.rating_times_per_src = config["RATING_TIMES_PER_SRC"]

        self._check_config()

        self.batch = int(self.src_video_num/self.video_per_group)
        self.group_num = self.rating_times_per_src * self.batch
        self.gp_isAvailable = [True for _ in range(self.group_num)]
        self.qp_objs, self.gp_info = self._create_qp_objs()

        print("++ %d source videos +++" % self.src_video_num)
        print("++ %d rating times per source video +++" % self.rating_times_per_src)
        print("++ %d groups +++" % self.group_num)
        print("++ %d qp_objs +++" % len(self.qp_objs))

    def _check_config(self) -> None:
        if self.src_video_num % self.video_per_group !=0 :
            sys.exit("Error! source video number should be divisible by VIDEO_PER_GROUP")

        return None

    def _create_qp_objs(self)-> tuple:
        """
        Each qp_obj represents one source video of one group.
        Totally, group_num*video_per_group qp_obj will be created
        group_num = rating_times_per_src * (src_video_num/video_per_group)
        qp_objs number = group_num *video_per_group

        qp_objs = {"g-s":obj}, g:group, s:source video
        gp_info = {"g":{"avbl_count":int, "src":[], "src_map":[]}}
            avbl_count: trail num
            src: the index within the group, shuffled, different workers will get different orders of the video sequence
            src_map: the mapping between the 'src' and the source video name
        """
        qp_objs = {}
        gp_info = {}
        
        for g in range(self.group_num):
            srcs = [str(i) for i in range(self.video_per_group)]
            random.shuffle(srcs)
            gp_info[str(g)] = {"avbl_count":self.calc_upper_num, "src":srcs, "src_map":self._gp_src_url_mapping(str(g))}

            for s in range(self.video_per_group):
                qp_objs["%d-%d" % (g, s)] = QuestPlusJnd(self.calc_upper_num, g, s)
        
        return (qp_objs, gp_info)

    def _gp_src_url_mapping(self, g:str) -> list:
        """
        Goal: map the group src_map to the src_urls([]) index
        """
        batch_idx = int(g) % self.batch
        _range = [batch_idx*self.video_per_group, (batch_idx+1)*self.video_per_group]
        output = [i for i in range(_range[0], _range[1])]

        return output
    
    def _select_src_url(self, g:str, s:str) -> str:
        gp_src_idx = self.gp_info[str(g)]["src"][int(s)]
        src_map_idx = self.gp_info[str(g)]["src_map"][int(gp_src_idx)]
        url = self.src_urls[src_map_idx]

        return url

    def _select_avbl_group(self) -> str:
        if True in self.gp_isAvailable:
            g = self.gp_isAvailable.index(True)
            self.gp_isAvailable[g] = False
            return str(g)
        
        else: # end exp
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

    def _update_gp_info(self, g:str) -> None:
        # shuffle src list
        srcs = [str(i) for i in range(self.video_per_group)]
        random.shuffle(srcs)
        self.gp_info[str(g)]["src"] = srcs 

        # reduce available count for this group
        self.gp_info[str(g)]["avbl_count"] = self.gp_info[str(g)]["avbl_count"] - 1

        # set group is available the avbl_count != 0
        if self.gp_info[str(g)]["avbl_count"] >0:
            self.gp_isAvailable[int(g)] = True

        return None

    def get_gp_next_stim(self) -> list:
        g = self._select_avbl_group()
        if g:
            srcs = self._select_src_video(g)
            output = []
            for s in srcs:
                qp_obj = self._get_qp_obj(g, s)
                next_stim = str(qp_obj.next_stim["intensity"])
                url = self._select_src_url(str(g), str(s)).replace("qpV", next_stim)
                output.append((g, s, url, next_stim))

            return output
        else:
            # TODO: end exp
            return "no experiment is available"

    def update_gp_qp_params(self, gp_decision:list) -> None:
        gp_decision = self._process_decision(gp_decision)
        for gd in gp_decision:
            self._update_qp_params(gd[0], gd[1], gd[2])

        self._update_gp_info(gp_decision[0][0])

        return None
    

if __name__ == "__main__":
    qpr = QpObjsRecord()
    # print(qpr._gp_src_url_mapping(2))


    # print("-- init video --")
    # print(qpr.get_gp_next_stim())

    # print("-- 1st update --")
    # gp_decision = [("0-0", "1"), ("0-1", "1"), ("0-2", "2")]
    # qpr.update_gp_qp_params(gp_decision)
    # print(qpr.get_gp_next_stim())

    # print("-- 2nd update --")
    # gp_decision = [("0-0", "2"), ("0-1", "1"), ("0-2", "1")]
    # qpr.update_gp_qp_params(gp_decision)
    # print(qpr.get_gp_next_stim())

    # print("-- 3rd update --")
    # gp_decision = [("0-0", "1"), ("0-1", "2"), ("0-2", "1")]
    # qpr.update_gp_qp_params(gp_decision)
    # print(qpr.get_gp_next_stim())

    # print("-- 4th update --")
    # gp_decision = [("0-0", "3"), ("0-1", "1"), ("0-2", "1")]
    # qpr.update_gp_qp_params(gp_decision)
    # print(qpr.get_gp_next_stim())

    # print("-- 5th update --")
    # gp_decision = [("1-0", "3"), ("1-1", "1"), ("1-2", "1")]
    # qpr.update_gp_qp_params(gp_decision)
    # print(qpr.get_gp_next_stim())

