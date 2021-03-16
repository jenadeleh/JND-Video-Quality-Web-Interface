import { sendMsg } from "./Connection"

export function requestVideos(pname, puid) {
    sendMsg(_data(pname, puid));    
}

function _data(pname, puid) {
    return {"action":"select_videos", "pname": pname, "puid":puid}
}
