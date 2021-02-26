import uuid
from . import QuestPlusJnd

class QpObjsRecord():
    def __init__(self
                ,calc_upper_num
                , group_num
                , src_video_num) -> None:
        
        self.calc_upper_num = calc_upper_num
        self.group_num = group_num
        self.src_video_num = src_video_num

        self.gp_src_uuid = {}
        self.qp_objs = {}
        self.gp_isAvailable = [True for _ in range(self.group_num)]

    def create(self):
        """
        Each calculator represents one source video of one group.
        Totally, group_num*src_video_num calculators will be created

        Output:
        gp_src_uuid = {"0-0":obj_uuid}, obj uuid of a specific group and source video
        qp_objs = {"uuid":obj}
        """
        # TODO:
        for g in range(self.group_num):
            for s in range(self.src_video_num):
                uu_id = uuid.uuid4().hex
                qp_calc = QuestPlusJnd(self.calc_upper_num, uu_id, g, s)
                self.qp_objs[uu_id] = qp_calc
                self.gp_src_uuid["%d-%d"%(g,s)] = uu_id

    def select(self):
        # TODO:
        gp_idx = self.gp_isAvailable.index(True)
        self.gp_isAvailable[gp_idx] = False
        pass

    def next_video_url(self):
        # TODO:
        pass

if __name__ == "__main__":
    pass