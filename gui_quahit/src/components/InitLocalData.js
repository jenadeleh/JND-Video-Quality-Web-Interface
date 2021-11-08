import { storeLocalData, getLocalData } from "../utils/ManageLocalData"

export function initLocalData() {
    // TODO: replace local data
    if (getLocalData("jnd_video_data") === null) {
        storeLocalData("jnd_video_data", 
                        JSON.stringify({
                            "availHeight":"",
                            "devicePixelRatio":"",
                            "cali_time":"",
                            "browser_width_cm":"",
                            "availWidth":"",
                            "hasCalibrated":"",
                            "px_cm_rate":"",
                            "pname":"",
                            "outerWidth":"",
                            "outerHeight":"",
                            "euid":"",
                            "browser_height_cm":"",
                            "puid":"",
                        })
        )
    }
}
