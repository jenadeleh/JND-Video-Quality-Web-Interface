import * as $ from 'jquery';
import { recordCaliStartTime, increase, decrease } from "./Calibration";
import { getLocalData } from "../utils/ManageLocalData";
import { globalStatus } from "./GlobalStatus";
import { readInst, actStartExpBtn, adjustDist, addResultToCurVideo, processHit, actNextHitBtn } from "./BtnActions"


export function keyboardControl(){
    document.onkeyup = function (event) {
        var e = event || window.event;
        var keyCode = e.keyCode || e.which || e.code;
        switch (keyCode) {
            case 13://space
            case 32://enter
                if(globalStatus.exp_status == "inst_panel") {
                    readInst();
                } else if(globalStatus.exp_status == "dist_panel") {
                    adjustDist();
                } else if(globalStatus.exp_status == "hit_panel") {
                    actStartExpBtn();
                } else if(globalStatus.exp_status == "next-hit-panel") {
                    actNextHitBtn();
                }
                break;
            
            case 37: // left arrow
                if(globalStatus.exp_status == "decision") {
                    addResultToCurVideo("L");
                    processHit();
                }
                break

            case 39: // right arrow
                if(globalStatus.exp_status == "decision") {
                    addResultToCurVideo("R");
                    processHit();
                }
                break
            
            case 40: // down arrow
                if(globalStatus.exp_status == "decision") {
                    if ($("#not-sure-btn").attr("disabled") != "disabled") {
                        addResultToCurVideo("not sure");
                        processHit();
                    }
                }
                break

            default:
                break;
        }
    }

    document.onkeydown = function (event) {
        var e = event || window.event;
        var keyCode = e.keyCode || e.which;
        switch (keyCode) {
            case 38://up arrow
                e.preventDefault();
                if (getLocalData("hasCalibrated") == "false") {
                    $("#cali-fit-btn").css("visibility", "visible");
                    recordCaliStartTime();
                    increase();
                }
                break;
            case 40://down arrow
                e.preventDefault();
                if (getLocalData("hasCalibrated") == "false") {
                    $("#cali-fit-btn").css("visibility", "visible");
                    recordCaliStartTime();
                    decrease();    
                }
                break;
            default:
                break;
        }
    }
}

