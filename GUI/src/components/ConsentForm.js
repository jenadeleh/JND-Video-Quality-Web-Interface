import * as $ from 'jquery';
import { sendMsg } from "./Connection"
import { storeLocalData, getLocalData } from "../utils/ManageLocalData"
import { calibration } from "./Calibration"
import { globalStatus } from "./GlobalStatus"

export function req_inst_cf() {
    let data = {"action":"req_inst_cf", "pname":getLocalData("pname")};
    sendMsg(data).then(response => {
        _process_response(response)
    }).catch(err => {
        console.log("req_inst_cf errors: " + err.message);  
    })
}

export function submitCf(pname, pemail) {
    let data = {"action":"user_register", "pname":pname, "pemail":pemail};
    sendMsg(data).then(response => {
        if (response["status"] == "successful") {
            let { exp, puid } = response["data"];
            storeLocalData("exp", exp);
            storeLocalData("puid", puid);
            _passCF_action();
        } else if (response["status"] == "failed") {
            alert(response["data"]);
            return response["data"];
        }
    }).catch(err => {
        console.log("submitCf errors: " + err.message);  
    });
}

function _passCF_action() {
    calibration();// remove
}

function _process_response(response) {
    if (response["status"] == "successful") {
        let {ispexist, 
            instruction, 
            consent_form, 
            question, 
            text_end_hit, 
            text_end_exp, 
            btn_text_end_hit, 
            timeout_msg} = response["data"] 

        _render_interface_text(instruction, 
                                    question, 
                                    text_end_hit, 
                                    text_end_exp, 
                                    btn_text_end_hit, 
                                    timeout_msg)

        if (ispexist) {
            _passCF_action();
        } else {
            _render_consent_form(consent_form);
        }

    } else if (response["status"] == "failed") {
            alert(response["data"]);
            return response["data"];
    }
}

function _render_interface_text(instruction, 
                                question, 
                                text_end_hit, 
                                text_end_exp, 
                                btn_text_end_hit, 
                                timeout_msg) {

    _render_instruction(instruction);
    _render_question_text(question);
    _render_end_hit_text(text_end_hit, btn_text_end_hit);
    _render_timeout_text(timeout_msg);
    _render_end_exp_text(text_end_exp);
}

function _render_instruction(instruction) {
    $(".instruction-content").html(instruction);
    if (globalStatus.mode == "production") {
        $("#instruction-modal").css("display", "inline");
        $("#instruction-modal").modal("show");
    }
}
    
function _render_consent_form(consent_form) {
    $("#cf-content").html(consent_form); 
    $("#cf-panel").css("display", "inline")
}

function _render_end_hit_text(text_end_hit, btn_text_end_hit) {
    $("#hit-end-text").html(text_end_hit)
    $("#next-hit-btn").html(btn_text_end_hit)
}

function _render_question_text(question) {
    $("#question").html(question)
}

function _render_timeout_text(timeout_msg) {
    $("#timeout-msg").html(timeout_msg)
}

function _render_end_exp_text(text_end_exp) {
    // TODO:
}
