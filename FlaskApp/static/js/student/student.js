import { getClass, getGradesByFio } from '/static/js/student/requests.js';
import { toggleStudentInfo } from '/static/js/student/data-process.js';
import {print_error, clearElement} from '/static/js/script.js';
import { handleGradeFormSubmit, closeGradeForm, openGradeForm } from '/static/js/script.js';

$(function(){
    $("input#class-name").autocomplete({
        source: 'student/input-autocomplete',
        autoFocus: true,
        select: displayClass
        });
    function displayClass(event, ui){
        clearElement(output);
        const classNameJson = {
            'className': ui.item.label
        }
        getClass(classNameJson);
    }
});

function studentInfoDisplay(open = 0){
    if (open) {
        const toggleButton = document.getElementById('toggle-button');
        const studentInfo = document.getElementById('student-info');
        toggleButton.classList.add('expanded');
        studentInfo.classList.remove('student-info-toggle');
    } else {
        toggleStudentInfo();
        let output = document.getElementById("output");
        clearElement(output)
        output = document.getElementById("class-list");
        output.classList.remove('hide-table');
    }
}

function getStudent(i){
    const toggleHead = document.getElementById('toggle-head');
    studentInfoDisplay(1);
    let student=[]
    for(let j = 0; j < 5; j++){
        let cell = document.getElementById('class-list').rows[i].cells[j].innerHTML
        if(cell) student.push(cell)
        else student.push('')
    }
    document.getElementById('student-name').innerHTML = student[0];
    document.getElementById('student-mname').innerHTML = student[1];
    document.getElementById('student-lastname').innerHTML = student[2];
    document.getElementById('phone').innerHTML = student[3];
    document.getElementById('mail').innerHTML = student[4];
    const fio={
    'firstname': student[0],
    'middlename': student[1],
    'lastname': student[2]
    }
    if(getGradesByFio(fio)){
        let output = document.getElementById("class-list");
        output.classList.add('hide-table');
    }
}

function getClassList(){
    let className = document.getElementById("class-name").value;
    const regex = /^[1-9][A-Z]$/
    const regexSecond = /^[1-9][0-1][A-Z]$/
    if(regex.test(className) || regexSecond.test(className)){
        clearElement(output);
        const classNameJson = {
            'className': className
        }
        getClass(classNameJson);
    }else{
        print_error('Введите верное название класса')
    }
}

function openGradeFormWithFIO(){
    const firstname = document.getElementById('student-name').innerHTML;
    const middlename = document.getElementById('student-mname').innerHTML;
    const lastname = document.getElementById('student-lastname').innerHTML;
    const fio = lastname + ' ' + firstname + ' ' + middlename;
    const className = document.getElementById('class-name').value;
    document.getElementById('classname').value = className;
    document.getElementById('fio').value = fio;
    openGradeForm();
}

window.studentInfoDisplay = studentInfoDisplay;
window.getStudent = getStudent;
window.getClassList = getClassList;
const gradeForm = document.getElementById("grade-form");
gradeForm.addEventListener('submit', handleGradeFormSubmit);
window.openGradeFormWithFIO = openGradeFormWithFIO;
window.closeGradeForm = closeGradeForm;

