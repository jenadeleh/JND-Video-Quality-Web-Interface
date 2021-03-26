import * as $ from 'jquery';

export const sendMsg = (data) => {
    return new Promise((resolve,reject)=>{
        $.ajax({
            type: 'POST',
            url: "/scheduler",
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json', 
        }).done((response) => {
            resolve(response);
        }).fail((err) => {
            resolve(err);
        });
    });
}