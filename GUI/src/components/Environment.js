import * as $ from 'jquery';
import { getLocalData } from "../utils/ManageLocalData";
import { config } from "./Configuration"; 
import { globalStatus } from "./GlobalStatus";

export function _envCheck() {
    // check it is a maximized browser or not 
    if(
        screen.availWidth - window.outerWidth > 100 || 
        screen.availHeight - window.outerHeight > 100
    ) {
        showWarningCover("maximize_browser");
        globalStatus.isMaximizedBrowser = false;
    } else {
        globalStatus.isMaximizedBrowser = true;
    }

    // check it is the same monitor during the experiment or not 
    if (
        getLocalData("hasCalibrated") == "true"
    ) {
        if (
            screen.availWidth != getLocalData("availWidth") || 
            screen.availHeight != getLocalData("availHeight")
        ) {
            showWarningCover("same_monitor");
            globalStatus.isTheSameBrowser = false;
        } else {
            globalStatus.isTheSameBrowser = true;
        }
    } 

    // check the browser is zoomed or not

    let devicePixelRatio = getLocalData("devicePixelRatio")
    if (
        getLocalData("hasCalibrated")=="true" && 
        devicePixelRatio!=0
    ) {
        if (window.devicePixelRatio != devicePixelRatio) {
            showWarningCover("scale_browser");
            globalStatus.isNotZoomedBrowser = false;
        } else {
            globalStatus.isNotZoomedBrowser = true;
        }
    } 

    globalStatus.isCorrectEnv = globalStatus.isMaximizedBrowser && globalStatus.isTheSameBrowser && globalStatus.isNotZoomedBrowser;
    
    if (globalStatus.isCorrectEnv) {
        _hideWarningCover();
    }
}

export function checkEnvBackground() {
    globalStatus.env_bg_interval = setInterval(()=> _envCheck(),1000); 
}

export function getBrowserInfo() {
    let targeted_key = ["platform", "devicePixelRatio", "cookieEnabled", "language", "userAgent", "vendor"];
    for (let key in window.navigator) {
        if (!$.isFunction(window.navigator[key]) && typeof window.navigator[key] != 'object') {
            if (targeted_key.includes(key)) {
                globalStatus.os_info[key] = window.navigator[key];
            }
        }
    }  

    globalStatus.os_info["screen_resolution_w"] = screen.width;
    globalStatus.os_info["screen_resolution_h"] = screen.height;
    globalStatus.os_info["devicePixelRatio"] = window.devicePixelRatio;
    globalStatus.os_info["TimeZone"] = (-new Date().getTimezoneOffset()/60);
}

export function isPC() {
    // filter mobile devices
    let userAgentInfo = navigator.userAgent.toLowerCase();
    let Agents = ["android", "iphone", "symbianos", "windows phone", "ipad", "ipod"];
    for (let v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) >= 0) {
            showWarningCover("mobile_device");
            return false;
        }
    }
    return true;
}

export function isCorrectResolution() {
    if (screen.width < config.ENV_MIN_W || screen.height < config.ENV_MIN_H) {
        return false
    } 
    return true;
}

export function reso_warnings() {
    return `Your monitor resolution (${screen.height}x${screen.height}) does not fulfill the requirement. 
    The correct resolution should be width>=1366 and height>=768.`;
}

export function showWarningCover(message) {
    $("#warning-cover").css("visibility", "visible");
    $("#warning-msg").html(config.WARNING_MESSAGE[message]);
}
    
function _hideWarningCover() {
    $("#warning-cover").css("visibility", "hidden");
    $("#warning-msg").html();
}