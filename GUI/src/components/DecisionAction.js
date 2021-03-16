import * as $ from 'jquery';
import { SendMsg } from "./Connection"
import { globalStatus} from "./GlobalStatus"
import { updateProgressBar } from "./Progress"

export function DecisionAction(decision) {

    // clear timer
    clearTimeout(globalStatus.first_duration_timer);
    clearTimeout(globalStatus.second_duration_timer);

    // update control panel
    $("#warning-cover").css("display", "none");
    $("#video").css("display", "inline-block");
    $(".decision-btn").attr("disabled", true);

    // update progress bar
    globalStatus.task_finished_num += 1;
    updateProgressBar(globalStatus.task_finished_num, globalStatus.task_num);

    // store result
    // TODO: store result

    // check experiment is finished or not
    if (globalStatus.task_finished_num < globalStatus.task_num) {
        // TODO: display next video
        // TODO: enable control panel
        // let url="https://datasets.vqa.mmsp-kn.de/JND_datasets/Video_JND_dataset/JND_264_640x480/SRC089_640x480_30/crf_10/videoSRC089_640x480_30_qp_00_50_L_crf_10.mp4"
        // // console.log($("#video_src").attr("src"))
        // $("#video_src").attr("src", url)
        // $(".decision-btn").attr("disabled", false);
        // timeStampRecord.start_time = new Date().getTime();
        // timer();
    } else if (globalStatus.task_finished_num == globalStatus.task_num) {
        _end_exp();
    }
}

export function _end_exp() {
    $(".decision-btn").attr("disabled", true);
    $("#video").css("display", "none");
    $("#warning-cover").css("display", "inline-block")
                    .html("Thank you for your participation!");
}