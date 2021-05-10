import * as $ from 'jquery';
import { sendMsg } from "./Connection"
import { globalStatus } from "./GlobalStatus"
import { updateProgressBar } from "./ProgressBar"
import { setTimer, setExpireTimer } from "./Timer"
import { getLocalData } from "../utils/ManageLocalData"

export function displayFirstVideo() {
    $("#video-spinner").css("display", "none").removeClass("d-flex");
    globalStatus.cur_video = globalStatus.videos.shift();
    // console.log("--- First video ---")
    // console.log(globalStatus.cur_video["source_video"])
    let cur_vuid = globalStatus.cur_video["vuid"];
    delete globalStatus.cur_video["url"];
    globalStatus.exp_status = "decision";

    $(`#${cur_vuid}`).get(0).pause();
    $(`#vc-${cur_vuid}`).css("visibility", "visible");
    $("#start-exp-btn").attr("disabled",false);
}

export function displayNextVideo() {
    // remove previous video
    let pre_vuid = globalStatus.cur_video["vuid"];
    $(`#vc-${pre_vuid}`).remove();

    // display next video
    globalStatus.cur_video = globalStatus.videos.shift();
    let cur_vuid = globalStatus.cur_video["vuid"];
    delete globalStatus.cur_video["url"];
    $(`#vc-${cur_vuid}`).css("visibility", "visible").css("z-index", 1);

    // console.log("--- next video ---")
    // console.log(globalStatus.cur_video["source_video"])
    recordTime();
}

export function recordTime() {
    globalStatus.cur_video["start_time"] = new Date().getTime();
    setTimer();
}

export function reqLoadVideos(pname, puid, euid) {
    $("#video-pool, #video-spinner").css("height", globalStatus.video_h)
                                    .css("width", globalStatus.video_w);

    let data = {"action":"req_videos", "pname": pname, "puid":puid, "euid":euid}

    sendMsg(data).then(response => {
        if (response["status"] == "successful") {
            let videos_info = response["data"]["videos"];
            globalStatus.duration = response["data"]["duration"];
            globalStatus.videos = videos_info;
            globalStatus.videos = _shuffle(globalStatus.videos)
            globalStatus.video_num = globalStatus.videos.length;
            updateProgressBar(0, globalStatus.video_num);
            $("#loading-progress").html(globalStatus.loaded_video_num+ "/" +globalStatus.video_num);
            _addAllVideosToDom();
        } else if (response["status"] == "failed") {
            $(".exp-panel").css("display", "none");
            $("#msg-panel").html(response["data"]).css("display", "inline");
            clearTimeout(globalStatus.env_bg_interval);
            clearTimeout(globalStatus.FIRST_DURATION_TIMER);
            clearTimeout(globalStatus.SECOND_DURATION_TIMER);
            return response["data"];
        }
    });
}

    
function _addAllVideosToDom() {
    const tasks = Array.from(globalStatus.videos, (video_info) => _loadVideoAsync(video_info));
    Promise.all(tasks).then(() => {
        sendMsg({"action":"resource_monitor", 
                "pname": getLocalData("pname"), 
                "puid":getLocalData("puid"), 
                "euid":getLocalData("euid")}
        ).then(response => {
            if (response["status"] == "successful") {
                displayFirstVideo();
                globalStatus.start_time = response["data"]["start_date"];
                globalStatus.expire_msg = response["data"]["expire_msg"];
                setExpireTimer();
            } else if (response["status"] == "failed") {
                console.log("Error: _addAllVideosToDom")
            }
        }); 
    });
}

function _loadVideoAsync(video_info) {
    return new Promise(function(resolve, reject) {
        let $video_pool = $("#video-pool");
        let {url, vuid, side, qp, source_video} = video_info
        // console.log(url)
        let req = new XMLHttpRequest();
        req.open('GET', url, true);
        req.responseType = 'blob';
        req.onload = function() {
            if (this.status === 200) {
                let videoBlob = this.response;
                let v_l_url = URL.createObjectURL(videoBlob);

                let v_html = `<div class="video-cover"
                                id=vc-${vuid}
                                data-side=${side}
                                data-qp=${qp}
                                data-src-video=${source_video}
                                style="z-index:-1; height: ${globalStatus.video_h}px; width: ${globalStatus.video_w}px; visibility:hidden;"
                                >
                                <video class="vd" loop="loop" autoplay muted id=${vuid} height="${globalStatus.video_h}" width="${globalStatus.video_w}">
                                    <source src=${v_l_url} 
                                        type='video/mp4'
                                    >
                                </video>
                        </div>`
                $(v_html).appendTo($video_pool);

                globalStatus.loaded_video_num += 1;

                
                $("#loading-progress").html(globalStatus.loaded_video_num+ "/" +globalStatus.video_num);
                resolve();
            }
        }
        req.onerror = function() {}
        req.send();
    });
}

function _shuffle(arr) {
    for (let i = 1; i < arr.length; i++) {
        const random = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[random]] = [arr[random], arr[i]];
    }
    return arr
}
