import {print_error, clearElement} from '/static/js/script.js';
import { closeGradeForm, openGradeForm, serializeForm } from '/static/js/script.js';
import { addNewStudent} from '/static/js/staff/requests.js';
$(function(){
    $("input#class-name").autocomplete({
        source: '/student/input-autocomplete',
        autoFocus: true
        });
});

function handleAddStudentForm(){
    event.preventDefault();
    const data = serializeForm(gradeForm);
    addNewStudent(data);
    closeGradeForm();
}

const gradeForm = document.getElementById("grade-form");
gradeForm.addEventListener('submit', handleAddStudentForm);
window.openGradeForm = openGradeForm;
window.closeGradeForm = closeGradeForm;
