from lab5 import db_connect, db_close

from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime
import sqlite3

lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


# начальные данные – только для первичного заполнения БД
initial_films = [
    {
        'title': 'The Wolf of Wall Street',
        'title_ru': 'Волк с Уолл-стрит',
        'year': 2013,
        'description': '1987 год. Джордан Белфорт \
        становится брокером в успешном инвестиционном банке. \
        Вскоре банк закрывается после внезапного обвала \
        индекса Доу-Джонса. По совету жены Терезы Джордан \
        устраивается в небольшое заведение, занимающееся \
        мелкими акциями. Его настойчивый стиль общения с \
        клиентами и врождённая харизма быстро даёт свои плоды. \
        Он знакомится с соседом по дому Донни, торговцем, \
        который сразу находит общий язык с Джорданом и решает \
        открыть с ним собственную фирму. В качестве сотрудников \
        они нанимают нескольких друзей Белфорта, его отца \
        Макса и называют компанию «Стрэттон Оукмонт». \
        В свободное от работы время Джордан прожигает \
        жизнь: лавирует от одной вечеринки к другой, \
        вступает в сексуальные отношения с проститутками, \
        употребляет множество наркотических препаратов, \
        в том числе кокаин и кваалюд.'
    },
    {
        'title': 'Interstellar',
        'title_ru': 'Интерстеллар',
        'year': 2014,
        'description': 'Когда засуха, пыльные бури и вымирание \
        растений приводят человечество к продовольственному \
        кризису, коллектив исследователей и учёных отправляется \
        сквозь червоточину (которая предположительно соединяет \
        области пространства-времени через большое расстояние) в \
        путешествие, чтобы превзойти прежние ограничения для \
        космических путешествий человека и найти планету с \
        подходящими для человечества условиями.'
    },
    {
        'title': 'Oppenheimer',
        'title_ru': 'Оппенгеймер ',
        'year': 2023,
        'description': 'История жизни американского \
        физика-теоретика Роберта Оппенгеймера, который во времена \
        Второй мировой войны руководил Манхэттенским проектом — \
        секретными разработками ядерного оружия.'
    },
    {
        'title': 'The Gentlemen',
        'title_ru': 'Джентельмены',
        'year': 2019,
        'description': 'Один ушлый американец ещё со студенческих \
        лет приторговывал наркотиками, а теперь придумал схему \
        нелегального обогащения с использованием поместий обедневшей \
        английской аристократии и очень неплохо на этом разбогател. \
        Другой пронырливый журналист приходит к Рэю, правой руке американца, \
        и предлагает тому купить киносценарий, в котором подробно описаны \
        преступления его босса при участии других представителей \
        лондонского криминального мира — партнёра-еврея, китайской \
        диаспоры, чернокожих спортсменов и даже русского олигарха.'
    },
    {
        'title': 'Green Book',
        'title_ru': 'Зеленая книга',
        'year': 2018,
        'description': '1960-е годы. После закрытия нью-йоркского ночного клуба \
        на ремонт вышибала Тони по прозвищу Болтун ищет подработку на пару \
        месяцев. Как раз в это время Дон Ширли — утонченный светский лев, \
        богатый и талантливый чернокожий музыкант, исполняющий классическую \
        музыку — собирается в турне по южным штатам, где ещё сильны расистские \
        убеждения и царит сегрегация. Он нанимает Тони в качестве водителя, \
        телохранителя и человека, способного решать текущие проблемы. \
        У этих двоих так мало общего, и эта поездка навсегда изменит жизнь обоих.'
    }
]


def init_films_table():
    """Создаём таблицу films и заполняем её начальными данными, если она пустая."""
    conn, cur = db_connect()
    try:
        use_sqlite = isinstance(conn, sqlite3.Connection)

        if use_sqlite:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS films (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    title_ru TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    description TEXT NOT NULL
                )
            ''')
        else:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS films (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    title_ru TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    description TEXT NOT NULL
                )
            ''')

        # Проверяем, есть ли данные в таблице
        cur.execute('SELECT COUNT(*) AS cnt FROM films')
        row = cur.fetchone()
        count = row['cnt']

        if count == 0:
            # заполним начальными фильмами
            for f in initial_films:
                if use_sqlite:
                    cur.execute(
                        'INSERT INTO films (title, title_ru, year, description) '
                        'VALUES (?, ?, ?, ?)',
                        (f['title'], f['title_ru'], f['year'], f['description'])
                    )
                else:
                    cur.execute(
                        'INSERT INTO films (title, title_ru, year, description) '
                        'VALUES (%s, %s, %s, %s)',
                        (f['title'], f['title_ru'], f['year'], f['description'])
                    )

        conn.commit()
    finally:
        db_close(conn, cur)


