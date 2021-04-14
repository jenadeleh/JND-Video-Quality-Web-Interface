import * as $ from 'jquery';
import { actStartExpBtn, actDecisionBtn, actNextHitBtn, adjustDist} from "./BtnActions"
import { submitCf } from "./ConsentForm"
import { storeLocalData } from "../utils/ManageLocalData"
import { globalStatus } from "./GlobalStatus";
import { passCF_action } from "./ConsentForm"

export function initDoms() {
    $('#start-exp-btn').on('click', (e)=> {
        actStartExpBtn();
    });
    
    $('.decision-btn').on('click',(e)=> {
        actDecisionBtn(e);
    });

    $('#next-hit-btn').on('click', (e)=> {
        globalStatus.exp_status = "hit_panel";
        actNextHitBtn();
    });

    $("#cali-adjust-dist").on('click', (e)=> {
        adjustDist();
    });

    $("#read-inst-btn").on('click', (e)=> {
        $("#inst-panel").css("display", "none");
        if (globalStatus.ispexist) {
            passCF_action();
        } else {
            $("#cf-panel").css("display", "inline");
        }
    });

    let $cf_form = $("#cf-form");
    $cf_form.on("submit", () =>{ 
        let params = {};
        $cf_form.serializeArray().forEach((element)=>{
            params[element.name] = element.value;
        });
        storeLocalData("pname", params.pname);
    
        if (!params.pemail) {
            params.pemail = "";
        }
    
        submitCf(params.pname, params.pemail);
        return false;
    })
}

