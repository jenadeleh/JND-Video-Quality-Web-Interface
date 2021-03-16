import * as $ from 'jquery';

export function updateProgressBar(finished_num, task_num) {
    $(".task-progress").attr("aria-valuemax", task_num)
                    .css("width", 100*(finished_num/task_num) + "%")
                    .html(finished_num + "/" + task_num)
                    .css("color", "black");
}