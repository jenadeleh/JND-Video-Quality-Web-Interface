import * as $ from 'jquery';
import { sendMsg } from "./Connection"
import { processResponse } from "./ProcessResponse"
import { globalStatus } from "./GlobalStatus"

export default class Videos {
    constructor() {
        this.videos_info = Object;
        this.video_ids = [];
    }

    reqLoadVideos(pname, puid) {
        let data = {"action":"req_videos", "pname": pname, "puid":puid}

        sendMsg(data).then(response => {
            let resp = processResponse(response);
            if (typeof resp=='string') {
                // TODO: display warning message
            } else if (typeof resp=='object') {
                this.videos_info = resp;
                globalStatus.videos = this.videos_info;
                this._addAllVideosToDom(this.videos_info).then(()=>{
                    this._displayVideos();
                });
            }
        });
    }

    _displayVideos() {
        globalStatus.cur_video = globalStatus.videos.shift();
        let vuid = globalStatus.cur_video["vuid"];
        $(`#vc-${vuid}`).css("z-index", "1");
        $("#video-spinner").css("display", "none");
    }
    
    _addAllVideosToDom(videos_info) {
        return new Promise((resolve,reject)=>{
            let $video_pool = $("#video-pool");
            videos_info.forEach((ele)=>{
                let {url, vuid, side, qp} = ele;
                this.video_ids.push(vuid);

                let v_html = `<div class="video-cover" 
                                        id=vc-${vuid}
                                        data-side=${side}
                                        data-qp=${qp}
                                        style="z-index:-1; height: ${globalStatus.video_h}px; width: ${globalStatus.video_w}px;"
                                        >
                                        <video class="vd" loop="loop" muted id=${vuid}>
                                            <source src=${url} 
                                                type='video/mp4'
                                            >
                                        </video>
                            </div>`

                $(v_html).appendTo($video_pool);
            })

            resolve();
        });






        // let $video_pool = $("#video-pool");
        $video_pool.css("width", globalStatus.video_w+"px")
                    .css("height", globalStatus.video_h+"px")
        return
    }

    loadImageAsync(url) {
        return new Promise(function(resolve, reject) {
          const image = new Image();
      
          image.onload = function() {
            resolve(image);
          };
      
          image.onerror = function() {
            reject(new Error('Could not load image at ' + url));
          };
      
          image.src = url;
        });
    }
}