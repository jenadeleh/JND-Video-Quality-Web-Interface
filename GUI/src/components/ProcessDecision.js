import * as $ from 'jquery';
import { SendMsg } from "./Connection"
import { globalStatus} from "./GlobalStatus"
import { updateProgressBar } from "./ProgressBar"
import { displayVideo } from "./LoadVideos"

export function processDecision(decision) {

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

    } else if (globalStatus.task_finished_num == globalStatus.task_num) {
        _end_exp();
    }
}

function _end_exp() {
    $(".decision-btn").attr("disabled", true);
    $("#video").css("display", "none");
    $("#warning-cover").css("display", "inline-block")
                    .html("Thank you for your participation!");
}
