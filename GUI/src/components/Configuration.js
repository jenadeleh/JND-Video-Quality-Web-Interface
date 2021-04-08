import { globalStatus } from "./GlobalStatus";

export const config = {
    WARNING_MESSAGE: {
        "incorrect_cali": `<span style="color:#BA4A00;font-size:20pt">Your monitor's size is detected as small. Please use a bank card , and do the calibration again, or switch to a larger monitor. Thank you for your cooperation.</span>`,
        "mobile_device": "Mobile Device is not suitable for this work, please use PC, otherwise your work will be rejected.",
        "maximize_browser": "Please maximize your browser.",
        "same_monitor": "Please use the same monitor.",
        "scale_browser": "Please don't change the browser zoom level. You can set it back from browser menu, or using the CMD/CTRL and +/- key combination, or using CMD/CTRL and mouse scroll combination. Thank you.",
    },
    FIRST_DURATION: 5000,
    SECOND_DURATION: 3000,
    MONITOR_MIN_HEIGHT: 17,  // cm
    IMAGE_WIDTH_CM: 13.797, 
    IMAGE_HEIGHT_CM: 10.347, 
    DISTANCE: 30,
    ENV_MIN_W: 1360,
    ENV_MIN_H: 760,
};