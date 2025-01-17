import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus";
import { updateProgressBar } from "./ProgressBar";
import { getLocalData, storeLocalData } from "../utils/ManageLocalData";
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
  let gt = globalStatus.cur_video_pair["ground_truth"];
  let isCorrect = true;

  if (gt.indexOf(decision) == -1) {
    isCorrect = false;
  }

//   console.log("decision" + decision);
//   console.log("gt" + gt);
//   console.log("isCorrect" + isCorrect);

  if (globalStatus.session=="training") {
    // processHit(); // remove 
    if (isCorrect==false) {
      coaching(decision);
    } else if (isCorrect==true) {
      $("#hint").html(globalStatus.pass_training_question_text).css("display", "inline-block");
      $("#hint-frame").css("display", "inline-block");
      $("#try-again-btn").css("display", "none");
      setTimeout(()=> {
        $("#try-again-btn").css("display", "inline-block");
        $("#hint-frame").css("display", "none");
        processHit();
      }, 1000*globalStatus.traing_pass_text_timeout);
    }
  } else {
    if (isCorrect==false) {
      globalStatus.failedQuizNum += 1;
    } 
    addResultToCurVideo(decision);
    processHit();
  }
}

export function coaching(decision) {
  globalStatus.coaching = true;
  $("#decision-timeout-msg").css("display", "none");
  $(`#vc-${globalStatus.curVideoDomId}`).css("visibility", "visible")

  if (decision) {
    $("#hint").html("Hint:" + globalStatus.cur_video_pair["message"]);
  } else {
    $("#hint").html("Hint:" + globalStatus.no_decision_training_msg);
  }
  
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
  let videoDomId = globalStatus.curVideoDomId;
  $(`#left-${videoDomId}`).get(0).currentTime = 0;
  $(`#right-${videoDomId}`).get(0).currentTime = 0;

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
    storeLocalData("didTraining","true");
    globalStatus.isPassQuiz = (globalStatus.failedQuizNum <=globalStatus.failedQuizNumThr) ? true:false;
    _sendResult();
    _process_quiz_result();
    
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

export function displayEndHitPanel() {
  $(".video-cover").remove();
  $(".decision-btn").attr("disabled", true);
  $("#guide-panel, #task-progressbar, #instruction-btn").css("visibility", "hidden");
  $("#hit-end-panel").css("display", "inline");
  $("#hit-end-panel-msg").css("visibility", "visible")
  $("#video-spinner").css("display", "none")
                    .removeClass("d-flex");
  $("#hit-end-btn").css("display", "inline-block");
  $("#next-hit-btn").css("display", "none");
}

// function _gen_study_hit_url() {
//     let study_hit_url = "";
//     let info = "";

//     const context_items = [
//       "availHeight", 
//       "availWidth", 
//       "browser_height_cm", 
//       "browser_width_cm", 
//       "cali_time", 
//       "devicePixelRatio", 
//       "didTraining", 
//       "euid", 
//       "hasCalibrated", 
//       "outerHeight", 
//       "outerWidth", 
//       "px_cm_rate", 
//       "puid",
//       "workerid"
//     ];
  
//     context_items.forEach(function(item,idx)  {
//       if (info.length == 0) {
//         info = info + getLocalData(item)
//       } else {
//         info = info + "-" + getLocalData(item)
//       }
//     });
//     study_hit_url = globalStatus.study_hit_url + "studyhit/?info=" + info;
//     return study_hit_url
//   }

  
function _process_quiz_result() {
  // let study_hit_url = _gen_study_hit_url();
  globalStatus.isPassQuiz = (globalStatus.failedQuizNum <=globalStatus.failedQuizNumThr) ? true:false;
  if (globalStatus.isPassQuiz) {
    $("#hit-end-panel-msg").html(globalStatus.pass_quiz_text);
    $("#hit-end-text").html("");
    $("#main-study-btn").attr("href", globalStatus.study_hit_url);

    $("#show-instruction-btn, #main-study-btn").css("display", "inline-block");
    _show_code();
  } else {
    $("#hit-end-text").html("");
    $("#hit-end-panel-msg").html(globalStatus.fail_quiz_text);
    _show_code();
  }
}

function _show_code() {
    $("#hit-end-btn").html("Show the payment code and quit the experiment");
    $('#hit-end-btn').on('click', (e)=> {
      $("#msg-panel").html(
          globalStatus.text_end_exp 
          + "</br>" 
          + "<h2>" + globalStatus.copy_code + "</h2>"
          + "</br>" + "</br>"
          + "<button class='btn btn-info' type='button' id='display-survey-btn'>" + globalStatus.survey_btn_text + "</button>"
          + "</br>" + "</br>"
          + "<h3>" + globalStatus.code + "</h3>"
      ).css("display", "inline").css("z-index", 1);
      $("#hit-end-panel, #hit-panel").css("display", "none");
      $("#display-survey-btn").on('click', (e)=> {
        $("#survey-cover").css("display", "inline-block").css("visibility", "visible");
      });
    });
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

  let tmp_isPassQuiz = "false"

  if (globalStatus.isPassQuiz == true) {
    tmp_isPassQuiz = "true"
  } else if (globalStatus.isPassQuiz == false) {
    tmp_isPassQuiz = "false"
  }

  let send_data = {
    "action":"record_quiz_result",
    "euid":getLocalData("euid"),
    "workerid": getLocalData("workerid"),
    "data": {
      "result":globalStatus.result,
      "isPassQuiz": tmp_isPassQuiz,
      "os_info": globalStatus.os_info,
      "cali_info": cali_info
    }
  };

  globalStatus.result = [];

  sendMsg(send_data).then(response => {
    if (response["status"] == "successful") {
        globalStatus.code = response["code"];
      displayEndHitPanel();
      if (globalStatus.isPassQuiz == false) {
        displayEndHitPanel();
      }
      
    } else if (response["status"] == "failed") {
      displayEndHitPanel();
    }
  });
}