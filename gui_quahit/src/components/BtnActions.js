import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus";
import { updateProgressBar } from "./ProgressBar";
import { getLocalData } from "../utils/ManageLocalData";
import { sendMsg } from "./SendMsg";
import { passCF_action } from "./ConsentForm";
import { setTimer } from "./Timer";

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
  if (globalStatus.session=="training") {
    let gt = globalStatus.cur_video_pair["ground_truth"].split(",");

    if (gt.indexOf(decision) == -1) {
      coaching();
    } else {
      processHit();
    }
  } else {
    addResultToCurVideo(decision);
    processHit();
  }
}

export function coaching() {
  globalStatus.coaching = true;
  $("#decision-timeout-msg").css("display", "none");
  $(`#vc-${globalStatus.curVideoDomId}`).css("visibility", "visible")
  $("#hint").html("Hint:" + globalStatus.cur_video_pair["message"]);
  clearTimeout(globalStatus.FIRST_DURATION_TIMER);
  clearTimeout(globalStatus.SECOND_DURATION_TIMER);
  $("#hint-frame").css("display", "inline-block");
  $("#not-sure-btn").attr("disabled", true)
                  .removeClass("btn-primary")
                  .addClass("btn-secondary");
  globalStatus.isNotSureBtnAvl = false;
  $("#left-btn, #right-btn").attr("disabled", true);
}

export function tryAgainAction() {
  globalStatus.coaching = false;
  clearTimeout(globalStatus.FIRST_DURATION_TIMER);
  clearTimeout(globalStatus.SECOND_DURATION_TIMER);
  $("#hint-frame").css("display", "none");
  $("#left-btn, #right-btn").attr("disabled", false);
  setTimer();
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
  _displatStartTrainingMsg();
  $("#dist-panel").css("display", "none");
  $("#hit-panel").css("display", "inline");
  // actNextHitBtn();
}

export function startTraining() {
  $("#start-training-btn").css("display", "none");
  $("#dist-panel").css("display", "none");
  $("#hit-panel").css("display", "inline");
  actNextHitBtn();
}





export function readInst() {
  $("#inst-panel").css("display", "none");
  globalStatus.exp_status = "";
  
  if (getLocalData("workerid")){
    $("#ask-for-wid").html("Please confirm your worker ID.")
    $("#cf-workerid").val(getLocalData("workerid"))
  }
  
  $("#cf-panel").css("display", "inline");
}

function _endHit() {
  if (globalStatus.session=="training") {
    _displatStartQuizMsg();
  } else if (globalStatus.session=="quiz") {
    _sendResult();
  } 
}

function _displatStartQuizMsg() {
  globalStatus.session = "quiz";
  $(".video-cover").remove();
  $(".decision-btn").attr("disabled", true);
  $("#guide-panel, #task-progressbar, #instruction-btn").css("visibility", "hidden");
  $("#hit-end-panel").css("display", "inline");
  $("#video-spinner").css("display", "none")
                    .removeClass("d-flex");

  $("#hit-end-panel-msg").css("visibility", "hidden")
  $("#hit-end-text").html(globalStatus.quiz_description);
  $("#next-hit-btn").css("display", "inline-block");

  globalStatus.exp_status = "next-hit-panel";
  globalStatus.loaded_video_num = 0;
  updateProgressBar(0, globalStatus.video_num);
  globalStatus.videos_original_url = []
  globalStatus.videos_pairs_sequence = []
  globalStatus.videos_pairs = {};
  globalStatus.task_num = 0;
  globalStatus.videos_url_mapping = {};
}


function _displatStartTrainingMsg() {
  globalStatus.session = "training";
  $(".video-cover").remove();
  $(".decision-btn").attr("disabled", true);
  $("#guide-panel, #task-progressbar, #instruction-btn").css("visibility", "hidden");
  $("#hit-end-panel").css("display", "inline");
  $("#video-spinner").css("display", "none")
                    .removeClass("d-flex");

  $("#hit-end-panel-msg").css("visibility", "hidden")
  $("#hit-end-text").html(globalStatus.training_description);
  $("#start-training-btn").css("display", "inline-block");
}

export function displayEndHitPanel(code) {
  $(".video-cover").remove();
  $(".decision-btn").attr("disabled", true);
  $("#guide-panel, #task-progressbar, #instruction-btn").css("visibility", "hidden");
  $("#hit-end-panel").css("display", "inline");
  $("#hit-end-panel-msg").css("visibility", "visible")
  $("#video-spinner").css("display", "none")
                    .removeClass("d-flex");

  $("#home-page-btn").css("display", "inline-block");
  $("#next-hit-btn").css("display", "none");

  $("#hit-end-text").html(code);
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
    "action":"record_quiz_result",
    "euid":getLocalData("euid"),
    "workerid": getLocalData("workerid"),
    "data": {
      "result":globalStatus.result,
      "os_info": globalStatus.os_info,
      "cali_info": cali_info
    }
  };

  globalStatus.result = [];

  sendMsg(send_data).then(response => {
    if (response["status"] == "successful") {
      displayEndHitPanel(response["code"]);
    } else if (response["status"] == "failed") {
      displayEndHitPanel(response["error"]);
    }
  });
}