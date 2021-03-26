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
            let [instruction, consent_form] = [response["data"]["instruction"], 
                                            response["data"]["consent_form"]]

            return [instruction, consent_form];

        // user_register
        } else if (response["restype"] == "user_register") {
            return response["data"]
        }

    } else if (response["status"] == "failed") {
            alert(response["data"]);
            return response["data"];
    }
}