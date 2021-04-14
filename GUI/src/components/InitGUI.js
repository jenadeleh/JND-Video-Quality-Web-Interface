import * as $ from 'jquery';
import { initDoms } from "./InitDoms"
import { req_inst_cf } from "./ConsentForm"
import { checkEnvBackground, isPC, showWarningCover, isCorrectResolution, getBrowserInfo, reso_warnings } from "./Environment"; 
import { globalStatus } from "./GlobalStatus";
import { keyboardControl } from "./KeyboardControl";
import { initLocalData } from "./InitLocalData";

export function initGUI() {
    if (!isPC()) {
        showWarningCover("mobile_device");
    } else if (!isCorrectResolution()) {
        $("#warning-cover").css("visibility", "visible");
        $("#warning-msg").html(reso_warnings());
    } else {
        // initLocalData();
        checkEnvBackground();
        if (!globalStatus.isNotMaximizedBrowser) {
            getBrowserInfo();
            initDoms();
            keyboardControl();
            req_inst_cf();
        }
    }
}
