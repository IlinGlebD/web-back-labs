from flask import Blueprint, render_template, request, jsonify, session
import random

lab9 = Blueprint("lab9", __name__)

TOTAL_BOXES = 10
LIMIT_PER_USER = 3

# Эти коробки можно открыть только авторизованным
RESTRICTED_BOXES = {0, 1, 2}

GREETINGS = [
    "С Новым годом! Пусть мечты сбываются!",
    "Желаю счастья, здоровья и тепла!",
    "Пусть новый год принесёт удачу!",
    "Пусть будет больше радости и меньше забот!",
    "Желаю ярких событий и побед!",
    "Пусть дом будет полон уюта и любви!",
    "Пусть финансы растут, а стресс убывает!",
    "Желаю вдохновения и уверенности в себе!",
    "Пусть каждый день будет лучше предыдущего!",
    "Пусть всё задуманное реализуется!"
]

BOX_IMAGES = ["box1.png", "box2.png", "box3.png", "box4.png", "box5.png"]

# Глобально для всех пользователей/браузеров (в памяти процесса сервера)
opened_boxes_global = set()


def is_authenticated() -> bool:
    # Самый простой способ: если у вас уже есть авторизация в проекте —
    # просто убедитесь, что при логине кладёте user_id в session.
    return "user_id" in session


def ensure_session_data():
    # Коробки в сетке: храним только id и картинку (позиции делает CSS-grid)
    if "lab9_positions" not in session:
        session["lab9_positions"] = [{"id": i, "img": random.choice(BOX_IMAGES)} for i in range(TOTAL_BOXES)]

    # Уникальные поздравления на каждую коробку (для данного пользователя)
    if "lab9_map" not in session:
        ids = list(range(TOTAL_BOXES))
        random.shuffle(ids)

        gift_map = {}
        for idx, box_id in enumerate(ids):
            gift_map[str(box_id)] = {
                "greeting": GREETINGS[idx],
                "gift_img": random.choice(BOX_IMAGES)
            }
        session["lab9_map"] = gift_map

    session.setdefault("lab9_opened_count", 0)


@lab9.route("/lab9/")
def main():
    ensure_session_data()
    return render_template(
        "lab9/index.html",
        positions=session["lab9_positions"],
        opened_global=list(opened_boxes_global),
        remaining=TOTAL_BOXES - len(opened_boxes_global),
        opened_count=session["lab9_opened_count"],
        total_boxes=TOTAL_BOXES,
        is_auth=is_authenticated(),
        restricted_boxes=list(RESTRICTED_BOXES)
    )


@lab9.post("/lab9/api/status")
def api_status():
    ensure_session_data()
    return jsonify({
        "remaining": TOTAL_BOXES - len(opened_boxes_global),
        "opened_global": list(opened_boxes_global),
        "opened_count": session.get("lab9_opened_count", 0),
        "limit": LIMIT_PER_USER,
        "total": TOTAL_BOXES
    })


@lab9.post("/lab9/api/open")
def api_open():
    ensure_session_data()

    data = request.get_json(force=True) or {}
    box_id = data.get("box_id")

    if box_id is None:
        return jsonify({"ok": False, "message": "Не передан box_id"}), 400

    try:
        box_id = int(box_id)
    except ValueError:
        return jsonify({"ok": False, "message": "Некорректный box_id"}), 400

    if box_id < 0 or box_id >= TOTAL_BOXES:
        return jsonify({"ok": False, "message": "Коробка не найдена"}), 404

    # Закрытые коробки — только для авторизованных
    if (box_id in RESTRICTED_BOXES) and (not is_authenticated()):
        return jsonify({
            "ok": False,
            "auth_required": True,
            "message": "Этот подарок доступен только авторизованным пользователям."
        }), 200

    # Уже открыта глобально (в любом браузере)
    if box_id in opened_boxes_global:
        return jsonify({
            "ok": False,
            "already_opened": True,
            "message": "Эта коробка уже пустая — подарок забрали."
        }), 200

    # Лимит 3 на пользователя (в сессии)
    opened_count = session.get("lab9_opened_count", 0)
    if opened_count >= LIMIT_PER_USER:
        return jsonify({
            "ok": False,
            "limit_reached": True,
            "message": "Вы уже открыли 3 коробки. Больше нельзя!"
        }), 200

    # Открываем
    opened_boxes_global.add(box_id)
    session["lab9_opened_count"] = opened_count + 1

    payload = session["lab9_map"].get(str(box_id))
    if not payload:
        return jsonify({"ok": False, "message": "Нет данных по коробке"}), 500

    return jsonify({
        "ok": True,
        "box_id": box_id,
        "greeting": payload["greeting"],
        "gift_img": payload["gift_img"],
        "remaining": TOTAL_BOXES - len(opened_boxes_global),
        "opened_count": session["lab9_opened_count"],
        "limit": LIMIT_PER_USER
    })


@lab9.post("/lab9/api/refill")
def api_refill():
    # Кнопка "Дед Мороз" — только для авторизованных
    if not is_authenticated():
        return jsonify({"ok": False, "message": "Только для авторизованных пользователей."}), 403

    opened_boxes_global.clear()          # все коробки снова полные (для всех)
    session["lab9_opened_count"] = 0     # сброс лимита для текущего пользователя

    return jsonify({
        "ok": True,
        "message": "Дед Мороз наполнил все коробки!",
        "remaining": TOTAL_BOXES - len(opened_boxes_global),
        "opened_count": session["lab9_opened_count"],
        "limit": LIMIT_PER_USER
    })


@lab9.route("/lab9/reset")
def reset():
    session.clear()
    return "ok"
