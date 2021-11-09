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

// TODO: check result is correct, give hint, try again, timeout, try again

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

    console.log(`your decision: ${decision}, gt: ${gt}`);
    if (gt.indexOf(decision) == -1) {
      $("#hint").html("Hint:" + globalStatus.cur_video_pair["message"]);
      clearTimeout(globalStatus.FIRST_DURATION_TIMER);
      clearTimeout(globalStatus.SECOND_DURATION_TIMER);
      $("#hint-frame").css("display", "inline-block");
      $("#left-btn, #right-btn").attr("disabled", true);
      $("#not-sure-btn").attr("disabled", true)
                      .removeClass("btn-primary")
                      .addClass("btn-secondary");

      // TODO: coaching
      // TODO: no decision, coaching
      // TODO: 
    } else {
      processHit();
      console.log("correct answer")
    }
  } else {
    addResultToCurVideo(decision);
    processHit();
  }


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
  if (globalStatus.session=="quiz") {
    _sendResult();
  }
}

export function displayEndHitPanel(code) {
  $(".video-cover").remove();
  $(".decision-btn").attr("disabled", true);
  $("#guide-panel, #task-progressbar, #instruction-btn").css("visibility", "hidden");
  $("#hit-end-panel").css("display", "inline");
  $("#video-spinner").css("display", "none")
                    .removeClass("d-flex");

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