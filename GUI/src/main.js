import * as $ from 'jquery';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-slider';
import 'bootstrap-slider/dist/css/bootstrap-slider.min.css';

import { updateProgressBar } from "./components/Progress"
import { TimeCounter } from "./components/Timer"
import { DecisionAction } from "./components/DecisionAction"
import { NUMERIC_DECISION } from "./components/Config"
import { timeStampRecord, taskRecord } from "./components/GlobalStatus"

// $("#instruction-modal").modal("show");
updateProgressBar(taskRecord.finish_num, taskRecord.TASK_NUM);

$('#start-exp-btn').on('click', ()=> {
    $("#start-exp-btn").attr("disabled", true)
                        .css("display", "none");

    $(".decision-btn").attr("disabled", false);

    $("#video").get(0).play();

    timeStampRecord.start_time = new Date().getTime();
    TimeCounter();  
});

$('.decision-btn').on('click',(e)=> {
    let decision = $(e.target).attr("data-decision");
    let numeric_decision = NUMERIC_DECISION[decision];
    DecisionAction(numeric_decision);
});
