import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus"
import { displayVideos, reqLoadVideos } from "./Videos"
import { updateProgressBar } from "./ProgressBar"
import { getLocalData } from "../utils/ManageLocalData"
import { sendMsg } from "./Connection"
import { setTimer } from "./Timer"

export function actStartExpBtn() {
    $("#start-exp-btn").attr("disabled", true)
                    .css("display", "none");

    $("#left-btn, #right-btn").attr("disabled", false);

    _playCurVideo();
    setTimer();
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
    $(".decision-btn").attr("disabled", true);
    // request new videos
    reqLoadVideos(getLocalData("pname"), getLocalData("puid"));
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

    clearTimeout(globalStatus.first_duration_timer);
    clearTimeout(globalStatus.second_duration_timer);       

    if (globalStatus.videos.length > 0) {
        displayVideos();
        _playCurVideo();
        setTimer();
    } else {
        _endHit();
    }
}

function _playCurVideo() {
    let vuid = globalStatus.cur_video["vuid"];
    $(`#${vuid}`).get(0).play();

    globalStatus.cur_video["start_time"] = new Date().getTime();
}

function _endHit() {
    _displayUIComponents();
    sendResult();
}

function _displayUIComponents() {
    $(".video-cover").remove();
    $(".decision-btn").attr("disabled")
    $("#guide-panel, #task-progressbar, #instruction-btn").css("visibility", "hidden");
    $("#hit-end-panel").css("display", "inline");
    updateProgressBar(0, globalStatus.video_num);
}

function sendResult() {
    let send_data = {"action":"record_result",
                    "pname": getLocalData("pname"),
                    "puid": getLocalData("puid"),
                    "result": globalStatus.result};
    globalStatus.result = [];
    sendMsg(send_data);
}
