from flask import Flask, url_for, request, redirect, Response, abort, render_template
import datetime
app = Flask(__name__)

@app.route("/lab1/web")
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

@app.route('/lab1/author')
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

@app.route('/lab1/image')
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

@app.route('/lab1/counter')
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

@app.route('/lab1/cleencounter')
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

@app.route('/lab1/info')
def info():
    return redirect('/lab1/author')

@app.route('/lab1/created')
def created():
    return '''<!doctype html>
        <html>
           <body>
               <h1>Создано успешно</h1>
               <div><i>что-то создано...</i></div>
           </body>
        </html>''', 201

@app.route('/404')
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

@app.route('/')
@app.route('/index')
def index():
    return '''<!doctype html>
        <html>
            <head>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <meta charset="utf-8">
            </head>
            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
                </header>
                <ul>
                    <li><a href="/lab1">Лабораторная работа 1</a></li>
                    <li><a href="/lab2">Лабораторная работа 2</a></li>
                </ul>
                <hr>
                <footer>
                    Ильин Глеб Дмитриевич, ФБИ-32, 3 курс, 2025
                </footer>
            </body>
        </html>'''

@app.route('/lab1')
def lab1():
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

@app.route('/400')
def error400():
    return "<h1>400 Bad Request</h1><p>Запрос не может быть понят сервером из-за некорректного синтаксиса.</p>", 400

@app.route('/401')
def error401():
    return "<h1>401 Unauthorized</h1><p>Для доступа требуется аутентификация.</p>", 401

@app.route('/402')
def error402():
    return "<h1>402 Payment Required</h1><p>Необходима оплата для продолжения.</p>", 402

@app.route('/403')
def error403():
    return "<h1>403 Forbidden</h1><p>У вас нет прав для доступа к этому ресурсу.</p>", 403

@app.route('/405')
def error405():
    return "<h1>405 Method Not Allowed</h1><p>Метод запроса не поддерживается для данного ресурса.</p>", 405

@app.route('/418')
def error418():
    return "<h1>418 I'm a teapot</h1><p>Я — чайник. Сервер отказывается заваривать кофе в чайнике.</p>", 418

@app.route('/error')
def error():
    return 1 / 0

@app.errorhandler(500)
def internal_error(err):
    e500 = url_for('static', filename='500.webp')
    return '''<!doctype html>
        <html>
            <head>
                <meta charset="utf-8">
                <title>Ошибка 500 — Внутренняя ошибка сервера</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background: #fff5f5;
                        color: #333;
                        text-align: center;
                        padding: 60px;
                    }
                    h1 {
                        font-size: 42px;
                        color: #c00;
                    }
                    p {
                        font-size: 20px;
                        margin: 20px 0;
                    }
                    a {
                        color: #0066cc;
                        text-decoration: none;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    img {
                        hieght: 500px;
                        width: 500px;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <h1>500 — Упс! Что-то пошло не так...</h1>
                <p>
                    На сервере произошла внутренняя ошибка.<br>
                    Пожалуйста, попробуйте позже или вернитесь <a href="/">на главную</a>.
                </p>
                <img src="''' + e500 + '''" alt="500 error cat">
            </body>
        </html>
        ''', 500

# Журнал посещений
access_log = []

@app.errorhandler(404)
def not_found(err):
    ip = request.remote_addr
    date = datetime.datetime.now()
    url = request.url

    # Добавляем запись в журнал
    access_log.append(f"[{date}] пользователь {ip} зашел на адрес: {url}")

    # Создаём HTML для журнала
    log_html = "<ul>"
    for entry in access_log:
        log_html += f"<li>{entry}</li>"
    log_html += "</ul>"

    return f'''<!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>404 — Страница не найдена</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f0f8ff;
                    color: #333;
                    text-align: center;
                    padding: 40px;
                }}
                h1 {{
                    font-size: 48px;
                    color: #d9534f;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 20px;
                    margin-bottom: 20px;
                }}
                a {{
                    color: #0275d8;
                    text-decoration: none;
                    font-weight: bold;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                ul {{
                    text-align: left;
                    display: inline-block;
                    margin-top: 20px;
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 5px;
                }}
            </style>
        </head>
        <body>
            <h1>404 — Страница не найдена</h1>
            <p>Ваш IP: {ip}<br>
            Дата: {date}<br>
            <a href="/">Вернуться на главную</a></p>
            <h2>Журнал посещений</h2>
            {log_html}
        </body>
    </html>
    ''', 404

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {'flower': 'роза', 'price': 300},
    {'flower': 'тюльпан', 'price': 310},
    {'flower': 'незабудка', 'price': 320},
    {'flower': 'ромашка', 'price': 330},
    ]

@app.route('/lab2/flowers/')
def all_flowers():
    return render_template('flower.html', flower=flower_list)

