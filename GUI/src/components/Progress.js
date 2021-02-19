import * as $ from 'jquery';

export function updateProgressBar(finish_num, task_num) {
    $(".task-progress").attr("aria-valuemax", task_num)
                    .css("width", 100*(finish_num/task_num) + "%")
                    .html(finish_num + "/" + task_num)
                    .css("color", "black");
}