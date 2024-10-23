import {print_error, clearElement} from '/static/js/script.js';
import { closeGradeForm, openGradeForm, serializeForm } from '/static/js/script.js';
import { addNewStudent, addNewTeacher} from '/static/js/staff/requests.js';
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
    clearElement(document.getElementById("output"));
}

function handleAddTeacherForm(){
    event.preventDefault();
    const data = serializeForm(teacherForm);
    addNewTeacher(data);
    closeGradeForm('popup-background-teacher');
    clearElement(document.getElementById("output"));
}

const gradeForm = document.getElementById("grade-form");
gradeForm.addEventListener('submit', handleAddStudentForm);
const teacherForm = document.getElementById("teacher-add-form");
teacherForm.addEventListener('submit', handleAddTeacherForm);
window.openGradeForm = openGradeForm;
window.closeGradeForm = closeGradeForm;
