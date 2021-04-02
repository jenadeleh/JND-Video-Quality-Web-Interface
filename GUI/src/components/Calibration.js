import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus"
import { getLocalData } from "../utils/ManageLocalData"
import { reqLoadVideos } from "./Videos"

export function calibration() {
    $("#cf-panel").css("display", "none");
    $("#hit-panel").css("display", "inline"); 

    $("#video-spinner, #video-pool").css("height", globalStatus.video_h)
                                    .css("width", globalStatus.video_w);

    // request and load videos
    reqLoadVideos(getLocalData("pname"), getLocalData("puid"));
}
