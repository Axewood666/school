import {print_error, clearElement, Add_cell} from '/static/js/script.js';

export async function addNewStudent(student){
    try {
    let response = await fetch('/profile/staff/add-new-student', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(student)
    });
    if(response.ok){
        let result = await response.json();
        console.log(result.response);
    }else{
        print_error(JSON.parse(error.responseText)[0].error)
    }
    }catch(error){
        console.log('Ошибка: ', error);
    }
}