import * as $ from 'jquery';
import { actStartExpBtn, actDecisionBtn, actNextHitBtn, adjustDist} from "./BtnActions"
import { submitCf } from "./ConsentForm"
import { storeLocalData } from "../utils/ManageLocalData"

export function initDoms() {
    $('#start-exp-btn').on('click', (e)=> {
        actStartExpBtn();
    });
    
    $('.decision-btn').on('click',(e)=> {
        actDecisionBtn(e);
    });

    $('#next-hit-btn').on('click', (e)=> {
        actNextHitBtn();
    });

    $("#cali-adjust-dist").on('click', (e)=> {
        adjustDist();
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

