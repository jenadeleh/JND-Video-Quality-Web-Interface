import * as $ from 'jquery';
import { recordCaliStartTime, increase, decrease } from "./Calibration";
import { getLocalData } from "../utils/ManageLocalData";
import { actStartExpBtn } from "./BtnActions" 
import { adjustDist } from "./BtnActions"
import { globalStatus } from "./GlobalStatus";
import { addResultToCurVideo, processHit, actNextHitBtn } from "./BtnActions"

export function keyboardControl(){
    document.onkeyup = function (event) {
        var e = event || window.event;
        var keyCode = e.keyCode || e.which || e.code;
        switch (keyCode) {
            case 13://space
            case 32://enter

                if(globalStatus.display_panel == "dist-panel") {
                    adjustDist();
                    globalStatus.display_panel = "hit-panel";
                } else if(globalStatus.display_panel == "hit-panel") {
                    actStartExpBtn();
                    globalStatus.display_panel = "";
                } else if(globalStatus.display_panel == "next-hit-panel") {
                    actNextHitBtn();
                }
                break;
            
            case 37: // left arrow
                addResultToCurVideo("L");
                processHit();
                break

            case 39: // right arrow
                addResultToCurVideo("R");
                processHit();
                break
            
            case 40: // down arrow
                if ($("#not-sure-btn").attr("disabled") != "disabled") {
                    addResultToCurVideo("not sure");
                    processHit();
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

