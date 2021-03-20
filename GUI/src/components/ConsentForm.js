import * as $ from 'jquery';
import { sendMsg } from "./Connection"

export default class ConsentForm {
    constructor() {}
    
    req_ins_consent_f() {
        let data = {"action":"req_inst_cf"};
        return sendMsg(data);    
    }

    render_instruction(instruction) {
        $(".instruction-content").html(instruction);
        // $("#instruction-modal").css("display", "inline");
        // $("#instruction-modal").modal("show");
    }
    
    render_consent_form(consent_form) {
        $("#cf-content").html(consent_form); 
        $("#cf-panel").css("display", "inline")
    }

    submitCfResult(pname, pemail) {
        let data = {"action":"user_register", "pname":pname, "pemail":pemail};
        return sendMsg(data);    
    }
}

