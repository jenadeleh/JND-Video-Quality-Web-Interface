import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus"
import { setTimer } from "./Timer"
import { endExpAction } from "./DecisionAction"

export function loadVideos(videos) {
    _load_all_videos_into_dom(videos);
    _display_panel();

}

function _load_all_videos_into_dom(videos) {
    /**
     * load all videos into dom, z-index is used to make the videos overlap
     */

    // TODO: add video information into dom
    return
}

function _display_panel(){
    /**
     * after all videos are loaded, display the first video, and enable buttons
     */
    return
}