import os
import json
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, jsonify, send_from_directory

app = Flask(__name__)
app.secret_key = "change-me-random-string-2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
PHOTOS_JSON = os.path.join(BASE_DIR, "photos.json")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXT = {"png", "jpg", "jpeg", "webp", "gif"}
ADMIN_PASSWORD = "nogti2026"

SERVICES = {
    "man_ukrep": "Маникюр + укрепление гелем",
    "man_gig": "Гигиенический маникюр",
    "man_french": "Маникюр + гель-лак + френч",
    "man_design": "Маникюр + покрытие + дизайн",
    "man_muzh": "Мужской маникюр",
    "man_snyatie": "Снятие покрытия",
    "man_snyatie_gig": "Снятие покрытия + гигиенический маникюр",
    "man_model": "Моделирование",
    "ped_uhod": "Аппаратный педикюр + уход",
    "ped_pokrytie": "Аппаратный педикюр + покрытие гель-лаком",
    "ped_express": "Экспресс педикюр",
    "ped_express_pokrytie": "Экспресс педикюр с покрытием гель-лак",
    "ped_muzh": "Мужской педикюр",
    "ped_snyatie": "Снятие покрытия (педикюр)",
    "ped_snyatie_express": "Снятие покрытия + экспресс педикюр",
    "cx_s": "Комплекс S",
    "cx_m": "Комплекс M",
    "cx_l": "Комплекс L",
    "cx_xl": "Комплекс XL",
    "cabinet_hero": "Фото кабинета (главный экран)",
    "cabinet_about": "Фото кабинета (О нас)",
    "work_1": "Работа 1",
    "work_2": "Работа 2",
    "work_3": "Работа 3",
    "work_4": "Работа 4",
    "work_5": "Работа 5",
    "work_6": "Работа 6",
}


