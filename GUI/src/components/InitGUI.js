import * as $ from 'jquery';
import { initDoms } from "./InitDoms"
import { req_inst_cf } from "./ConsentForm"
import { checkEnvBackground, isPC, showWarningCover, isCorrectResolution, getBrowserInfo, reso_warnings } from "./Environment"; 
import { globalStatus } from "./GlobalStatus";

export function initGUI() {
    if (!isPC()) {
        showWarningCover("mobile_device");
    } else if (!isCorrectResolution()) {
        $("#warning-cover").css("visibility", "visible");
        $("#warning-msg").html(reso_warnings());
    } else {
        checkEnvBackground();
        if (!globalStatus.isNotMaximizedBrowser) {
            getBrowserInfo();
            initDoms();
            req_inst_cf();
        }
    }
}
