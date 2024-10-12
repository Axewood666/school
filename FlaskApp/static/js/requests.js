function List_of_students() {
    data = fio();
    $.ajax({
        url: '/teacher/list-of-students',
        type: 'POST',
        data: data,
        success: function(response) {
            students_response_process(response);
        },
        error: function(error) {
            console.log(error);
            document.getElementById("output").innerHTML = error.responseText;
        }
    });
}

async function List_of_subjects() {
    let data = fio();

    try {
        let response = await fetch('/teacher/list-of-subjects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if(response.ok) {
            let result = await response.json();
            subjects_response_process(result.subjects);
        } else {
            document.getElementById("output").innerHTML = "Преподаватель не найден";
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

function fio(){
    let name = document.getElementById('name').value;
    let lastName = document.getElementById('lastName').value;
    let middleName = document.getElementById('middleName').value;
    return {
        '_name': name,
        '_lastName': lastName,
        '_middleName': middleName
    };
}

function subjects_response_process(result){
    const ol = document.createElement("ol");
    for(let i = 0; i < result.length; i++){
        let el = document.createElement("li")
        let aEl = document.createElement("a")
        aEl.setAttribute("href", `${result[i]}`);
        let elText = document.createTextNode(`${result[i]}`);
        aEl.appendChild(elText);
        el.appendChild(aEl);
        ol.appendChild(el);
    }
    const outputElement = document.getElementById("output");
    while (outputElement.firstChild) {
      outputElement.removeChild(outputElement.firstChild);
    }
     outputElement.appendChild(ol);
     ol.classList.add('rectangle')
}
function students_response_process(response){
            const tbl = document.createElement("table");
            const tblBody = document.createElement("tbody");
            let row = document.createElement("tr");
            for(let i = 0; i < response[0].length; i++){
                let headCell = document.createElement("th");
                let  cellText = document.createTextNode(`${response[0][i]}`);
                headCell.appendChild(cellText);
                row.appendChild(headCell);
            }
            tblBody.appendChild(row);
            for(let i = 1; i < response.length;i++){
                row = document.createElement("tr");
                for (let j = 0; j < response[i].length; j++){
                    const cell = document.createElement("td");
                    let cellText = document.createTextNode(`${response[i][j]}`);
                    cell.appendChild(cellText);
                    row.appendChild(cell);
                }
                tblBody.appendChild(row);
            }
            tbl.appendChild(tblBody);
            const outputElement = document.getElementById("output");
            while (outputElement.firstChild) {
              outputElement.removeChild(outputElement.firstChild);
            }
            outputElement.appendChild(tbl);
            tbl.setAttribute("border", "2");
}