def load_photos():
    if os.path.exists(PHOTOS_JSON):
        try:
            with open(PHOTOS_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_photos(data):
    with open(PHOTOS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/api/photos")
def api_photos():
    return jsonify(load_photos())


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("password") != ADMIN_PASSWORD:
            return render_template_string(
                ADMIN_TEMPLATE,
                services=SERVICES,
                photos=load_photos(),
                error="Неверный пароль",
                authed=False,
            )
        key = request.form.get("service_key")
        file = request.files.get("photo")
        if key in SERVICES and file and file.filename and allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"{key}.{ext}"
            file.save(os.path.join(UPLOAD_DIR, filename))
            photos = load_photos()
            photos[key] = filename
            save_photos(photos)
            return redirect(url_for("admin", ok=1))
        return redirect(url_for("admin", err=1))
    return render_template_string(
        ADMIN_TEMPLATE, services=SERVICES, photos=load_photos(), authed=True
    )


ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Админка — На ногтях</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #F5F5F4; color: #2A2A2C; margin: 0; padding: 30px; }
        .wrap { max-width: 900px; margin: 0 auto; }
        h1 { font-size: 1.4rem; margin-bottom: 20px; }
        .card { background: #fff; border: 1px solid #E4E5E7; border-radius: 6px; padding: 16px; margin-bottom: 12px; }
        .row { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
        .thumb { width: 56px; height: 56px; background: #E4E5E7; border-radius: 4px; object-fit: cover; display: flex; align-items: center; justify-content: center; color: #8A8D91; font-size: 0.6rem; }
        button { background: #2A2A2C; color: #fff; border: 0; padding: 9px 16px; border-radius: 4px; cursor: pointer; font-size: 0.8rem; }
        .ok { color: #2e7d32; font-size: 0.85rem; }
        .err { color: #c62828; font-size: 0.85rem; }
        .login { max-width: 320px; margin: 80px auto; }
        input[type=password] { width: 100%; padding: 10px; border: 1px solid #E4E5E7; border-radius: 4px; margin-bottom: 12px; font-size: 1rem; box-sizing: border-box; }
        a { color: #2A2A2C; }
    </style>
</head>
<body>
<div class="wrap">
    <h1>Админка «На ногтях»</h1>
    {% if not authed %}
    <div class="card login">
        <form method="post">
            <input type="password" name="password" placeholder="Пароль" required>
            <button type="submit">Войти</button>
        </form>
        {% if error %}<p class="err">{{ error }}</p>{% endif %}
    </div>
    {% else %}
    {% if request.args.get('ok') %}<p class="ok">Фото загружено.</p>{% endif %}
    {% if request.args.get('err') %}<p class="err">Ошибка: проверьте формат (png, jpg, jpeg, webp, gif).</p>{% endif %}
    <p><a href="/">← На сайт</a></p>
    {% for key, title in services.items() %}
    <div class="card">
        <div class="row">
            {% if photos.get(key) %}
                <img class="thumb" src="/uploads/{{ photos[key] }}" alt="{{ title }}">
            {% else %}
                <div class="thumb">НЕТ</div>
            {% endif %}
            <div style="flex:1; min-width:180px;">
                <strong>{{ title }}</strong><br>
                <span style="font-size:0.75rem;color:#8A8D91;">{{ key }}</span>
            </div>
            <form method="post" enctype="multipart/form-data" class="row">
                <input type="hidden" name="service_key" value="{{ key }}">
                <input type="hidden" name="password" value="__AUTHED__">
                <input type="file" name="photo" accept="image/*" required>
                <button type="submit">Загрузить</button>
            </form>
        </div>
    </div>
    {% endfor %}
    {% endif %}
</div>
</body>
</html>
"""


HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>На ногтях — маникюр и педикюр в центре Оренбурга</title>
    <meta name="description" content="Студия маникюра и педикюра «На ногтях» в Оренбурге. Скорость, стерильность, светлый кабинет. Онлайн-запись.">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>Н</text></svg>">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --white: #FFFFFF;
            --offwhite: #F5F5F4;
            --marble: #E4E5E7;
            --muted: #8A8D91;
            --graphite: #2A2A2C;
            --radius: 3px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body {
            font-family: 'Montserrat', sans-serif;
            color: var(--graphite);
            background: var(--white);
            line-height: 1.65;
            font-weight: 300;
            -webkit-font-smoothing: antialiased;
        }
        .container { max-width: 1180px; margin: 0 auto; padding: 0 24px; }

        header {
            background: rgba(255,255,255,0.92);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--marble);
            padding: 16px 0;
            position: sticky; top: 0; z-index: 100;
        }
        .header-inner { display: flex; justify-content: space-between; align-items: center; gap: 24px; }
        .logo {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.6rem;
            font-weight: 500;
            letter-spacing: 3px;
            color: var(--graphite);
            text-transform: uppercase;
            text-decoration: none;
            white-space: nowrap;
        }
        nav { display: flex; align-items: center; gap: 28px; }
        nav a {
            text-decoration: none; color: var(--graphite);
            font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase;
            transition: color 0.3s;
        }
        nav a:hover { color: var(--muted); }
        .header-phone {
            font-size: 0.9rem; color: var(--graphite);
            text-decoration: none; white-space: nowrap;
        }
        .header-phone:hover { color: var(--muted); }
        .btn {
            display: inline-block;
            background: var(--graphite);
            color: #fff !important;
            padding: 12px 28px;
            border-radius: var(--radius);
            font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase;
            text-decoration: none;
            transition: background 0.3s, color 0.3s;
            border: 1px solid var(--graphite);
            cursor: pointer;
        }
        .btn:hover { background: transparent; color: var(--graphite) !important; }

        .hero {
            padding: 90px 0 0;
            background:
                linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)),
                url('/static/marble.jpg') center/cover no-repeat;
        }
        .hero-inner {
            display: grid;
            grid-template-columns: 1.1fr 1fr;
            gap: 60px;
            align-items: center;
        }
        .hero-kicker {
            font-size: 0.75rem; letter-spacing: 4px; text-transform: uppercase;
            color: var(--muted); margin-bottom: 20px;
        }
        .hero h1 {
            font-family: 'Cormorant Garamond', serif;
            font-size: 3.6rem;
            font-weight: 400;
            line-height: 1.1;
            color: var(--graphite);
            margin-bottom: 20px;
        }
        .hero p {
            font-size: 1rem; color: var(--muted);
            max-width: 460px; margin-bottom: 32px;
        }
        .hero-actions { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }
        .hero-actions .link-max {
            font-size: 0.85rem; color: var(--graphite);
            text-decoration: none; border-bottom: 1px solid var(--muted);
            padding-bottom: 2px;
        }
        .hero-actions .link-max:hover { color: var(--muted); }
        .hero-image {
            aspect-ratio: 3/4;
            background: var(--marble);
            border-radius: var(--radius);
            overflow: hidden;
        }
        .hero-image img { width: 100%; height: 100%; object-fit: cover; display: block; }
        .facts {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            border-top: 1px solid var(--marble);
            margin-top: 60px;
        }
        .fact {
            padding: 24px 0;
            text-align: center;
            font-size: 0.85rem;
            color: var(--graphite);
            border-right: 1px solid var(--marble);
        }
        .fact:last-child { border-right: none; }
        .fact span { display: block; font-size: 0.75rem; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }

        section { padding: 90px 0; }
        .section-label {
            font-size: 0.7rem; letter-spacing: 4px; text-transform: uppercase;
            color: var(--muted); margin-bottom: 12px; text-align: center;
        }
        .section-title {
            font-family: 'Cormorant Garamond', serif;
            font-size: 2.6rem; font-weight: 400;
            text-align: center; color: var(--graphite);
            margin-bottom: 50px;
        }

        .about { background: var(--offwhite); }
        .about-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }
        .about-image {
            aspect-ratio: 4/5;
            background: var(--marble);
            border-radius: var(--radius);
            overflow: hidden;
        }
        .about-image img { width: 100%; height: 100%; object-fit: cover; display: block; }
        .about-text p { color: var(--graphite); font-size: 1rem; margin-bottom: 16px; }
        .about-text p:last-of-type { margin-bottom: 0; }

        .features { background: var(--white); }
        .features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
        }
        .feature-num {
            font-family: 'Cormorant Garamond', serif;
            font-size: 2.6rem; font-weight: 300;
            color: var(--marble);
            line-height: 1;
            margin-bottom: 14px;
        }
        .feature-item h3 {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.4rem; font-weight: 500;
            margin-bottom: 8px; color: var(--graphite);
        }
        .feature-item p { color: var(--muted); font-size: 0.9rem; }

        .services { background: var(--offwhite); }
        .tabs {
            display: flex; justify-content: center; gap: 8px;
            margin-bottom: 40px; flex-wrap: wrap;
        }
        .tab-btn {
            background: transparent;
            border: 1px solid var(--marble);
            color: var(--graphite);
            padding: 10px 22px;
            border-radius: var(--radius);
            font-family: 'Montserrat', sans-serif;
            font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase;
            cursor: pointer;
            transition: all 0.3s;
        }
        .tab-btn.active, .tab-btn:hover {
            background: var(--graphite); color: #fff; border-color: var(--graphite);
        }
        .tab-panel { display: none; }
        .tab-panel.active { display: block; }
        .service-row {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 14px 0;
            border-bottom: 1px dotted var(--marble);
        }
        .service-thumb {
            flex: 0 0 56px;
            width: 56px; height: 56px;
            background: var(--marble);
            border-radius: var(--radius);
            overflow: hidden;
        }
        .service-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
        .service-info { flex: 1 1 auto; display: flex; flex-direction: column; }
        .service-info .name { font-weight: 400; color: var(--graphite); }
        .service-info .meta { color: var(--muted); font-size: 0.8rem; font-weight: 300; }
        .service-row .price {
            font-weight: 600; color: var(--graphite);
            white-space: nowrap;
        }
        .complexes-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }
        .complex-card {
            background: var(--white);
            border: 1px solid var(--marble);
            border-radius: var(--radius);
            padding: 26px 20px;
            position: relative;
        }
        .complex-card .badge {
            position: absolute; top: 12px; right: 12px;
            font-size: 0.65rem; letter-spacing: 1px; text-transform: uppercase;
            color: var(--muted);
        }
        .complex-thumb {
            width: 100%;
            aspect-ratio: 4/3;
            background: var(--marble);
            border-radius: var(--radius);
            overflow: hidden;
            margin-bottom: 14px;
        }
        .complex-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
        .complex-card h4 {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.6rem; font-weight: 500;
            margin-bottom: 10px; color: var(--graphite);
        }
        .complex-card .desc { font-size: 0.8rem; color: var(--muted); margin-bottom: 16px; min-height: 48px; }
        .complex-card .price { font-weight: 600; color: var(--graphite); font-size: 1.1rem; }
        .services-cta {
            text-align: center; margin-top: 40px;
            display: flex; flex-direction: column; align-items: center; gap: 14px;
        }
        .services-cta .full-price {
            font-size: 0.85rem; color: var(--graphite);
            text-decoration: none; border-bottom: 1px solid var(--muted);
            padding-bottom: 2px;
        }

        .portfolio { background: var(--white); }
        .portfolio-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        .portfolio-item {
            aspect-ratio: 1/1;
            background: var(--marble);
            border-radius: var(--radius);
            overflow: hidden;
        }
        .portfolio-item img { width: 100%; height: 100%; object-fit: cover; display: block; }

        .reviews { background: var(--offwhite); }
        .reviews-rating {
            text-align: center; margin-bottom: 40px;
        }
        .reviews-rating .num {
            font-family: 'Cormorant Garamond', serif;
            font-size: 4rem; font-weight: 300;
            color: var(--graphite); line-height: 1;
        }
        .reviews-rating .sub {
            font-size: 0.8rem; letter-spacing: 2px;
            text-transform: uppercase; color: var(--muted);
        }
        .reviews-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        .review-card {
            background: var(--white);
            border: 1px solid var(--marble);
            border-radius: var(--radius);
            padding: 26px;
        }
        .review-head {
            display: flex; justify-content: space-between; align-items: baseline;
            margin-bottom: 12px; gap: 10px;
        }
        .review-name { font-weight: 500; color: var(--graphite); }
        .review-status { font-size: 0.75rem; color: var(--muted); }
        .review-text { font-size: 0.9rem; color: var(--graphite); }
        .reviews-cta { text-align: center; margin-top: 36px; }
        .reviews-cta a {
            font-size: 0.85rem; color: var(--graphite);
            text-decoration: none; border-bottom: 1px solid var(--muted);
            padding-bottom: 2px;
        }

        .booking {
            background:
                linear-gradient(rgba(228,229,231,0.85), rgba(228,229,231,0.85)),
                url('/static/marble.jpg') center/cover no-repeat;
            padding: 80px 0;
            text-align: center;
        }
        .booking h2 {
            font-family: 'Cormorant Garamond', serif;
            font-size: 2.4rem; font-weight: 400;
            color: var(--graphite); margin-bottom: 16px;
        }
        .booking p { color: var(--graphite); margin-bottom: 30px; }
        .booking-actions {
            display: flex; justify-content: center; align-items: center;
            gap: 20px; flex-wrap: wrap;
        }
        .booking-actions .link-max {
            font-size: 0.85rem; color: var(--graphite);
            text-decoration: none; border-bottom: 1px solid var(--graphite);
            padding-bottom: 2px;
        }

        .contacts { background: var(--white); }
        .contacts-inner {
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            gap: 40px;
            align-items: start;
        }
        .contact-block { margin-bottom: 24px; }
        .contact-block strong {
            display: block;
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.3rem; font-weight: 500;
            color: var(--graphite); margin-bottom: 6px;
        }
        .contact-block p, .contact-block a { color: var(--graphite); font-size: 0.95rem; text-decoration: none; }
        .contact-block a:hover { color: var(--muted); }
        .contact-block .btn { margin-top: 8px; }
        .map-wrap {
            aspect-ratio: 16/10;
            background: var(--marble);
            border-radius: var(--radius);
            overflow: hidden;
        }
        .map-wrap iframe { width: 100%; height: 100%; border: 0; display: block; }

        footer {
            background: var(--graphite); color: var(--marble);
            padding: 24px 0;
            font-size: 0.8rem;
        }
        .footer-inner {
            display: flex; justify-content: space-between; align-items: center;
            gap: 20px; flex-wrap: wrap;
        }
        .footer-inner .logo { color: #fff; font-size: 1.2rem; }
        .footer-inner a { color: var(--marble); text-decoration: none; }
        .footer-inner a:hover { color: #fff; }

        .sticky-book {
            display: none;
            position: fixed; bottom: 0; left: 0; right: 0;
            background: var(--graphite);
            color: #fff; text-align: center;
            padding: 14px; font-size: 0.85rem; letter-spacing: 1px;
            text-transform: uppercase; text-decoration: none;
            z-index: 200;
        }

        @media (max-width: 900px) {
            .hero-inner { grid-template-columns: 1fr; gap: 40px; }
            .hero h1 { font-size: 2.4rem; }
            .hero-image { aspect-ratio: 16/10; }
            .facts { grid-template-columns: 1fr; }
            .fact { border-right: none; border-bottom: 1px solid var(--marble); }
            .fact:last-child { border-bottom: none; }
            .about-content { grid-template-columns: 1fr; }
            .about-image { aspect-ratio: 16/10; }
            .features-grid { grid-template-columns: 1fr; gap: 28px; }
            .complexes-grid { grid-template-columns: repeat(2, 1fr); }
            .reviews-grid { grid-template-columns: 1fr; }
            .contacts-inner { grid-template-columns: 1fr; }
            .portfolio-grid { grid-template-columns: repeat(2, 1fr); }
            nav a:not(.btn) { display: none; }
            .header-phone { display: none; }
            .sticky-book { display: block; }
            body { padding-bottom: 56px; }
        }
        @media (max-width: 600px) {
            .hero { padding: 60px 0 0; }
            .hero h1 { font-size: 2rem; }
            .section-title { font-size: 2rem; }
            section { padding: 60px 0; }
            .complexes-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <header>
        <div class="container header-inner">
            <a href="#" class="logo">На ногтях</a>
            <nav>
                <a href="#services">Услуги</a>
                <a href="#portfolio">Работы</a>
                <a href="#reviews">Отзывы</a>
                <a href="#contacts">Контакты</a>
                <a href="https://n1348500.yclients.ru/" class="btn" target="_blank" rel="noopener">Записаться</a>
            </nav>
            <a href="tel:+79619436282" class="header-phone">+7 (961) 943-62-82</a>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <div class="hero-inner">
                <div class="hero-text">
                    <div class="hero-kicker">Студия маникюра и педикюра</div>
                    <h1>Маникюр и педикюр в центре Оренбурга</h1>
                    <p>Светлый кабинет с панорамными окнами, стерильные инструменты и аккуратное покрытие.</p>
                    <div class="hero-actions">
                        <a href="https://n1348500.yclients.ru/" class="btn" target="_blank" rel="noopener">Записаться онлайн</a>
                        <a href="https://max.ru/u/f9LHodD0cOJ-bX6hYDR-apIXmyZo1_Ld9ZYwm9eiteKL6U75nrNiCPIacWo" class="link-max" target="_blank" rel="noopener">Написать в Max</a>
                    </div>
                </div>
                <div class="hero-image" data-photo="cabinet_hero"></div>
            </div>
            <div class="facts">
                <div class="fact"><span>Время</span>40–75 минут</div>
                <div class="fact"><span>Адрес</span>Оренбург, ТД «Вояж»</div>
                <div class="fact"><span>Рейтинг</span>4.7 на Яндекс Картах</div>
            </div>
        </div>
    </section>

    <section class="about" id="about">
        <div class="container">
            <div class="section-label">О студии</div>
            <h2 class="section-title">Воздух, свет и скорость</h2>
            <div class="about-content">
                <div class="about-image" data-photo="cabinet_about"></div>
                <div class="about-text">
                    <p>«На ногтях» — это небольшая студия в центре Оренбурга, где маникюр и педикюр занимают от 40 до 75 минут. Мы не растягиваем процедуру на полдня и не заставляем ждать: вы приходите к назначенному времени, а уходите с аккуратным покрытием, которое держится неделями.</p>
                    <p>Кабинет наполнен светом: с двух сторон панорамные окна, белые тюли и мраморные вставки. Здесь нет спешки и суеты — только спокойная атмосфера, в которой приятно провести обеденный перерыв или вечер после работы.</p>
                    <p>Мы внимательно относимся к стерильности: инструменты проходят полную обработку, материалы — только проверенных брендов. Педикюр делаем так же тщательно, как маникюр, уделяя внимание каждой детали.</p>
                    <p>К нам приходят за скоростью, качеством и атмосферой — и возвращаются снова. Убедитесь сами: запишитесь онлайн или напишите в Max, и мы подберём удобное время.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="features" id="features">
        <div class="container">
            <div class="section-label">Почему нас выбирают</div>
            <h2 class="section-title">Три причины</h2>
            <div class="features-grid">
                <div class="feature-item">
                    <div class="feature-num">01</div>
                    <h3>Скорость</h3>
                    <p>Маникюр за 40–75 минут — успеваете в обеденный перерыв.</p>
                </div>
                <div class="feature-item">
                    <div class="feature-num">02</div>
                    <h3>Стерильность</h3>
                    <p>Инструменты проходят полную обработку, материалы — проверенных брендов.</p>
                </div>
                <div class="feature-item">
                    <div class="feature-num">03</div>
                    <h3>Кабинет</h3>
                    <p>Светлое пространство с панорамными окнами и мрамором.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="services" id="services">
        <div class="container">
            <div class="section-label">Прайс-лист</div>
            <h2 class="section-title">Услуги и цены</h2>

            <div class="tabs">
                <button class="tab-btn active" data-tab="manicure">Маникюр</button>
                <button class="tab-btn" data-tab="pedicure">Педикюр</button>
                <button class="tab-btn" data-tab="complex">Комплексы</button>
            </div>

            <div class="tab-panel active" id="tab-manicure">
                <div class="service-row">
                    <div class="service-thumb" data-photo="man_ukrep"></div>
                    <div class="service-info">
                        <span class="name">Маникюр + укрепление гелем</span>
                        <span class="meta">1 ч 30 мин · Комбинированный маникюр с укреплением гелем и покрытием гель-лак</span>
                    </div>
                    <span class="price">1 600 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="man_gig"></div>
                    <div class="service-info">
                        <span class="name">Гигиенический маникюр</span>
                        <span class="meta">30 мин</span>
                    </div>
                    <span class="price">700–800 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="man_french"></div>
                    <div class="service-info">
                        <span class="name">Маникюр + гель-лак + френч</span>
                        <span class="meta">1 ч 30 мин · Комбинированный маникюр, укрепление гелем, дизайн френч</span>
                    </div>
                    <span class="price">1 800 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="man_design"></div>
                    <div class="service-info">
                        <span class="name">Маникюр + покрытие + дизайн</span>
                        <span class="meta">1 ч 40 мин</span>
                    </div>
                    <span class="price">1 650–2 000 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="man_muzh"></div>
                    <div class="service-info">
                        <span class="name">Мужской маникюр</span>
                        <span class="meta">1 ч</span>
                    </div>
                    <span class="price">700 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="man_snyatie"></div>
                    <div class="service-info">
                        <span class="name">Снятие покрытия</span>
                        <span class="meta">30 мин</span>
                    </div>
                    <span class="price">200 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="man_snyatie_gig"></div>
                    <div class="service-info">
                        <span class="name">Снятие покрытия + гигиенический маникюр</span>
                        <span class="meta">1 ч</span>
                    </div>
                    <span class="price">800 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="man_model"></div>
                    <div class="service-info">
                        <span class="name">Моделирование (исправление клюющих и скрученных ногтей)</span>
                        <span class="meta">2 ч</span>
                    </div>
                    <span class="price">1 800–2 000 ₽</span>
                </div>
            </div>

            <div class="tab-panel" id="tab-pedicure">
                <div class="service-row">
                    <div class="service-thumb" data-photo="ped_uhod"></div>
                    <div class="service-info">
                        <span class="name">Аппаратный педикюр + уход</span>
                        <span class="meta">1 ч 30 мин</span>
                    </div>
                    <span class="price">1 800 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="ped_pokrytie"></div>
                    <div class="service-info">
                        <span class="name">Аппаратный педикюр + покрытие гель-лаком</span>
                        <span class="meta">1 ч</span>
                    </div>
                    <span class="price">2 100 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="ped_express"></div>
                    <div class="service-info">
                        <span class="name">Экспресс педикюр</span>
                        <span class="meta">30 мин</span>
                    </div>
                    <span class="price">1 200 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="ped_express_pokrytie"></div>
                    <div class="service-info">
                        <span class="name">Экспресс педикюр с покрытием гель-лак</span>
                        <span class="meta">45 мин</span>
                    </div>
                    <span class="price">1 500 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="ped_muzh"></div>
                    <div class="service-info">
                        <span class="name">Мужской педикюр</span>
                        <span class="meta">1 ч</span>
                    </div>
                    <span class="price">2 000 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="ped_snyatie"></div>
                    <div class="service-info">
                        <span class="name">Снятие покрытия</span>
                        <span class="meta">20 мин</span>
                    </div>
                    <span class="price">200 ₽</span>
                </div>
                <div class="service-row">
                    <div class="service-thumb" data-photo="ped_snyatie_express"></div>
                    <div class="service-info">
                        <span class="name">Снятие покрытия + экспресс педикюр</span>
                        <span class="meta">45 мин</span>
                    </div>
                    <span class="price">1 300 ₽</span>
                </div>
            </div>

            <div class="tab-panel" id="tab-complex">
                <div class="complexes-grid">
                    <div class="complex-card">
                        <div class="complex-thumb" data-photo="cx_s"></div>
                        <h4>S</h4>
                        <div class="desc">Маникюр + покрытие и педикюр пальчиков с покрытием</div>
                        <div class="price">3 100 ₽</div>
                    </div>
                    <div class="complex-card">
                        <div class="complex-thumb" data-photo="cx_m"></div>
                        <h4>M</h4>
                        <div class="desc">Моделирование и экспресс педикюр с покрытием</div>
                        <div class="price">3 300–3 500 ₽</div>
                    </div>
                    <div class="complex-card">
                        <span class="badge">Популярный</span>
                        <div class="complex-thumb" data-photo="cx_l"></div>
                        <h4>L</h4>
                        <div class="desc">Маникюр с укреплением и полный педикюр с покрытием</div>
                        <div class="price">3 700 ₽</div>
                    </div>
                    <div class="complex-card">
                        <div class="complex-thumb" data-photo="cx_xl"></div>
                        <h4>XL</h4>
                        <div class="desc">Моделирование и полный педикюр с покрытием</div>
                        <div class="price">3 900–4 100 ₽</div>
                    </div>
                </div>
            </div>

            <div class="services-cta">
                <a href="https://n1348500.yclients.ru/" class="btn" target="_blank" rel="noopener">Записаться</a>
                <a href="https://n1348500.yclients.ru/" class="full-price" target="_blank" rel="noopener">Полный прайс на странице записи</a>
            </div>
        </div>
    </section>

    <section class="portfolio" id="portfolio">
        <div class="container">
            <div class="section-label">Галерея</div>
            <h2 class="section-title">Наши работы</h2>
            <div class="portfolio-grid">
                <div class="portfolio-item" data-photo="work_1"></div>
                <div class="portfolio-item" data-photo="work_2"></div>
                <div class="portfolio-item" data-photo="work_3"></div>
                <div class="portfolio-item" data-photo="work_4"></div>
                <div class="portfolio-item" data-photo="work_5"></div>
                <div class="portfolio-item" data-photo="work_6"></div>
            </div>
        </div>
    </section>

    <section class="reviews" id="reviews">
        <div class="container">
            <div class="section-label">Доверие</div>
            <h2 class="section-title">Отзывы</h2>
            <div class="reviews-rating">
                <div class="num">4.7</div>
                <div class="sub">16 отзывов на Яндекс Картах</div>
            </div>
            <div class="reviews-grid">
                <div class="review-card">
                    <div class="review-head"><span class="review-name">Гульнара Крушенова</span><span class="review-status">Знаток города 2 уровня</span></div>
                    <div class="review-text">Мастер Светлана — настоящий профессионал! Маникюр выполнен безупречно: кутикула обработана идеально, покрытие ровное, без затёков, форма ногтей подобрана грамотно. Все инструменты стерильны, срок носки ногтей четыре недели. Очень довольна, рекомендую мастера!</div>
                </div>
                <div class="review-card">
                    <div class="review-head"><span class="review-name">Татьяна Мазалова</span><span class="review-status">Знаток города 2 уровня</span></div>
                    <div class="review-text">Наконец-то я нашла своего мастера — это Светлана! Стоит отметить аккуратность, вежливость, чуткость и профессиональный уровень этого мастера. Светлана всегда готова предложить новое и подсказать что-то по уходу за ногтями. Скоро Новый год, приходите в эту студию к Светлане, успех гарантирован!</div>
                </div>
                <div class="review-card">
                    <div class="review-head"><span class="review-name">Катя С.</span><span class="review-status">Знаток города 3 уровня</span></div>
                    <div class="review-text">Сегодня посетила салон красоты, мастера по маникюру Светлану. Ноготочки были обработаны быстро и качественно. Рекомендую. При первом посещении цена была снижена, что очень приятно. Мастер тактична и доброжелательна, можно посоветоваться. Спасибо.</div>
                </div>
            </div>
            <div class="reviews-cta">
                <a href="https://yandex.ru/maps/org/na_nogtyakh/110317468223/" target="_blank" rel="noopener">Все отзывы на Яндекс Картах</a>
            </div>
        </div>
    </section>

    <section class="booking">
        <div class="container">
            <h2>Запишитесь на удобное время</h2>
            <p>Онлайн-запись открыта круглосуточно.</p>
            <div class="booking-actions">
                <a href="https://n1348500.yclients.ru/" class="btn" target="_blank" rel="noopener">Записаться онлайн</a>
                <a href="https://max.ru/u/f9LHodD0cOJ-bX6hYDR-apIXmyZo1_Ld9ZYwm9eiteKL6U75nrNiCPIacWo" class="link-max" target="_blank" rel="noopener">Написать в Max</a>
                <a href="tel:+79619436282" class="link-max">+7 (961) 943-62-82</a>
            </div>
        </div>
    </section>

    <section class="contacts" id="contacts">
        <div class="container">
            <div class="section-label">Где нас найти</div>
            <h2 class="section-title">Контакты</h2>
            <div class="contacts-inner">
                <div>
                    <div class="contact-block">
                        <strong>Адрес</strong>
                        <p>Оренбург, ул. Карагандинская, 49/1<br>ТД «Вояж»</p>
                    </div>
                    <div class="contact-block">
                        <strong>Часы работы</strong>
                        <p>Ежедневно 10:00–20:00</p>
                    </div>
                    <div class="contact-block">
                        <strong>Телефон</strong>
                        <p><a href="tel:+79619436282">+7 (961) 943-62-82</a></p>
                    </div>
                    <div class="contact-block">
                        <strong>Онлайн-запись</strong>
                        <a href="https://n1348500.yclients.ru/" class="btn" target="_blank" rel="noopener">Записаться на приём</a>
                    </div>
                </div>
                <div class="map-wrap">
                    <iframe src="https://yandex.ru/map-widget/v1/?ll=55.155543%2C51.784616&z=16.99&pt=55.155543,51.784616,pm2rdm" loading="lazy" title="Карта: На ногтях, Оренбург" allowfullscreen></iframe>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container footer-inner">
            <a href="#" class="logo">На ногтях</a>
            <div><a href="tel:+79619436282">+7 (961) 943-62-82</a></div>
            <div>&copy; {{ year }} «На ногтях». Все права защищены.</div>
        </div>
    </footer>

    <a href="https://n1348500.yclients.ru/" class="sticky-book" target="_blank" rel="noopener">Записаться</a>

    <script>
        document.querySelectorAll('.tab-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var tab = btn.getAttribute('data-tab');
                document.querySelectorAll('.tab-btn').forEach(function (b) { b.classList.remove('active'); });
                document.querySelectorAll('.tab-panel').forEach(function (p) { p.classList.remove('active'); });
                btn.classList.add('active');
                document.getElementById('tab-' + tab).classList.add('active');
            });
        });

        fetch('/api/photos').then(function (r) { return r.json(); }).then(function (photos) {
            document.querySelectorAll('[data-photo]').forEach(function (el) {
                var key = el.getAttribute('data-photo');
                if (photos[key]) {
                    el.innerHTML = '<img src="/uploads/' + photos[key] + '" alt="' + key + '">';
                }
            });
        }).catch(function () {});
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_PAGE, year=datetime.now().year)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
