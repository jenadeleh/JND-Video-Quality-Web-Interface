import * as $ from 'jquery';
import { sendMsg } from "./Connection"
import { globalStatus } from "./GlobalStatus"
import { updateProgressBar } from "./ProgressBar"
import { setTimer } from "./Timer"

export function displayVideos(mode) {
    // mode : new_hit/next_video
    globalStatus.cur_video = globalStatus.videos.shift();
    delete globalStatus.cur_video["url"]; 
    let vuid = globalStatus.cur_video["vuid"];
    $(`#vc-${vuid}`).css("z-index", "1");
    $("#video-spinner").css("display", "none");
    $("#start-exp-btn").attr("disabled",false); 

    //TODO: check
    // let cur_v_dom = $(document.getElementById(vuid));
    // let v_dur = cur_v_dom.duration;
    // console.log(cur_v_dom)

    // let video_load_interval = setInterval(()=> {
    //     let percent = cur_v_dom.currentTime/v_dur;
    //     if (percent > 0.90) {
    //         $(`#vc-${vuid}`).css("z-index", "1");
    //         $("#video-spinner").css("display", "none");
    //         if (mode=="new_hit") {
    //             $("#start-exp-btn").attr("disabled",false); 
    //         } else if (mode=="next_video") {
    //             playCurVideo();
    //         }
    //         clearInterval(video_load_interval);
    //     }

    //     // cur_v_dom.currentTime++;
    //     // cur_v_dom.duration, cur_v_dom.currentTime, 
    //     console.log(percent)
    // },500);
}

export function reqLoadVideos(pname, puid, euid) {
    let data = {"action":"req_videos", "pname": pname, "puid":puid, "euid":euid}

    sendMsg(data).then(response => {
        if (response["status"] == "successful") {
            let videos_info = response["data"]["videos"];
            globalStatus.videos = videos_info;
            globalStatus.video_num = globalStatus.videos.length;
            updateProgressBar(0, globalStatus.video_num);
            _addAllVideosToDom(videos_info).then((last_vid)=>{
                //TODO:
                // let vuid = last_vid;
                // let cur_v_dom = document.getElementById(vuid);
                // let v_dur = cur_v_dom.duration;
                // let mode="new_hit";
                // console.log(cur_v_dom, vuid)

                // let video_load_interval = setInterval(()=> {

                //     console.log(cur_v_dom.currentTime, cur_v_dom.duration)
                //     let percent = cur_v_dom.currentTime/cur_v_dom.duration;
                //     if (percent > 0.90) {
                //         $(`#vc-${vuid}`).css("z-index", "1");
                //         $("#video-spinner").css("display", "none");
                //         if (mode=="new_hit") {
                //             $("#start-exp-btn").attr("disabled",false); 
                //         } else if (mode=="next_video") {
                //             playCurVideo();
                //         }
                //         clearInterval(video_load_interval);
                //     }

                //     // cur_v_dom.currentTime++;
                //     // cur_v_dom.duration, cur_v_dom.currentTime, 
                //     console.log(percent)
                // },500);

                displayVideos("new_hit");
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

export function playCurVideo() {
    const promise = new Promise(function(resolve, reject) {
        let vuid = globalStatus.cur_video["vuid"];
        $(`#${vuid}`).get(0).play();
        resolve();
    });

    promise.then(function () {
        globalStatus.cur_video["start_time"] = new Date().getTime();
        globalStatus.exp_status = "decision";
        setTimer();
    });
}
    
function _addAllVideosToDom(videos_info) {
    return new Promise((resolve,reject)=>{
        let $video_pool = $("#video-pool");

        $video_pool.css("height", globalStatus.video_h)
                    .css("width", globalStatus.video_w);


        let last_vid = "";

        let video_list = ["videoSRC001_640x480_30_qp_00_01_L.mp4",  
                            "videoSRC015_640x480_30_qp_00_01_L.mp4",  
                            "videoSRC089_640x480_30_qp_00_01_L.mp4",
                            "videoSRC006_640x480_30_qp_00_01_L.mp4",  
                            "videoSRC074_640x480_30_qp_00_01_L.mp4"]


                        
                        
        videos_info.forEach((ele)=>{
            let {url, vuid, side, qp} = ele;
            last_vid = vuid;

            let v_l_url = null;

            let url_ = "https://jnd.mmsp-kn.de/static/videos/" + video_list.shift();

            let req = new XMLHttpRequest();
            req.open('GET', url_, true);
            req.responseType = 'blob';
            req.onload = function() {
                if (this.status === 200) {
                    let videoBlob = this.response;
                    v_l_url = URL.createObjectURL(videoBlob); // IE10+

                    console.log(v_l_url)

                    let v_html = `<div class="video-cover" 
                                    id=vc-${vuid}
                                    data-side=${side}
                                    data-qp=${qp}
                                    style="z-index:-1; height: ${globalStatus.video_h}px; width: ${globalStatus.video_w}px;"
                                    >
                                    <video class="vd" loop="loop" controls autoplay muted id=${vuid} height="${globalStatus.video_h}" width="${globalStatus.video_w}">
                                        <source src=${v_l_url} 
                                            type='video/mp4'
                                        >
                                    </video>
                            </div>`

                $(v_html).appendTo($video_pool);
                }
            }
            req.onerror = function() {}
            
            req.send();




            // let v_html = `<div class="video-cover" 
            //                     id=vc-${vuid}
            //                     data-side=${side}
            //                     data-qp=${qp}
            //                     style="z-index:-1; height: ${globalStatus.video_h}px; width: ${globalStatus.video_w}px;"
            //                     >
            //                     <video class="vd" loop="loop" controls autoplay muted id=${vuid} height="${globalStatus.video_h}" width="${globalStatus.video_w}">
            //                         <source src=${v_l_url} 
            //                             type='video/mp4'
            //                         >
            //                     </video>
            //             </div>`

            // $(v_html).appendTo($video_pool);
        })  
        
         
        resolve(last_vid);
    });
}


