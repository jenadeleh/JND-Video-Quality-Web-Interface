import * as $ from 'jquery';
import { storeLocalData, getLocalData } from "../utils/ManageLocalData"
import { displayConsentForm } from "./DisplayConsentForm"
import { requestVideos } from "./RequestVideos"
import { processResponse } from "./ProcessResponse"
import { initDoms } from "./InitDoms"
import { sendMsg } from "./Connection"

export function initGUI() {
    sendMsg({"action":"get_instruction"}).then(response => {
        _init_gui(response)
    }).catch(err => {
        console.log("get_instruction errors");  
    })
}

function _init_gui(response) {
    _init_instruction(response)
    _init_doms();
    _init_local_storage();

    // let didConsentForm  = getLocalData("didConsentForm");
    // if (didConsentForm === null) {
    //     storeLocalData("didConsentForm", "false");
    //     displayConsentForm();
    // } else if (didConsentForm == "false") {
    //     displayConsentForm();
    // } else if (didConsentForm == "true") {
    //     // TODO: calibration
    // }

    // storeLocalData("pname", "guangan"); //TODO: remove later

    // // request videos information
    // processResponse(requestVideos(getLocalData("pname"), getLocalData("puid")));


    // updateProgressBar(taskRecord.finish_num, taskRecord.TASK_NUM);
}

function _init_local_storage() {
    let exp  = getLocalData("exp");
    if (exp === null) {
        storeLocalData("pname", "");
        storeLocalData("puid", "");
        storeLocalData("exp", "");
    } 
    return
}

function _init_doms() {
    initDoms();
}

function _init_instruction(response) {
    let instruction = processResponse(response);
    _render_instruction(instruction);
    $("#instruction-modal").modal("show");
}

function _render_instruction(instruction) {
    $(".instruction-content").html(instruction);
}