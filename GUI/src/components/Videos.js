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

                console.log(this.videos_info)
                // TODO: 
                this._loadAllVideos(this.videos_info);
            }
        });
    }
    
    _loadAllVideos(videos_info) {
        let $video_pool = $("#video-pool");

        // TODO: 
        // $("#spinner-lv-panel").css("height", globalStatus.video_h)
        //                         .css("width", globalStatus.video_w);

        videos_info.forEach((ele)=>{
            let {url, vuid, side, qp} = ele;
            this.video_ids.push(vuid);

            let v_html = `<div class="video-cover" 
                                    id=${vuid} 
                                    data-side=${side}
                                    data-qp=${qp}
                                    style="z-index:-1; height: ${globalStatus.video_h}px; width: ${globalStatus.video_w}px;"
                                    >
                                    <video loop="loop" muted autoplay>
                                        <source id="video_src" 
                                                src=${url} 
                                                type='video/mp4'>
                                    </video>
                        </div>`

            
            $(v_html).appendTo($video_pool);

            // $("#spinner-lv-panel").css("z-index", "-1");
            $video_pool.css("z-index", "1");
            $("#b5e2b773-75dd-4471-8f8b-36d0594e5db1").addClass("curr-display");
        })


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