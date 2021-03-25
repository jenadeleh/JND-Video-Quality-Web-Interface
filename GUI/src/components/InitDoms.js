import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus"

export function initDoms() {
    // experiment session
    $('#start-exp-btn').on('click', ()=> {
        $("#start-exp-btn").attr("disabled", true)
                            .css("display", "none");
    
        $("#left-btn, #right-btn").attr("disabled", false);
        
        // play video
        let vuid = globalStatus.cur_video["vuid"];
        $(`#${vuid}`).get(0).play();



        // $("#ee164506-a515-436c-b88d-af272d7bd291").addClass("curr-display");
        // timeStampRecord.start_time = new Date().getTime();
        // TimeCounter();  
    });
    
    $('.decision-btn').on('click',(e)=> {
        let decision = $(e.target).attr("data-decision");
        let numeric_decision = NUMERIC_DECISION[decision];
        DecisionAction(numeric_decision);
    });
    
    return
}

