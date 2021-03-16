import * as $ from 'jquery';
import { UpdateVideo } from "./LoadVideos"
import { storeLocalData, getLocalData } from "../utils/ManageLocalData"
import { loadVideos } from "./LoadVideos"

export function processResponse(response) {
    if (response["status"] == "successful") {
        if (response["restype"] == "select_videos") {
            storeLocalData("exp", data["exp"]);
            storeLocalData("puid", data["puid"]);
            loadVideos(response["data"]["videos"]);
        }
    } else if (response["status"] == "failed") {
        console.log(response["data"]);
    }
}