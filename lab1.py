from flask import Blueprint, url_for, request, redirect, Response, abort
import datetime
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }


@lab1.route('/lab1/author')
def author():
    name = 'Ильин Глеб Дмитриевич'
    group = 'ФБИ-32'
    faculty = 'ФБ'

    return '''<!doctype html>
        <html>
           <body>
               <p>Студент: ''' + name + '''</p>
               <p>Группа: ''' + group + '''</p>
               <p>Факультет: ''' + faculty + '''</p>
               <a href="/lab1/web">web</a>
           </body>
        </html>'''


@lab1.route('/lab1/image')
def image():
    path = url_for('static', filename='дуб.jpg')
    css = url_for('static', filename='lab1.css')

    html = f'''<!doctype html>
        <html>
            <head>
                <meta charset="utf-8">
                <link rel="stylesheet" href="{css}">
                <title>Дуб</title>
            </head>
            <body>
                <h1>Дуб</h1>
                <img src="{path}">
            </body>
        </html>'''

    # создаём объект ответа
    response = Response(html)

    # стандартный заголовок Content-Language
    response.headers['Content-Language'] = 'ru'

    # два произвольных (нестандартных) заголовка
    response.headers['X-Developer'] = 'Gleb Ilin'
    response.headers['X-Lab-Work'] = 'Lab1'

    return response

count = 0


@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''<!doctype html>
        <html>
           <body>
               Сколько раз вы сюда заходили: ''' + str(count) + '''<br>
               <a href="/lab1/cleencounter">Очистка счётчика</a>
               <hr>
               Дата и время: ''' + str(time) + '''<br>
               Запрошенный адрес: ''' + url + '''<br>
               Ваш IP-адрес: ''' + client_ip + '''<br>
           </body>
        </html>'''


@lab1.route('/lab1/cleencounter')
def cleencounter():
    global count
    count = 0
    return '''<!doctype html>
        <html>
           <body>
               Счётчик очищен! <br>
               Сколько раз вы сюда заходили: ''' + str(count) + '''<br>
               <a href="/lab1/counter">Вернуться на счётчик</a>
           </body>
        </html>'''


@lab1.route('/lab1/info')
def info():
    return redirect('/lab1/author')


@lab1.route('/lab1/created')
def created():
    return '''<!doctype html>
        <html>
           <body>
               <h1>Создано успешно</h1>
               <div><i>что-то создано...</i></div>
           </body>
        </html>''', 201


@lab1.route('/404')
def error404():
    dog = url_for('static', filename='404.jpg')
    return '''<!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Страница не найдена</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f9fafc;
                    color: #333;
                    text-align: center;
                    padding: 50px;
                }
                h1 {
                    font-size: 48px;
                    margin-bottom: 20px;
                    color: #d9534f;
                }
                p {
                    font-size: 20px;
                    margin-bottom: 30px;
                }
                a {
                    color: #0275d8;
                    text-decoration: none;
                    font-weight: bold;
                }
                a:hover {
                    text-decoration: underline;
                }
                img {
                    width: 250px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>404 — Ой! Страница потерялась...</h1>
            <p>Похоже, такой страницы у нас нет.<br>
               Но вы всегда можете вернуться <a href="/">на главную</a>.
            </p>
            <br>
            <img src="''' + dog + '''" alt="404 dog">
        </body>
    </html>
    ''', 404


@lab1.route('/lab1')
def lab():
    return '''<!doctype html>
        <html>
            <head>
                <title>Лабораторная 1</title>
            </head>
            <body>
                <p>
                    Flask — фреймворк для создания веб-приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков — минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </p>
                <a href="/">Корень сайта</a>
                <h2>Список роутов</h2>
                <ul>
                    <li><a href="/">Главное меню</a></li>
                    <li><a href="/index">Главное меню</a></li>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab1/web">Страница с кодом html</a></li>
                    <li><a href="/lab1/author">Автор</a></li>
                    <li><a href="/lab1/image">Страница с картинкой</a></li>
                    <li><a href="/lab1/counter">Счётчик</a></li>
                    <li><a href="/lab1/cleencounter">Очистка счётчика</a></li>
                    <li><a href="/lab1/info">Info (redirect)</a></li>
                    <li><a href="/lab1/created">Создано (201)</a></li>
                    <li><a href="/400">Ошибка 400</a></li>
                    <li><a href="/401">Ошибка 401</a></li>
                    <li><a href="/402">Ошибка 402</a></li>
                    <li><a href="/403">Ошибка 403</a></li>
                    <li><a href="/404">Ошибка 404</a></li>
                    <li><a href="/405">Ошибка 405</a></li>
                    <li><a href="/418">Ошибка 418</a></li>
                    <li><a href="/error">Искусственная ошибка (500) (/error)</a></li>
                </ul>
            </body>
        </html>'''


@lab1.route('/400')
def error400():
    return "<h1>400 Bad Request</h1><p>Запрос не может быть понят сервером из-за некорректного синтаксиса.</p>", 400


@lab1.route('/401')
def error401():
    return "<h1>401 Unauthorized</h1><p>Для доступа требуется аутентификация.</p>", 401


@lab1.route('/402')
def error402():
    return "<h1>402 Payment Required</h1><p>Необходима оплата для продолжения.</p>", 402


@lab1.route('/403')
def error403():
    return "<h1>403 Forbidden</h1><p>У вас нет прав для доступа к этому ресурсу.</p>", 403


@lab1.route('/405')
def error405():
    return "<h1>405 Method Not Allowed</h1><p>Метод запроса не поддерживается для данного ресурса.</p>", 405


@lab1.route('/418')
def error418():
    return "<h1>418 I'm a teapot</h1><p>Я — чайник. Сервер отказывается заваривать кофе в чайнике.</p>", 418


@lab1.route('/error')
def error():
    return 1 / 0
