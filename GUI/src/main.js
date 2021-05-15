import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-slider';
import 'bootstrap-slider/dist/css/bootstrap-slider.min.css';

import { initGUI } from "./components/InitGUI"
import { globalStatus } from "./components/GlobalStatus";
import { sendMsg } from "./components/SendMsg"
import { getLocalData } from "./utils/ManageLocalData"

_check_close_tab_browser();
initGUI();

function _check_close_tab_browser() {
    window.onbeforeunload = function (e) {
        e = e || window.event;
        if (e) {
            if (globalStatus.exp_status == "decision" || 
                globalStatus.exp_status == "hit_panel") {
                sendMsg({"action":"release_resource", "puid":getLocalData("puid")});
                clearTimeout(globalStatus.EXPIRE_TIMER);
                // e.returnValue = "You will lost your result if you close the tab.";
            }    
        }
    
        // Chrome, Safari, Firefox 4+, Opera 12+ , IE 9+
        if (globalStatus.exp_status == "decision" || 
            globalStatus.exp_status == "hit_panel") {
                sendMsg({"action":"release_resource", "puid":getLocalData("puid")});
                clearTimeout(globalStatus.EXPIRE_TIMER);
                // return ("You will lost your result if you close the tab.");
        }
    };
}