# Flask один раз, при подключении blueprint'а, вызовет init_films_table()
@lab7.record_once
def init(state):
    with state.app.app_context():
        init_films_table()


def row_to_film(row):
    """Преобразование строки БД в словарь фильма."""
    # и для RealDictRow/dict, и для sqlite3.Row, и для обычного кортежа
    if isinstance(row, dict) or hasattr(row, 'keys'):
        return {
            'id': row['id'],
            'title': row['title'],
            'title_ru': row['title_ru'],
            'year': row['year'],
            'description': row['description'],
        }
    else:
        return {
            'id': row[0],
            'title': row[1],
            'title_ru': row[2],
            'year': row[3],
            'description': row[4],
        }


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    try:
        cur.execute('SELECT id, title, title_ru, year, description FROM films ORDER BY id')
        rows = cur.fetchall()
    finally:
        db_close(conn, cur)
    return jsonify([row_to_film(r) for r in rows])


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    use_sqlite = isinstance(conn, sqlite3.Connection)
    ph = '?' if use_sqlite else '%s'
    try:
        cur.execute(
            f'SELECT id, title, title_ru, year, description FROM films WHERE id = {ph}',
            (id,)
        )
        row = cur.fetchone()
    finally:
        db_close(conn, cur)

    if row is None:
        abort(404)

    return row_to_film(row)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    use_sqlite = isinstance(conn, sqlite3.Connection)
    ph = '?' if use_sqlite else '%s'
    try:
        cur.execute(f'DELETE FROM films WHERE id = {ph}', (id,))
        deleted = cur.rowcount
        conn.commit()
    finally:
        db_close(conn, cur)

    if deleted == 0:
        abort(404)

    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()

    # русское название обязательно
    if film.get('title_ru', '').strip() == '':
        return {'title_ru': 'Заполните русское название'}, 400

    # автозаполнение оригинального названия
    if film.get('title', '').strip() == '':
        film['title'] = film['title_ru']

    # проверка года
    year = int(film.get('year', ''))
    current_year = datetime.now().year
    if year < 1895 or year > current_year:
        return {'year': f'Год должен быть от 1895 до {current_year}'}, 400

    # проверка описания
    description = film.get('description', '').strip()
    if description == '':
        return {'description': 'Заполните описание'}, 400
    if len(description) > 2000:
        return {'description': 'Описание не должно превышать 2000 символов'}, 400

    conn, cur = db_connect()
    use_sqlite = isinstance(conn, sqlite3.Connection)
    ph = '?' if use_sqlite else '%s'
    try:
        cur.execute(
            f'UPDATE films SET title = {ph}, title_ru = {ph}, year = {ph}, description = {ph} '
            f'WHERE id = {ph}',
            (film['title'], film['title_ru'], year, description, id)
        )
        updated = cur.rowcount
        conn.commit()
    finally:
        db_close(conn, cur)

    if updated == 0:
        abort(404)

    film['id'] = id
    film['year'] = year
    film['description'] = description
    return film, 200


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    # русское название обязательно
    if film.get('title_ru', '').strip() == '':
        return {'title_ru': 'Заполните русское название'}, 400

    # автозаполнение оригинального названия
    if film.get('title', '').strip() == '':
        film['title'] = film['title_ru']

    # проверка года
    year = int(film.get('year', ''))
    current_year = datetime.now().year
    if year < 1895 or year > current_year:
        return {'year': f'Год должен быть от 1895 до {current_year}'}, 400

    # проверка описания
    description = film.get('description', '').strip()
    if description == '':
        return {'description': 'Заполните описание'}, 400
    if len(description) > 2000:
        return {'description': 'Описание не должно превышать 2000 символов'}, 400

    conn, cur = db_connect()
    use_sqlite = isinstance(conn, sqlite3.Connection)
    try:
        if use_sqlite:
            # SQLite
            cur.execute(
                'INSERT INTO films (title, title_ru, year, description) '
                'VALUES (?, ?, ?, ?)',
                (film['title'], film['title_ru'], year, description)
            )
            new_id = cur.lastrowid
        else:
            # Postgres – используем RETURNING id
            cur.execute(
                'INSERT INTO films (title, title_ru, year, description) '
                'VALUES (%s, %s, %s, %s) RETURNING id',
                (film['title'], film['title_ru'], year, description)
            )
            row = cur.fetchone()
            new_id = row['id']

        conn.commit()
    finally:
        db_close(conn, cur)

    film['id'] = new_id
    film['year'] = year
    film['description'] = description

    return {"id": new_id, "film": film}, 201