@app.route('/lab2/add_flower/', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = request.form.get('price')
    if name and price:
        flower_list.append({"flower": name, "price": int(price)})
    return redirect('/lab2/flowers/')

@app.route('/lab2/del_flowers/')
def del_flowers():
    if len(flower_list) == 0:
        abort(404)
    flower_list.clear()
    return '''<h1>Цветов нет</h1>
    <p><a href="/lab2/flowers/">Список цветов</a></p>'''

@app.route('/lab2/del_flowers/<int:idx>/')
def delete_flower(idx):
    if idx < 0 or idx >= len(flower_list):
        abort(404)
    flower_list.pop(idx)
    return redirect('/lab2/flowers/')

@app.route('/lab2/example/')
def example():
    name = 'Ильин Глеб'
    lab_number = 2
    group = 'ФБИ-32'
    course = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
        ]
    return render_template('example.html', name=name,
                           lab_number=lab_number, group=group,
                           course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = '0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:num1>/<int:num2>')
def calc(num1, num2):
    return f'''<h1>Расчёт с параметрами:</h1>
    <p>{num1} + {num2} = {num1 + num2}<br>
    {num1} - {num2} = {num1 - num2}<br>
    {num1} x {num2} = {num1 * num2}<br>
    {num1}/{num2} = {num1/num2}<br>
    {num1}<sup>{num2}</sup> = {num1**num2}</p>'''

@app.route('/lab2/calc/')
def calc1():
    return redirect(url_for('calc', num1=1, num2=1))

@app.route('/lab2/calc/<int:num1>')
def calc_with_one(num1):
    return redirect(url_for('calc', num1=num1, num2=1))

@app.route('/lab2/books/')
def books():
    books_data = [
        {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
        {"author": "Рэй Брэдбери", "title": "451° по Фаренгейту", "genre": "Фантастика", "pages": 249},
        {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Роман", "pages": 480},
        {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман-эпопея", "pages": 1225},
        {"author": "Фрэнсис С. Фицджеральд", "title": "Великий Гэтсби", "genre": "Роман", "pages": 200},
        {"author": "Даниэль Киз", "title": "Цветы для Элджернона", "genre": "Научная фантастика", "pages": 288},
        {"author": "Джоан Роулинг", "title": "Гарри Поттер и философский камень", "genre": "Фэнтези", "pages": 352},
        {"author": "Александр Дюма", "title": "Граф Монте-Кристо", "genre": "Приключения", "pages": 1312},
        {"author": "Артур Конан Дойл", "title": "Собака Баскервилей", "genre": "Детектив", "pages": 256},
        {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 464},
        {"author": "Дж. Р. Р. Толкин", "title": "Хоббит", "genre": "Фэнтези", "pages": 304},
    ]
    return render_template('books.html', books=books_data)

@app.route('/lab2/gallery/')
def gallery():
    cats = [
        {"name": "Барсик", "slug": "cat1", "desc": "Любит спать на клавиатуре."},
        {"name": "Мурка", "slug": "cat2", "desc": "Охотница за солнечными зайчиками."},
        {"name": "Симба", "slug": "cat3", "desc": "Король подоконника."},
        {"name": "Буся", "slug": "cat4", "desc": "Обожает бумажные пакеты."},
        {"name": "Тима", "slug": "cat5", "desc": "Занимается паркуром по шторам."},
        {"name": "Луна", "slug": "cat6", "desc": "Ночная сторожка холодильника."},
        {"name": "Пушок", "slug": "cat7", "desc": "Самый мягкий в мире."},
        {"name": "Кнопа", "slug": "cat8", "desc": "Мини-кот с максимальным характером."},
        {"name": "Феликс", "slug": "cat9", "desc": "Ценитель картонных коробок."},
        {"name": "Нюша", "slug": "cat10", "desc": "Громко мурчит по утрам."},
        {"name": "Граф", "slug": "cat11", "desc": "Эстет и лорд лотка."},
        {"name": "Снежок", "slug": "cat12", "desc": "Бел как облачко."},
        {"name": "Зефир", "slug": "cat13", "desc": "Сладкий, но шкодный."},
        {"name": "Чёрныш", "slug": "cat14", "desc": "Мастер стелса."},
        {"name": "Лео", "slug": "cat15", "desc": "Маленький лев, большой характер."},
        {"name": "Персик", "slug": "cat16", "desc": "Персиковый пушистик."},
        {"name": "Ириска", "slug": "cat17", "desc": "Липнет к людям."},
        {"name": "Марс", "slug": "cat18", "desc": "Космокот: любит коробки-ракеты."},
        {"name": "Туман", "slug": "cat19", "desc": "Едва заметен в пледе."},
        {"name": "Соня", "slug": "cat20", "desc": "Спит 25 часов в сутки."},
        {"name": "Рыжик", "slug": "cat21", "desc": "Солнечный характер."},
        {"name": "Боня", "slug": "cat22", "desc": "Хрустит кормом как чипсами."},
        {"name": "Мята", "slug": "cat23", "desc": "Любит кошачью мяту (очевидно!)."},
        {"name": "Тигра", "slug": "cat24", "desc": "Полосатый инспектор шкафа."},
    ]
    # для каждого кота - файл static/images/cats/<slug>.jpg
    for item in cats:
        item["img_url"] = url_for('static',
                                  filename=f'images/cats/{item["slug"]}.jpg')
    return render_template('gallery.html', items=cats, title="Галерея котиков")
