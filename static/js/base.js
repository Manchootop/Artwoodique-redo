// Get all close buttons by class name
var closeButtons = document.getElementsByClassName('close');

// Add click event listeners to close buttons
document.addEventListener('DOMContentLoaded', function () {
    var closeButtons = document.querySelectorAll('.close');

    closeButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var message = this.parentElement;
            if (message.style.display === 'none' || message.style.display === '') {
                message.style.display = 'flex';
            } else {
                message.style.display = 'none';
            }
        });
    });

    // Show messages with class 'alert' by setting display to 'flex'
    var alertMessages = document.querySelectorAll('.custom-message .alert');
    alertMessages.forEach(function (message) {
        message.style.display = 'flex';
    });
});
