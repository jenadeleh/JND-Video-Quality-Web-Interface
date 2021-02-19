import * as $ from 'jquery';
import { timeStampRecord, taskRecord } from "./GlobalStatus"
import { TimeCounter } from "./Timer"
import { endExpAction } from "./DecisionAction"

export function UpdateVideo(url) {
    if (taskRecord.finish_num == taskRecord.TASK_NUM) {
        endExpAction();
    } else {
        // TODO: after loading video
        let url="https://datasets.vqa.mmsp-kn.de/JND_datasets/Video_JND_dataset/JND_264_640x480/SRC089_640x480_30/crf_10/videoSRC089_640x480_30_qp_00_50_L_crf_10.mp4"
        // console.log($("#video_src").attr("src"))
        $("#video_src").attr("src", url)
        $(".decision-btn").attr("disabled", false);
        timeStampRecord.start_time = new Date().getTime();
        TimeCounter();
    }
}