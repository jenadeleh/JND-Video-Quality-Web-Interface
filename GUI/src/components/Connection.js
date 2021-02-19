import * as $ from 'jquery';
import { UpdateVideo } from "./UpdateVideo"

export function SendMsg(data) {
    $.ajax({
        type: 'POST',
        url: "/scheduler",
        data: JSON.stringify(data), 
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json', 
    }).done((response) => {
        console.log(JSON.stringify(response));
        responseAction(response)
    });
}

function responseAction(response) {
    // TODO:
    UpdateVideo(response["url"])
}