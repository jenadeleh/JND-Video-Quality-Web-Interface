import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus"
import { displayNextVideo, reqLoadVideos, recordTime, stopExpireTimer } from "./Videos"
import { updateProgressBar } from "./ProgressBar"
import { getLocalData } from "../utils/ManageLocalData"
import { sendMsg } from "./SendMsg"
import { passCF_action } from "./ConsentForm"


export function actStartExpBtn(e) {
    $("#start-exp-btn").attr("disabled", true)
                    .css("display", "none");

    $("#left-btn, #right-btn").attr("disabled", false);
    let cur_vuid = globalStatus.cur_video["vuid"];
    $(`#${cur_vuid}`).get(0).play();
    stopExpireTimer();
    recordTime();
}

export function actDecisionBtn(e) {
    let decision = $(e.target).attr("data-decision");
    addResultToCurVideo(decision);
    processHit();
}

export function actNextHitBtn() {
    $("#hit-end-panel").css("display", "none");
    $("#start-exp-btn").css("display", "inline");
    $("#guide-panel, #task-progressbar, #instruction-btn").css("visibility", "visible");
    $("#video-spinner").css("display", "inline").addClass("d-flex");
    $(".decision-btn").attr("disabled", true);
    $("#start-exp-btn").attr("disabled",true);
    $("#video-cover").remove();

    globalStatus.exp_status = "hit_panel";

    // request new videos
    reqLoadVideos(getLocalData("pname"), getLocalData("puid"), getLocalData("euid"));
}

export function addResultToCurVideo(decision) {
    globalStatus.cur_video["decision"] = decision;
    globalStatus.cur_video["end_time"] = new Date().getTime();
    globalStatus.result.push(globalStatus.cur_video);
    // console.log("----- Result of Current Video -----");
    // console.log(globalStatus.cur_video);
}

export function processHit() {
    $("#not-sure-btn").attr("disabled", true)
                    .removeClass("btn-primary")
                    .addClass("btn-secondary");
    $(".video-cover").css("visibility", "visible");
    $("#timeout-msg").css("display", "none");

    updateProgressBar(globalStatus.video_num - globalStatus.videos.length
                    , globalStatus.video_num);

    clearTimeout(globalStatus.FIRST_DURATION_TIMER);
    clearTimeout(globalStatus.SECOND_DURATION_TIMER);       

    if (globalStatus.videos.length > 0) {
        displayNextVideo();
    } else {
        clearTimeout(globalStatus.EXPIRE_TIMER);
        _endHit();
    }
}

export function adjustDist() {
    $("#dist-panel").css("display", "none");
    $("#hit-panel").css("display", "inline");
    actNextHitBtn();
}

export function readInst() {
    $("#inst-panel").css("display", "none");
    globalStatus.exp_status = "";
    if (globalStatus.ispexist) {
        passCF_action();
    } else {
        $("#cf-panel").css("display", "inline");
    }
}

function _endHit() {
    displayEndHitPanel();
    _sendResult();
}

export function displayEndHitPanel() {
    $(".video-cover").remove();
    $(".decision-btn").attr("disabled")
    $("#guide-panel, #task-progressbar, #instruction-btn").css("visibility", "hidden");
    $("#hit-end-panel").css("display", "inline");
    $("#video-spinner").css("display", "none").removeClass("d-flex");
    globalStatus.exp_status = "next-hit-panel";
    updateProgressBar(0, globalStatus.video_num);
    globalStatus.loaded_video_num = 0;
}

function _sendResult() {
    let cali_info = {};

    ["cali_time", "browser_width_cm", "browser_height_cm", "devicePixelRatio", "px_cm_rate"].forEach((el)=>{
        cali_info[el] = getLocalData(el);
    });

    let send_data = {
                        "action":"record_result",
                        "euid":getLocalData("euid"),
                        "pname": getLocalData("pname"),
                        "puid": getLocalData("puid"),
                        "data": {"result":globalStatus.result,
                                "os_info": globalStatus.os_info,
                                "cali_info": cali_info}
                    };
    globalStatus.result = [];
    sendMsg(send_data);
}


