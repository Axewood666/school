async function addGrade(data) {
    try {
    let response = await fetch('teacher/add-grade', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    if(response.ok){
        console.log('ok');
    }else{

    }
    }catch(error){
        console.log('Ошибка: ', error);
    }
}

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

window.openGradeForm = openGradeForm;
window.closeGradeForm = closeGradeForm;
const gradeForm = document.getElementById("grade-form");
gradeForm.addEventListener('submit', handleGradeFormSubmit);
