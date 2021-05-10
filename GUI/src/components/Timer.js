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
    $("#timeout-msg").css("display", "inline-block");
    $(".video-cover").css("visibility", "hidden");
    $("#not-sure-btn").attr("disabled", false)
                    .removeClass("btn-secondary")
                    .addClass("btn-primary");
}

export function setExpireTimer() {
    
    let time_now = new Date().getTime();
    let time_diff = (time_now - globalStatus.start_time) / 1000; // sec

    console.log(time_diff, globalStatus.duration)
    if (time_diff >= globalStatus.duration) {
        _showTimeoutMsg();
    } else {

        let wait_time = (globalStatus.duration - time_diff)*1000; // ms
        globalStatus.EXPIRE_TIMER = setTimeout(()=> {
            _showTimeoutMsg();
        }, wait_time);
    }
}

function _showTimeoutMsg() {
    clearInterval(globalStatus.env_bg_interval);
    clearTimeout(globalStatus.FIRST_DURATION_TIMER);
    clearTimeout(globalStatus.SECOND_DURATION_TIMER);
    $("#warning-cover").css("display", "inline").css("visibility", "visible");
    $("#warning-msg").html(globalStatus.expire_msg);
}
