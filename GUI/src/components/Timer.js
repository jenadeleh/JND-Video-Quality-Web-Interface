import * as $ from 'jquery';
import { config } from "./Configuration"
import { globalStatus } from "./GlobalStatus"
import { addResultToCurVideo, processHit } from "./BtnActions"

export function setTimer() {
    globalStatus.FIRST_DURATION_TIMER = setTimeout(()=> { 
        _display_warning_info();
        _SECOND_DURATION_timer();
    }, config.FIRST_DURATION);
}

function _SECOND_DURATION_timer() {
    globalStatus.SECOND_DURATION_TIMER = setTimeout(()=> { 
        addResultToCurVideo("no decision");
        processHit();
    }, config.SECOND_DURATION);  
}

function _display_warning_info() {
    $("#decision-timeout-msg").css("display", "inline-block");
    $(".video-cover").css("visibility", "hidden");
    $("#not-sure-btn").removeClass("btn-secondary").addClass("btn-primary");
    globalStatus.isNotSureBtnAvl = true;
    if (globalStatus.isWarning == false) {
        $("#not-sure-btn").attr("disabled", false);
    }
}

