import * as $ from 'jquery';
import { storeLocalData, getLocalData } from "../utils/ManageLocalData"
import { initDoms } from "./InitDoms"
import { processResponse } from "./ProcessResponse"
import ConsentForm from "./ConsentForm"
import Videos from "./Videos"
import { globalStatus } from "./GlobalStatus"

export function initGUI() {
    _init_doms();
    _init_local_storage();

    const consent_form = new ConsentForm();
    
    // request instruction and consent form
    consent_form.req_ins_consent_f().then(response => {
        let [inst, cf] = processResponse(response)
        consent_form.render_instruction(inst);

        if (getLocalData("hasSignedCF") === "false") {
            consent_form.render_consent_form(cf);
        } else if (getLocalData("hasSignedCF") === "true") {
            console.log("----- hasSignedCF -----");
            // TODO: calibration
            // actions after calibration
            _displayExpPanel();      
        }

    }).catch(err => {
        console.log("req_ins_consent_f errors: " + err.message);  
    })

    // submit the consent form
    let $cf_form = $("#cf-form");
    $cf_form.on("submit", () =>{ 
        let params = {};
        $cf_form.serializeArray().forEach((element)=>{
            params[element.name] = element.value;
        });
        storeLocalData("pname", params.pname);

        consent_form.submitCfResult(params.pname, params.pemail).then(response => {
            let { puid, exp } = processResponse(response);
            storeLocalData("exp", exp);
            storeLocalData("puid", puid);
            
            storeLocalData("hasSignedCF", "true");

            // TODO: calibration
            // actions after calibration
            _displayExpPanel();

        }).catch(err => {
            console.log("submitCfResult errors: " + err.message);  
        });
        return false;
    })
}
function _displayExpPanel() {
    const videos = new Videos();

    $("#cf-panel").css("display", "none");
    $("#exp-panel").css("display", "inline"); 

    $("#video-spinner, #video-pool").css("height", globalStatus.video_h)
                                    .css("width", globalStatus.video_w);

    // request and load videos
    videos.reqLoadVideos(getLocalData("pname"), getLocalData("puid"));
}

function _init_local_storage() {
    let exp  = getLocalData("exp");
    if (exp == null) {
        storeLocalData("pname", "");
        storeLocalData("puid", "");
        storeLocalData("exp", "");
        storeLocalData("hasSignedCF", "false");
    } 
}

function _init_doms() {
    initDoms();
}

