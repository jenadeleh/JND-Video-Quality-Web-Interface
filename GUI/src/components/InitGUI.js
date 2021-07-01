import * as $ from 'jquery';
import { initDoms } from "./InitDoms"
import { req_inst_cf } from "./ConsentForm"
import { 
    checkEnvBackground, 
    isPC, 
    showWarningCover, 
    isCorrectResolution, 
    isCorrectBrowser, 
    getBrowserInfo, 
    reso_warnings 
} from "./Environment"; 

import { globalStatus } from "./GlobalStatus";
import { keyboardControl } from "./KeyboardControl";
import { initLocalData } from "./InitLocalData";
import { actionCloseTabBrowser } from "./ActionCloseTabBrowser"

export function initGUI() {
    if (!isPC()) {
        showWarningCover("mobile_device");
    } else if (!isCorrectBrowser()) {
    
        showWarningCover("correct_browser");
    } else if (!isCorrectResolution()) {
        $("#warning-cover").css("visibility", "visible");
        $("#warning-msg").html(reso_warnings());
    } else {
        checkEnvBackground();
        if (!globalStatus.isNotMaximizedBrowser) {
            // initLocalData();
            actionCloseTabBrowser();
            getBrowserInfo();
            initDoms();
            keyboardControl();
            req_inst_cf();
        }
    }
}


