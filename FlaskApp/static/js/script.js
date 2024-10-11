function sendData() {
    var name = document.getElementById('name').value;
    var lastName = document.getElementById('lastName').value;
    var middleName = document.getElementById('middleName').value;
    $.ajax({
        url: '/process',
        type: 'POST',
        data: {
                '_name': name,
                '_lastName': lastName,
                '_middleName': middleName
        },
        success: function(response) {

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
        },
        error: function(error) {
            console.log(error);
            document.getElementById("output").innerHTML = error.responseText;
        }
    });
}
