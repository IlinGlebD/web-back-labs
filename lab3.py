from flask import Blueprint, render_template, request, make_response, redirect
from datetime import datetime

lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'Аноним')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age', 'неизвестно сколько')
    return render_template('lab3/lab3.html', name=name, name_color=name_color,
                           age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Gleb', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    errors = {}
    submitted = bool(request.args)  # форма отправлена?
    if request.args:
        if not user:
            errors['user'] = 'Заполните поле!'
        if not age:
            errors['age'] = 'Заполните поле!'
    ok = submitted and not errors
    return render_template('lab3/form1.html', user=user, age=age, sex=sex,
                           errors=errors, ok=ok)


@lab3.route('/lab3/order')
def order():
    return render_template('/lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success', methods=['GET', 'POST'])
def success():
    price = request.values.get('price', type=int)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    # получаем параметры из адресной строки
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fontsize = request.args.get('fontsize')
    lineheight = request.args.get('lineheight')

    # если есть изменения — ставим cookie и делаем redirect
    if any([color, bgcolor, fontsize, lineheight]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bgcolor:
            resp.set_cookie('bgcolor', bgcolor)
        if fontsize:
            resp.set_cookie('fontsize', fontsize)
        if lineheight:
            resp.set_cookie('lineheight', lineheight)
        return resp

    # читаем текущие cookie и отображаем шаблон
    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fontsize = request.cookies.get('fontsize')
    lineheight = request.cookies.get('lineheight')

    resp = make_response(render_template(
        'lab3/settings.html',
        color=color,
        bgcolor=bgcolor,
        fontsize=fontsize,
        lineheight=lineheight
    ))
    return resp


@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bgcolor')
    resp.delete_cookie('fontsize')
    resp.delete_cookie('lineheight')
    return resp


@lab3.route('/lab3/ticket/order',  methods=['GET'])
def ticket_order():
    return render_template('lab3/ticket_order.html', errors=None, form_data={})


@lab3.route('/lab3/ticket/submit', methods=['POST'])
def ticket_submit():
    # Считываем значения
    full_name = request.form.get('full_name', '').strip()
    berth = request.form.get('berth')  # нижняя/верхняя/верхняя боковая/нижняя боковая
    bedding = request.form.get('bedding')  # 'yes'/'no'
    baggage = request.form.get('baggage')  # 'yes'/'no'
    age_raw = request.form.get('age', '').strip()
    origin = request.form.get('origin', '').strip()
    destination = request.form.get('destination', '').strip()
    trip_date_s = request.form.get('trip_date', '').strip()
    insurance = request.form.get('insurance')  # 'yes'/'no'

    errors = []
    form_data = {
        'full_name': full_name,
        'berth': berth,
        'bedding': bedding,
        'baggage': baggage,
        'age': age_raw,
        'origin': origin,
        'destination': destination,
        'trip_date': trip_date_s,
        'insurance': insurance
    }

    # Валидация "все поля непустые"
    required_radio = {
        'bedding': bedding,
        'baggage': baggage,
        'insurance': insurance
        }
    for k, v in required_radio.items():
        if v not in ('yes', 'no'):
            errors.append('Выберите вариант для поля: ' + {
                'bedding': 'С бельём',
                'baggage': 'С багажом',
                'insurance': 'Нужна ли страховка'
            }[k])

    if not full_name:
        errors.append('Введите ФИО пассажира.')
    if berth not in ('нижняя', 'верхняя', 'верхняя боковая', 'нижняя боковая'):
        errors.append('Выберите полку.')
    if not origin:
        errors.append('Укажите пункт выезда.')
    if not destination:
        errors.append('Укажите пункт назначения.')
    if origin and destination and origin.lower() == destination.lower():
        errors.append('Пункты выезда и назначения не должны совпадать.')

    # Возраст
    try:
        age = int(age_raw)
        if age < 1 or age > 120:
            errors.append('Возраст должен быть от 1 до 120 лет.')
    except ValueError:
        errors.append('Возраст должен быть целым числом.')
        age = None  # чтобы не падать ниже

    # Дата
    trip_date = None
    if not trip_date_s:
        errors.append('Укажите дату поездки.')
    else:
        try:
            trip_date = datetime.strptime(trip_date_s, '%Y-%m-%d').date()
        except ValueError:
            errors.append('Некорректный формат даты.')

    if errors:
        return render_template('lab3/ticket_order.html', errors=errors,
                               form_data=form_data), 400

    # Расчёт цены
    price = 1000 if age >= 18 else 700  # базовая
    if berth in ('нижняя', 'нижняя боковая'):
        price += 100
    if bedding == 'yes':
        price += 75
    if baggage == 'yes':
        price += 250
    if insurance == 'yes':
        price += 150

    is_child = age < 18

    # Можно собрать разбор цены для отображения
    breakdown = []
    breakdown.append(('Базовый тариф', 700 if is_child else 1000))
    if berth in ('нижняя', 'нижняя боковая'):
        breakdown.append(('Нижняя/нижняя боковая полка', 100))
    if bedding == 'yes':
        breakdown.append(('Бельё', 75))
    if baggage == 'yes':
        breakdown.append(('Багаж', 250))
    if insurance == 'yes':
        breakdown.append(('Страховка', 150))

    return render_template(
        'lab3/ticket.html',
        full_name=full_name,
        berth=berth,
        bedding=bedding == 'yes',
        baggage=baggage == 'yes',
        age=age,
        origin=origin,
        destination=destination,
        trip_date=trip_date,
        insurance=insurance == 'yes',
        is_child=is_child,
        price=price,
        breakdown=breakdown
    )


PRODUCTS = [
    {"name": "Galaxy S21", "price": 39990, "brand": "Samsung", "color": "черный"},
    {"name": "iPhone 13", "price": 69990, "brand": "Apple",   "color": "белый"},
    {"name": "Pixel 7", "price": 45990, "brand": "Google",  "color": "черный"},
    {"name": "Redmi Note 12", "price": 19990, "brand": "Xiaomi",  "color": "синий"},
    {"name": "Realme 11", "price": 22990, "brand": "Realme",  "color": "золотой"},
    {"name": "Nothing Phone (1)", "price": 34990, "brand": "Nothing", "color": "черный"},
    {"name": "Moto G54", "price": 15990, "brand": "Motorola","color": "зеленый"},
    {"name": "Honor 90", "price": 42990, "brand": "Honor",   "color": "серебристый"},
    {"name": "Poco F5", "price": 33990, "brand": "Xiaomi",  "color": "белый"},
    {"name": "Galaxy A55", "price": 29990, "brand": "Samsung", "color": "голубой"},
    {"name": "iPhone SE", "price": 39990, "brand": "Apple",   "color": "красный"},
    {"name": "Pixel 6a", "price": 32990, "brand": "Google",  "color": "мятный"},
    {"name": "Infinix Note 30", "price": 14990, "brand": "Infinix", "color": "черный"},
    {"name": "Tecno Pova 5", "price": 13990, "brand": "Tecno",   "color": "синий"},
    {"name": "Vivo V29", "price": 37990, "brand": "Vivo",    "color": "черный"},
    {"name": "OPPO Reno10", "price": 35990, "brand": "OPPO",    "color": "серый"},
    {"name": "Sony Xperia 10 V", "price": 44990, "brand": "Sony",    "color": "белый"},
    {"name": "Nokia G42", "price": 16990, "brand": "Nokia",   "color": "фиолетовый"},
    {"name": "Asus Zenfone 9", "price": 55990, "brand": "ASUS",    "color": "черный"},
    {"name": "OnePlus Nord 3", "price": 39990, "brand": "OnePlus", "color": "зеленый"},
    {"name": "Huawei nova 11", "price": 32990, "brand": "Huawei",  "color": "черный"},
    {"name": "Meizu 20", "price": 28990, "brand": "Meizu",   "color": "серебристый"},
]


def overall_min_max():
    prices = [p["price"] for p in PRODUCTS]
    return (min(prices), max(prices))


def apply_filters(items, min_p, max_p):
    result = []
    for it in items:
        price = it["price"]
        if min_p is not None and price < min_p:
            continue
        if max_p is not None and price > max_p:
            continue
        result.append(it)
    return result


@lab3.route('/lab3/products', methods=['GET'])
def products_filter():
    # Глобальные мин/макс для плейсхолдеров
    glob_min, glob_max = overall_min_max()

    # Кнопка сброса: очищаем куки и показываем все
    if request.args.get('action') == 'reset':
        resp = make_response(render_template(
            'lab3/products.html',
            items=PRODUCTS,
            count=len(PRODUCTS),
            glob_min=glob_min, glob_max=glob_max,
            cur_min='', cur_max='',  # поля пустые
            message=None
        ))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp

    # Берем значения: сначала из query, если пусто — из cookie
    min_s = request.args.get('min', default=None)
    max_s = request.args.get('max', default=None)

    # Если пользователь не передал параметры, но есть куки — подставим их
    if (min_s is None or min_s == ''):
        min_s = request.cookies.get('min_price', default='')
    if (max_s is None or max_s == ''):
        max_s = request.cookies.get('max_price', default='')

    # Преобразуем к числам (пустые оставляем None)
    def to_int_or_none(s):
        if s is None or s == '':
            return None
        try:
            return int(s)
        except:
            return None

    min_v = to_int_or_none(min_s)
    max_v = to_int_or_none(max_s)

    # Если оба заданы и перепутаны — меняем местами
    if min_v is not None and max_v is not None and min_v > max_v:
        min_v, max_v = max_v, min_v
        # и в форме поменяем местами
        min_s, max_s = (str(min_v), str(max_v))

    # Фильтруем (если оба None — покажем все)
    filtered = apply_filters(PRODUCTS, min_v, max_v)
    message = None
    if len(filtered) == 0:
        message = "Не найдено ни одного товара"

    # Готовим ответ и ставим куки, если пользователь передал фильтры
    resp = make_response(render_template(
        'lab3/products.html',
        items=filtered,
        count=len(filtered),
        glob_min=glob_min, glob_max=glob_max,
        cur_min=min_s or '',
        cur_max=max_s or '',
        message=message
    ))

    # Сохраняем куки только если хотя бы одно из значений было в запросе
    # (т.е. человек нажал «Искать»)
    if 'min' in request.args or 'max' in request.args:
        # Пустые очищаем
        if min_v is None:
            resp.delete_cookie('min_price')
        else:
            resp.set_cookie('min_price', str(min_v))
        if max_v is None:
            resp.delete_cookie('max_price')
        else:
            resp.set_cookie('max_price', str(max_v))

    return resp
