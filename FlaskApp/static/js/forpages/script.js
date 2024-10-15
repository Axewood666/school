import { addGrade } from '/static/js/requests.js';

function serializeForm(formNode){
    const { elements } = formNode;
    const data = Array.from(elements)
    .filter(item => !!item.name)
    .reduce((arr, el) => {
        const {name, value} = el;
        arr[name] = value
        return arr;
    }, {});
    return data;
}

function openGradeForm(){
    document.getElementById("popup-background").style.display = "flex";
}
function closeGradeForm(){
    event.preventDefault();
    document.getElementById("popup-background").style.display = "none";
}

function handleGradeFormSubmit(event){
    event.preventDefault();
    document.getElementById("popup-background").style.display = "none";
    const data = serializeForm(gradeForm);
    addGrade(data);
}


const gradeForm = document.getElementById("grade-form");
gradeForm.addEventListener('submit', handleGradeFormSubmit);
window.openGradeForm = openGradeForm;
window.closeGradeForm = closeGradeForm;
