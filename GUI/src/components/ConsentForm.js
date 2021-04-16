import * as $ from 'jquery';
import { sendMsg } from "./Connection"
import { storeLocalData, getLocalData } from "../utils/ManageLocalData"
import { checkCaliStatus, calibration, passCali } from "./Calibration"
import { globalStatus } from "./GlobalStatus"

export function req_inst_cf() {
    let data = {"action":"req_inst_cf", "puid":getLocalData("puid")};
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
            let { euid, puid } = response["data"];
            storeLocalData("euid", euid);
            storeLocalData("puid", puid);
            passCF_action();
        } else if (response["status"] == "failed") {
            $("#msg-panel").html(response["data"]).css("display", "inline");
            return response["data"];
        }
    }).catch(err => {
        console.log("submitCf errors: " + err.message);  
    });
}

export function passCF_action() {
    $("#cf-panel").css("display", "none");
    checkCaliStatus();
    if (getLocalData("hasCalibrated") == "true") {
        passCali();
        globalStatus.exp_status = "dist_panel"
    } else { // need to do calibration
        $("#cali-panel").css("display", "inline");
        calibration();
    }
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
            timeout_msg,
            instruction_btn_text} = response["data"] 

        _render_interface_text(instruction, 
                                consent_form,
                                question, 
                                text_end_hit, 
                                text_end_exp, 
                                btn_text_end_hit, 
                                timeout_msg,
                                instruction_btn_text);

        $("#inst-panel").css("display", "inline");
        
        globalStatus.ispexist = ispexist;

    } else if (response["status"] == "failed") {
        $("#msg-panel").html(response["data"]).css("display", "inline");
        clearTimeout(globalStatus.env_bg_interval);
        return response["data"];
    }
}

function _render_interface_text(instruction, 
                                consent_form,
                                question, 
                                text_end_hit, 
                                text_end_exp, 
                                btn_text_end_hit, 
                                timeout_msg,
                                instruction_btn_text) {

    _render_instruction(instruction);
    _render_consent_form(consent_form);
    _render_question_text(question);
    _render_end_hit_text(text_end_hit, btn_text_end_hit);
    _render_timeout_text(timeout_msg);
    _render_end_exp_text(text_end_exp);
    _render_read_inst_btn_text(instruction_btn_text);
}

function _render_instruction(instruction) {
    $(".instruction-content").html(instruction);
    globalStatus.exp_status = "inst_panel";
    if (globalStatus.mode == "production") {
        $("#instruction-modal").css("display", "inline");
        $("#instruction-modal").modal("show");
    }
}
    
function _render_consent_form(consent_form) {
    $("#cf-content").html(consent_form); 
}

function _render_end_hit_text(text_end_hit, btn_text_end_hit) {
    $("#hit-end-text").html(text_end_hit);
    $("#next-hit-btn").html(btn_text_end_hit);
}

function _render_question_text(question) {
    $("#question").html(question);
}

function _render_timeout_text(timeout_msg) {
    $("#timeout-msg").html(timeout_msg);
}

function _render_read_inst_btn_text(instruction_btn_text) {
    $("#read-inst-btn").html(instruction_btn_text);
}

function _render_end_exp_text(text_end_exp) {
    globalStatus.text_end_exp = text_end_exp;
}
