function fillFilmList() {
    fetch(`/lab7/rest-api/films/`)
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i<films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitleRus = document.createElement('td');
            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdAction = document.createElement('td');

            tdTitleRus.innerHTML = films[i].title_ru || films[i].title || '';

            if (films[i].title) {
                tdTitle.innerHTML = `<i>(${films[i].title})</i>`;
            } else {
                tdTitle.innerHTML = '';
            }

            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);
            }

            tdAction.appendChild(editButton);
            tdAction.appendChild(delButton);

            tr.appendChild(tdTitleRus);
            tr.appendChild(tdTitle);
            tr.appendChild(tdYear);
            tr.appendChild(tdAction);

            tbody.appendChild(tr);
        }
    })
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
    .then(function () {
        fillFilmList();
    });
}

function clearErrors() {
    const fields = ['title_ru-error', 'year-error', 'description-error'];
    fields.forEach(function(id) {
        const el = document.getElementById(id);
        if (el) {
            el.innerText = '';
            el.style.display = 'none';
        }
    });
}

function showModal() {
    clearErrors();
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title_ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    }

    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        // если всё ок или ошибок нет — просто выходим
        if (!errors) return;

        // сначала очищаем старые ошибки
        clearErrors();

        // title
        if (errors.title_ru) {
            let el = document.getElementById('title_ru-error');
            el.innerText = errors.title_ru;
            el.style.display = 'block';
        }

        // ошибка для года
        if (errors.year) {
            const el = document.getElementById('year-error');
            if (el) {
                el.innerText = errors.year;
                el.style.display = 'block';
            }
        }

        // description
        if (errors.description) {
            const el = document.getElementById('description-error');
            if (el) {
                el.innerText = errors.description;
                el.style.display = 'block';
            }
        }
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function(data) {
        return data.json();
    })
    .then(function(film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title_ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    });
}