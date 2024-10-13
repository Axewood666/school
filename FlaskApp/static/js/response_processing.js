export function subjects_response_process(result){
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

export function students_response_process(response){
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

export function grade_response_process(grades){
        const tbl = document.createElement("table");
        const tblBody = document.createElement("tbody");
        for(let i = 0; i < grades.length;i++){
            let row = document.createElement("tr");
            let cell = Add_cell(grades[i].name);
            row.appendChild(cell);
            cell = Add_cell(grades[i].subject);
            row.appendChild(cell);
            cell = Add_cell(grades[i].grade);
            row.appendChild(cell);
            cell = Add_cell(grades[i].date);
            row.appendChild(cell);
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

function Add_cell(el){
    const cell = document.createElement("td");
    let cellText = document.createTextNode(`${el}`);
    cell.appendChild(cellText);
    return cell;
}