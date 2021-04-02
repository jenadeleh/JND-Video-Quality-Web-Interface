import * as $ from 'jquery';
import { initDoms } from "./InitDoms"
import { req_inst_cf } from "./ConsentForm"

export function initGUI() {
    initDoms();
    req_inst_cf();
}
