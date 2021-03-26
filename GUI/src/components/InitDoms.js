import * as $ from 'jquery';
import { globalStatus } from "./GlobalStatus"
import { actStartExpBtn, actDecisionBtn, actNextExpBtn} from "./BtnActions"

export function initDoms() {
    $('#start-exp-btn').on('click', ()=> {
        actStartExpBtn();
    });
    
    $('.decision-btn').on('click',(e)=> {
        actDecisionBtn(e);
    });

    $('#next-exp-btn').on('click', ()=> {
        actNextExpBtn();
    });
}

