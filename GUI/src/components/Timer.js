import * as $ from 'jquery';
import { DecisionAction } from "./DecisionAction"
import { NUMERIC_DECISION } from "./Config"
import { timeoutRecord } from "./GlobalStatus"

const firstTimer = 5000;
const secondTimer = 3000;

export function TimeCounter() {
    timeoutRecord.Sec5 = setTimeout(()=> { 
        DisplayWarningInfo();
        Timer3Sec();
    }, firstTimer);
}

function Timer3Sec() {
    timeoutRecord.Sec3 = setTimeout(()=> { 
        DecisionAction(NUMERIC_DECISION["nodecision"]);
    }, secondTimer);  
}

function DisplayWarningInfo() {
    $("#video").css("display", "none");
    $("#warning-cover").css("display", "inline-block");
}
