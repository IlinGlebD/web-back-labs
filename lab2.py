from flask import Blueprint, url_for, request, redirect, abort, render_template
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {'flower': 'роза', 'price': 300},
    {'flower': 'тюльпан', 'price': 310},
    {'flower': 'незабудка', 'price': 320},
    {'flower': 'ромашка', 'price': 330},
    ]


@lab2.route('/lab2/flowers/')
def all_flowers():
    return render_template('lab2/flower.html', flower=flower_list)


@lab2.route('/lab2/add_flower/', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = request.form.get('price')
    if name and price:
        flower_list.append({"flower": name, "price": int(price)})
    return redirect('/lab2/flowers/')


@lab2.route('/lab2/del_flowers/')
def del_flowers():
    if len(flower_list) == 0:
        abort(404)
    flower_list.clear()
    return '''<h1>Цветов нет</h1>
    <p><a href="/lab2/flowers/">Список цветов</a></p>'''


@lab2.route('/lab2/del_flowers/<int:idx>/')
def delete_flower(idx):
    if idx < 0 or idx >= len(flower_list):
        abort(404)
    flower_list.pop(idx)
    return redirect('/lab2/flowers/')


@lab2.route('/lab2/example/')
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
    return render_template('lab2/example.html', name=name,
                           lab_number=lab_number, group=group,
                           course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = '0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:num1>/<int:num2>')
def calc(num1, num2):
    return f'''<h1>Расчёт с параметрами:</h1>
    <p>{num1} + {num2} = {num1 + num2}<br>
    {num1} - {num2} = {num1 - num2}<br>
    {num1} x {num2} = {num1 * num2}<br>
    {num1}/{num2} = {num1/num2}<br>
    {num1}<sup>{num2}</sup> = {num1**num2}</p>'''


@lab2.route('/lab2/calc/')
def calc1():
    return redirect(url_for('lab2.calc', num1=1, num2=1))


@lab2.route('/lab2/calc/<int:num1>')
def calc_with_one(num1):
    return redirect(url_for('lab2.calc', num1=num1, num2=1))


@lab2.route('/lab2/books/')
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
    return render_template('lab2/books.html', books=books_data)


@lab2.route('/lab2/gallery/')
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
    return render_template('lab2/gallery.html', items=cats, title="Галерея котиков")
