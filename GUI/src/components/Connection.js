import * as $ from 'jquery';

export function sendMsg(data) {
    $.ajax({
        type: 'POST',
        url: "/scheduler",
        data: JSON.stringify(data), 
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json', 
    }).done((response) => {
        return response;
    });
}