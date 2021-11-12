import * as $ from 'jquery';
import { sendMsg } from "./SendMsg"
import { storeLocalData, getLocalData } from "../utils/ManageLocalData"
import { checkCaliStatus, calibration, passCali } from "./Calibration"
import { globalStatus } from "./GlobalStatus"

export function req_inst_cf() {
    let data = {"action":"req_inst_cf", "puid":getLocalData("puid"), "quahit":"yes"};
    sendMsg(data).then(response => {
        _process_response(response)
    }).catch(err => {
        console.log("req_inst_cf errors: " + err.message);
    })
}

export function submitCf(workerid) {
  passCF_action();
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
        _render_interface_text(response["data"]);
        $("#inst-panel").css("display", "inline");

    } else if (response["status"] == "failed") {
        $("#msg-panel").html(response["data"]).css("display", "inline");
        return response["data"];
    }
}

function _render_interface_text(response_data) {
  let {
    instruction, 
    consent_form, 
    question, 
    text_end_hit, 
    text_end_exp, 
    btn_text_end_hit, 
    decision_timeout_msg,
    instruction_btn_text,
    consent_btn_text,
    assignment_num_text,
    training_description,
    quiz_description,
    flickering_test_description,
    quality_test_description,
    quiz_videos, 
    training_videos,
    euid,
    wait_time,
    download_time,
    download_timeout_msg, 
    waiting_timeout_msg,
  } = response_data

  storeLocalData("euid", euid);
  globalStatus.download_time = download_time;
  globalStatus.wait_time = wait_time;
  globalStatus.training_description = training_description;
  globalStatus.training_description = quiz_description;
  globalStatus.flickering_test_description = flickering_test_description;
  globalStatus.quality_test_description = quality_test_description;
  globalStatus.training_videos = training_videos;
  globalStatus.quiz_videos = quiz_videos;
  globalStatus.download_timeout_msg = download_timeout_msg;
  globalStatus.waiting_timeout_msg = waiting_timeout_msg;

  _render_instruction(instruction);
  _render_consent_form(consent_form);
  _render_question_text(question);
  _render_end_hit_text(text_end_hit, btn_text_end_hit);
  _render_timeout_text(decision_timeout_msg);
  _render_read_inst_btn_text(instruction_btn_text);
  _render_read_consent_btn_text(consent_btn_text);
  _store_end_exp_text(text_end_exp);
  _store_assignment_num_text(assignment_num_text);
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
  // $("#hit-end-text").html(text_end_hit);
  // $("#next-hit-btn").html(btn_text_end_hit);
  $("#home-page-btn").html(btn_text_end_hit);
}

function _render_question_text(question) {
  $("#question").html(question);
}

function _render_timeout_text(decision_timeout_msg) {
  $("#decision-timeout-msg").html(`<h3>${decision_timeout_msg}</h3>`);
}

function _render_read_inst_btn_text(instruction_btn_text) {
  $("#read-inst-btn").html(instruction_btn_text);
}

function _render_read_consent_btn_text(consent_btn_text) {
  $("#cf-submit-btn").attr("value", consent_btn_text);
}

function _store_end_exp_text(text_end_exp) {
  globalStatus.text_end_exp = text_end_exp;
}

function _store_assignment_num_text(assignment_num_text) {
  globalStatus.assignment_num_text = assignment_num_text;
}
