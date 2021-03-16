import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus"
import { setTimer } from "./Timer"
import { endExpAction } from "./ProcessDecision"
import { displayView } from "./DisplayVideo"

export function loadVideos(videos) {
    _load_all_videos_into_dom(videos);
    displayVideo();
}

function _load_all_videos_into_dom(videos) {
    /**
     * load all videos into dom, z-index is used to make the videos overlap
     */

    // TODO: add video information into dom
    return
}


