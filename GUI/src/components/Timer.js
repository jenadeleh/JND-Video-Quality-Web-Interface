import * as $ from 'jquery';
import { config } from "./Config"
import { globalStatus } from "./GlobalStatus"
import { addResultToCurVideo, processExp } from "./BtnActions"

export function setTimer() {
    globalStatus.first_duration_timer = setTimeout(()=> { 
        _display_warning_info();
        _second_duration_timer();
    }, config.first_duration);
}

function _second_duration_timer() {
    globalStatus.second_duration_timer = setTimeout(()=> { 
        addResultToCurVideo("no decision"); 
        console.log("no decision");
        $("#not-sure-btn").attr("disabled", true)
                        .removeClass("btn-primary")
                        .addClass("btn-secondary");
        processExp();

    }, config.second_duration);  
}

function _display_warning_info() {
    // $("#message-panel").css("display", "inline-block");
    $("#not-sure-btn").attr("disabled", false)
                    .removeClass("btn-secondary")
                    .addClass("btn-primary");
}
