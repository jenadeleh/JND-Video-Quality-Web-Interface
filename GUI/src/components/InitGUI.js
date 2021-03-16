import { storeLocalData, getLocalData } from "../utils/ManageLocalData"
import { displayConsentForm } from "./DisplayConsentForm"
import { requestVideos } from "./RequestVideos"
import { processResponse } from "./ProcessResponse"

export function initGUI() {
    // $("#instruction-modal").modal("show");
    

    let exp  = getLocalData("exp");
    if (exp === null) {
        storeLocalData("pname", "");
        storeLocalData("puid", "");
        storeLocalData("exp", "");
    } 

    let didConsentForm  = getLocalData("didConsentForm");
    if (didConsentForm === null) {
        storeLocalData("didConsentForm", "false");
        displayConsentForm();
    } else if (didConsentForm == "false") {
        displayConsentForm();
    } else if (didConsentForm == "true") {
        // TODO: calibration
    }

    storeLocalData("pname", "guangan"); //TODO: remove later

    let response = requestVideos(getLocalData("pname"), getLocalData("puid"));
    processResponse(response);


    // updateProgressBar(taskRecord.finish_num, taskRecord.TASK_NUM);
}