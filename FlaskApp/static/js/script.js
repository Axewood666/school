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
            document.getElementById('output').innerHTML = response;
        },
        error: function(error) {
            console.log(error);

        }
    });
}
