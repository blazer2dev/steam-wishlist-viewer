document.getElementById('submit_form').addEventListener('submit', function (event) {
    var input = document.getElementsByName('steamid_input')[0].value;

    if (input === '') {
        event.preventDefault();
        document.getElementById('error_log').textContent = 'Error! Incorrect data!';
    }
});