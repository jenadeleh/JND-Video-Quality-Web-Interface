import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus";
import { updateProgressBar } from "./ProgressBar";
import { getLocalData } from "../utils/ManageLocalData";
import { sendMsg } from "./SendMsg";
import { passCF_action } from "./ConsentForm";
import { 
  displayNextVideo, 
  reqLoadVideos, 
  recordTime, 
  stopExpireTimer, 
  constructDomId
} from "./Videos";

export function actStartExpBtn(e) {
  $("#start-exp-btn").attr("disabled", true)
                  .css("display", "none");
  $("#left-btn, #right-btn").attr("disabled", false);

  globalStatus.canMakeDecision = true;
  let cur_video_pair = globalStatus.cur_video_pair; 
  let videoDomId = constructDomId(cur_video_pair)

  $(`#left-${videoDomId}`).get(0).play();
  $(`#right-${videoDomId}`).get(0).play();
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
  $(".decision-btn, #start-exp-btn").attr("disabled", true);
  $("#video-cover").remove();

  globalStatus.exp_status = "hit_panel";
  globalStatus.canMakeDecision = false;

  // request new videos
  reqLoadVideos(
    getLocalData("workerid"), 
    getLocalData("puid"), 
    getLocalData("euid")
  );
}

export function addResultToCurVideo(decision) {
  globalStatus.cur_video_pair["decision"] = decision;
  globalStatus.cur_video_pair["end_time"] = new Date().getTime();
  globalStatus.result.push(globalStatus.cur_video_pair);  
  // console.log("----- Result of Current Video -----");
  // console.log(globalStatus.cur_video_pair);
}

export function processHit() {
  globalStatus.isNotSureBtnAvl = false;
  $("#not-sure-btn").attr("disabled", true)
                  .removeClass("btn-primary")
                  .addClass("btn-secondary");
  $(".video-cover").css("visibility", "visible");
  $("#decision-timeout-msg").css("display", "none");

  updateProgressBar(
    globalStatus.task_num - globalStatus.videos_pairs_sequence.length, 
    globalStatus.task_num
  );

  clearTimeout(globalStatus.FIRST_DURATION_TIMER);
  clearTimeout(globalStatus.SECOND_DURATION_TIMER);       
  

  if (globalStatus.videos_pairs_sequence.length > 0) {
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
  $(".decision-btn").attr("disabled", true);
  $("#guide-panel, #task-progressbar, #instruction-btn").css("visibility", "hidden");
  $("#hit-end-panel").css("display", "inline");
  $("#video-spinner").css("display", "none")
                    .removeClass("d-flex");
  $("#finish-asgm-num").html(
    globalStatus.assignment_num_text.replace(
      "placeholder", globalStatus.finished_assignment_num+1
    )
  );
  globalStatus.exp_status = "next-hit-panel";
  globalStatus.loaded_video_num = 0;
  $("#loading-progress").html(globalStatus.loaded_video_num+ "/" +globalStatus.video_num);
  updateProgressBar(0, globalStatus.video_num);
}

function _sendResult() {
  let cali_info = {};

  [
    "cali_time", 
    "browser_width_cm", 
    "browser_height_cm", 
    "devicePixelRatio", 
    "px_cm_rate"
  ].forEach((el)=>{cali_info[el] = getLocalData(el);});

  let send_data = {
    "action":"record_result",
    "euid":getLocalData("euid"),
    "puid": getLocalData("puid"),
    "workerid": getLocalData("workerid"),
    "data": {
      "result":globalStatus.result,
      "os_info": globalStatus.os_info,
      "cali_info": cali_info
    }
  };
  globalStatus.result = [];
  sendMsg(send_data);
}