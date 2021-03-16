import * as $ from 'jquery';
import { DecisionAction } from "./DecisionAction"
import { config } from "./Config"
import { globalStatus } from "./GlobalStatus"

export function setTimer() {
    globalStatus.first_duration_timer = setTimeout(()=> { 
        _display_warning_info();
        _second_duration_timer();
    }, config.first_duration);
}

function _second_duration_timer() {
    globalStatus.second_duration_timer = setTimeout(()=> { 
        //TODO:
        // DecisionAction(NUMERIC_DECISION["nodecision"]); 
    }, config.second_duration);  
}

function _display_warning_info() {
    $("#video").css("display", "none");
    $("#warning-cover").css("display", "inline-block");
}
