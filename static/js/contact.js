document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.floating-placeholder').forEach(function (input) {
      input.addEventListener('input', function () {
        if (input.value.trim() !== '') {
          input.classList.add('has-content');
        } else {
          input.classList.remove('has-content');
        }
      });
    });
  });