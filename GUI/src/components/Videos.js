import * as $ from 'jquery';
import { sendMsg } from "./Connection"
import { globalStatus } from "./GlobalStatus"
import { updateProgressBar } from "./ProgressBar"

export function displayVideos() {
    globalStatus.cur_video = globalStatus.videos.shift();
    delete globalStatus.cur_video["url"]; 
    let vuid = globalStatus.cur_video["vuid"];
    $(`#vc-${vuid}`).css("z-index", "1");
    $("#video-spinner").css("display", "none");
}

export function reqLoadVideos(pname, puid, euid) {
    let data = {"action":"req_videos", "pname": pname, "puid":puid, "euid":euid}

    sendMsg(data).then(response => {
        if (response["status"] == "successful") {
            let videos_info = response["data"]["videos"];
            globalStatus.videos = videos_info;
            _addAllVideosToDom(videos_info).then(()=>{
                globalStatus.video_num = globalStatus.videos.length;
                updateProgressBar(0, globalStatus.video_num);
                displayVideos();
                $("#start-exp-btn").attr("disabled",false);
            });
        } else if (response["status"] == "failed") {
            $(".exp-panel").css("display", "none");
            $("#msg-panel").html(response["data"]).css("display", "inline");
            clearTimeout(globalStatus.env_bg_interval);
            clearTimeout(globalStatus.FIRST_DURATION_timer);
            clearTimeout(globalStatus.SECOND_DURATION_timer);
            return response["data"];
        }
    });
}
    
function _addAllVideosToDom(videos_info) {
    return new Promise((resolve,reject)=>{
        let $video_pool = $("#video-pool");

        $video_pool.css("height", globalStatus.video_h)
                    .css("width", globalStatus.video_w);

        videos_info.forEach((ele)=>{
            let {url, vuid, side, qp} = ele;

            let v_html = `<div class="video-cover" 
                                    id=vc-${vuid}
                                    data-side=${side}
                                    data-qp=${qp}
                                    style="z-index:-1; height: ${globalStatus.video_h}px; width: ${globalStatus.video_w}px;"
                                    >
                                    <video class="vd" loop="loop" muted id=${vuid} height="${globalStatus.video_h}" width="${globalStatus.video_w}">
                                        <source src=${url} 
                                            type='video/mp4'
                                        >
                                    </video>
                        </div>`

            $(v_html).appendTo($video_pool);
        })

        resolve();
    });
}

