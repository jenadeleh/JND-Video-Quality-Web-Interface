import * as $ from 'jquery';

export function updateProgressBar(cnt, total) {
    let pct = 100*(cnt/total);
    $("#task-progressbar").attr("aria-valuemax", total)
                    .attr("aria-valuenow", `${cnt}`)
                    .css("width",  `${pct}%`)
                    .html(`${cnt}/${total}`);
}