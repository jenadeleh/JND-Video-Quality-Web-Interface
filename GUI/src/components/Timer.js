import * as $ from 'jquery';
import { config } from "./Config"
import { globalStatus } from "./GlobalStatus"
import { addResultToCurVideo, processHit } from "./BtnActions"

export function setTimer() {
    globalStatus.first_duration_timer = setTimeout(()=> { 
        _display_warning_info();
        _second_duration_timer();
    }, config.first_duration);
}

function _second_duration_timer() {
    globalStatus.second_duration_timer = setTimeout(()=> { 
        addResultToCurVideo("no decision"); 
        processHit();
    }, config.second_duration);  
}

function _display_warning_info() {
    $("#timeout-msg").css("display", "inline-block");
    $(".video-cover").css("visibility", "hidden");
    $("#not-sure-btn").attr("disabled", false)
                    .removeClass("btn-secondary")
                    .addClass("btn-primary");
}
