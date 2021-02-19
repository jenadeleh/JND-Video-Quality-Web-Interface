import * as $ from 'jquery';
import { SendMsg } from "./Connection"
import { timeStampRecord, timeoutRecord, taskRecord } from "./GlobalStatus"
import { updateProgressBar } from "./Progress"

export function DecisionAction(numeric_decision) {

    // clear timer
    clearTimeout(timeoutRecord.Sec5);
    clearTimeout(timeoutRecord.Sec3);

    // update layout
    $("#warning-cover").css("display", "none");
    $("#video").css("display", "inline-block");
    $(".decision-btn").attr("disabled", true);

    // update progress bar
    taskRecord.finish_num += 1;
    updateProgressBar(taskRecord.finish_num, taskRecord.TASK_NUM);

    // send result to backend
    timeStampRecord.end_time = new Date().getTime();

    // TODO: token
    let data = {
        "action":"decision"
        , "start_time": timeStampRecord.start_time
        , "end_time": timeStampRecord.end_time
        , "decision":numeric_decision
    };

    SendMsg(data);
}

export function endExpAction() {
    $(".decision-btn").attr("disabled", true);
    $("#video").css("display", "none");
    $("#warning-cover").css("display", "inline-block")
                    .html("Thank you for your participantion!");
}