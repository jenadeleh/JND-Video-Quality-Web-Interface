import * as $ from 'jquery';
import { config } from "./Configuration";

export const sendMsg = (data) => {
    return new Promise((resolve,reject)=>{
        $.ajax({
            type: 'POST',
            url: config.SERVER_URL,
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json', 
        }).done((response) => {
            // console.log(response)
            resolve(response);
        }).fail((err) => {
            resolve(err);
        });
    });
}