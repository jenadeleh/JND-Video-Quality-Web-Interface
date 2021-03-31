import { storeLocalData, getLocalData } from "../utils/ManageLocalData"

export function processResponse(response) {

    console.log(response)
    if (response["status"] == "successful") {

        // req_videos
        if (response["restype"] == "req_videos") {
            let videos_info = (response["data"]["videos"]);
            return videos_info;

        // req_inst_cf
        } else if (response["restype"] == "req_inst_cf") {
            let [inst, cf, q_text, panel_text, btn_text, warning_msg] = [response["data"]["instruction"], 
                                                                            response["data"]["consent_form"],
                                                                            response["data"]["question"],
                                                                            response["data"]["text_end_exp"],
                                                                            response["data"]["btn_text_end_exp"],
                                                                            response["data"]["warning_msg"]]

            return [inst, cf, q_text, panel_text, btn_text, warning_msg];

        // user_register
        } else if (response["restype"] == "user_register") {
            return response["data"]
        }

    } else if (response["status"] == "failed") {
            alert(response["data"]);
            return response["data"];
    }
}