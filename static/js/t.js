// script.js

function showAnswer() {
    document.getElementById('show-answer-btn').style.display = 'none';
    document.getElementById('answer').style.display = 'block';

    var rightBtn = document.createElement('button');
    rightBtn.setAttribute('type', 'submit');
    rightBtn.setAttribute('class', 'btn btn-success mr-2');
    rightBtn.setAttribute('name', 'action');
    rightBtn.setAttribute('value', 'right');
    rightBtn.textContent = 'Right';

    var wrongBtn = document.createElement('button');
    wrongBtn.setAttribute('type', 'submit');
    wrongBtn.setAttribute('class', 'btn btn-danger');
    wrongBtn.setAttribute('name', 'action');
    wrongBtn.setAttribute('value', 'wrong');
    wrongBtn.textContent = 'Wrong';

    var form = document.querySelector('form');
    form.appendChild(rightBtn);
    form.appendChild(wrongBtn);
}
