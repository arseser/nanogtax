from flask import Flask, render_template_string

app = Flask(__name__)

# Сюда мы вставляем весь ваш HTML-код
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>На ногтях — маникюр и педикюр в Оренбурге</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #3a3a3a; background-color: #ffffff; line-height: 1.6; }
        .container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }

        /* Шапка */
        header { background: #fff; border-bottom: 1px solid #e0e0e0; padding: 20px 0; position: sticky; top: 0; z-index: 100; }
        .header-inner { display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 1.5rem; font-weight: 600; letter-spacing: 2px; color: #3a3a3a; text-transform: uppercase; }
        .logo span { color: #b0a8a0; }
        nav a { text-decoration: none; color: #3a3a3a; margin-left: 30px; font-size: 0.95rem; transition: color 0.3s; }
        nav a:hover { color: #b0a8a0; }
        .btn-book { background-color: #3a3a3a; color: #fff !important; padding: 10px 25px; border-radius: 50px; font-weight: 500; transition: background 0.3s; }
        .btn-book:hover { background-color: #b0a8a0; }

        /* Главный экран */
        .hero { padding: 100px 0; text-align: center; background: linear-gradient(135deg, #ffffff 0%, #f5f3f0 100%); }
        .hero h1 { font-size: 3rem; font-weight: 300; margin-bottom: 20px; color: #3a3a3a; }
        .hero h1 strong { font-weight: 600; color: #b0a8a0; }
        .hero p { font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto 40px; }
        .hero .btn-book { padding: 15px 40px; font-size: 1.1rem; display: inline-block; text-decoration: none; }

        /* О нас */
        .about { padding: 80px 0; background: #fff; }
        .about h2 { text-align: center; font-size: 2rem; font-weight: 400; margin-bottom: 50px; color: #3a3a3a; }
        .about-content { display: flex; flex-wrap: wrap; gap: 40px; align-items: center; }
        .about-text { flex: 1 1 500px; }
        .about-text p { margin-bottom: 20px; color: #555; font-size: 1.1rem; }
        .about-text p strong { color: #3a3a3a; }
        .about-text .btn-book { display: inline-block; margin-top: 20px; padding: 15px 40px; text-decoration: none; }
        .about-image { flex: 1 1 400px; background: #e8e4e0; height: 350px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 0.9rem; }

        /* Преимущества */
        .features { padding: 80px 0; background: #f9f8f7; }
        .features h2 { text-align: center; font-size: 2rem; font-weight: 400; margin-bottom: 50px; color: #3a3a3a; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }
        .feature-item { background: #fff; padding: 40px 30px; text-align: center; border-radius: 10px; transition: transform 0.3s; }
        .feature-item:hover { transform: translateY(-5px); }
        .feature-icon { font-size: 2.5rem; margin-bottom: 20px; }
        .feature-item h3 { font-weight: 500; margin-bottom: 10px; color: #3a3a3a; }
        .feature-item p { color: #666; font-size: 0.95rem; }

        /* Услуги */
        .services { padding: 80px 0; background: #f5f3f0; }
        .services h2 { text-align: center; font-size: 2rem; font-weight: 400; margin-bottom: 50px; color: #3a3a3a; }
        .services-category { margin-bottom: 40px; }
        .services-category h3 { font-size: 1.5rem; font-weight: 500; color: #b0a8a0; margin-bottom: 20px; border-bottom: 2px solid #b0a8a0; padding-bottom: 10px; }
        .service-row { display: flex; justify-content: space-between; align-items: baseline; padding: 15px 0; border-bottom: 1px solid #dcdcdc; font-size: 1.05rem; flex-wrap: wrap; gap: 10px; }
        .service-row .name { font-weight: 500; flex: 1 1 60%; }
        .service-row .meta { color: #999; font-size: 0.9rem; font-weight: 400; }
        .service-row .price { font-weight: 600; color: #b0a8a0; white-space: nowrap; }
        .service-note { text-align: center; margin-top: 30px; color: #888; font-size: 0.9rem; }

        /* Портфолио */
        .portfolio { padding: 80px 0; background: #fff; }
        .portfolio h2 { text-align: center; font-size: 2rem; font-weight: 400; margin-bottom: 50px; color: #3a3a3a; }
        .portfolio-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .portfolio-item { background: #e8e4e0; height: 250px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 0.9rem; }

        /* Отзывы */
        .reviews { padding: 80px 0; background: #f9f8f7; text-align: center; }
        .reviews h2 { font-size: 2rem; font-weight: 400; margin-bottom: 20px; color: #3a3a3a; }
        .reviews p { font-size: 1.2rem; color: #666; }
        .reviews strong { color: #b0a8a0; }

        /* Контакты */
        .contacts { padding: 80px 0; background: #f5f3f0; }
        .contacts h2 { text-align: center; font-size: 2rem; font-weight: 400; margin-bottom: 50px; color: #3a3a3a; }
        .contacts-inner { display: flex; flex-wrap: wrap; justify-content: center; gap: 50px; text-align: center; }
        .contact-block { font-size: 1rem; }
        .contact-block strong { display: block; font-size: 1.2rem; margin-bottom: 10px; color: #3a3a3a; }
        .contact-block p { color: #666; }
        .contact-block a { color: #b0a8a0; text-decoration: none; }

        /* Подвал */
        footer { background: #3a3a3a; color: #ccc; text-align: center; padding: 30px 0; font-size: 0.9rem; }

        /* Адаптивность */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2rem; }
            nav a:not(.btn-book) { display: none; }
            .service-row { flex-direction: column; align-items: flex-start; }
            .service-row .price { margin-top: 5px; }
            .about-content { flex-direction: column; }
        }
    </style>
</head>
<body>

    <!-- Шапка -->
    <header>
        <div class="container header-inner">
            <div class="logo">На <span>ногтях</span></div>
            <nav>
                <a href="#about">О нас</a>
                <a href="#services">Услуги</a>
                <a href="#portfolio">Портфолио</a>
                <a href="#contacts">Контакты</a>
                <a href="https://n1348500.yclients.ru/" class="btn-book" target="_blank">Записаться</a>
            </nav>
        </div>
    </header>

    <!-- Главный экран -->
    <section class="hero">
        <div class="container">
            <h1>Идеальный маникюр и педикюр<br><strong>за 40–75 минут</strong></h1>
            <p>Скорость и качество без отслоек. Успейте даже в обеденный перерыв.</p>
            <a href="https://n1348500.yclients.ru/" class="btn-book" target="_blank">Записаться онлайн</a>
        </div>
    </section>

    <!-- О нас -->
    <section class="about" id="about">
        <div class="container">
            <h2>О нас</h2>
            <div class="about-content">
                <div class="about-text">
                    <p>Добро пожаловать в студию <strong>«На ногтях»</strong>! Мы находимся в самом центре Оренбурга, по адресу ул. Карагандинская, 49/1 (ТД «Вояж»).</p>
                    <p>Наш главный принцип — <strong>скорость и качество</strong>. Мы делаем маникюр всего за 40–75 минут, что позволяет вам успеть на встречу или вернуться на работу в обеденный перерыв. При этом покрытие радует глаз неделями — <strong>без отслоек и сколов</strong>.</p>
                    <p>Наш кабинет — это воздушное пространство с панорамными окнами и белыми тюлями, где преобладает белый цвет с вставками серого мрамора. Здесь приятно расслабиться и привести руки в порядок.</p>
                    <p>Мы также делаем педикюр — такой же быстрый и качественный, как маникюр. А для удобства наших клиентов доступна <strong>онлайн-запись</strong>.</p>
                    <a href="https://n1348500.yclients.ru/" class="btn-book" target="_blank">Записаться онлайн</a>
                </div>
                <div class="about-image">Фото кабинета</div>
            </div>
        </div>
    </section>

    <!-- Преимущества -->
    <section class="features" id="features">
        <div class="container">
            <h2>Почему выбирают нас</h2>
            <div class="features-grid">
                <div class="feature-item">
                    <div class="feature-icon">⚡</div>
                    <h3>Скорость</h3>
                    <p>Маникюр за 40–75 минут. Идеально для тех, кто ценит время.</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">💎</div>
                    <h3>Качество</h3>
                    <p>Покрытие без отслоек. Проверено временем и клиентами.</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✨</div>
                    <h3>Атмосфера</h3>
                    <p>Светлый, просторный кабинет с панорамными окнами.</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🦶</div>
                    <h3>Педикюр</h3>
                    <p>Такой же быстрый и качественный, как маникюр.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Услуги и цены -->
    <section class="services" id="services">
        <div class="container">
            <h2>Услуги и цены</h2>

            <div class="services-category">
                <h3>Маникюр</h3>
                <div class="service-row"><span class="name">Маникюр + укрепление гелем <span class="meta">(1 ч 30 мин)</span></span><span class="price">1 600 ₽</span></div>
                <div class="service-row"><span class="name">Гигиенический маникюр <span class="meta">(30 мин)</span></span><span class="price">700–800 ₽</span></div>
                <div class="service-row"><span class="name">Маникюр + гель-лак + френч <span class="meta">(1 ч 30 мин)</span></span><span class="price">1 800 ₽</span></div>
                <div class="service-row"><span class="name">Маникюр + покрытие + дизайн <span class="meta">(1 ч 40 мин)</span></span><span class="price">1 650–2 000 ₽</span></div>
                <div class="service-row"><span class="name">Мужской маникюр <span class="meta">(1 ч)</span></span><span class="price">700 ₽</span></div>
                <div class="service-row"><span class="name">Снятие покрытия <span class="meta">(30 мин)</span></span><span class="price">200 ₽</span></div>
                <div class="service-row"><span class="name">Снятие покрытия + гигиенический маникюр <span class="meta">(1 ч)</span></span><span class="price">800 ₽</span></div>
                <div class="service-row"><span class="name">Моделирование (исправление клюющих и скрученных ногтей) <span class="meta">(2 ч)</span></span><span class="price">1 800–2 000 ₽</span></div>
            </div>

            <div class="services-category">
                <h3>Педикюр</h3>
                <div class="service-row"><span class="name">Аппаратный педикюр + уход <span class="meta">(1 ч 30 мин)</span></span><span class="price">1 800 ₽</span></div>
                <div class="service-row"><span class="name">Аппаратный педикюр + покрытие гель-лаком <span class="meta">(1 ч)</span></span><span class="price">2 100 ₽</span></div>
                <div class="service-row"><span class="name">Экспресс педикюр <span class="meta">(30 мин)</span></span><span class="price">1 200 ₽</span></div>
                <div class="service-row"><span class="name">Экспресс педикюр с покрытием гель-лак <span class="meta">(45 мин)</span></span><span class="price">1 500 ₽</span></div>
                <div class="service-row"><span class="name">Дизайн <span class="meta">(30 мин)</span></span><span class="price">50–200 ₽</span></div>
                <div class="service-row"><span class="name">Мужской педикюр <span class="meta">(1 ч)</span></span><span class="price">2 000 ₽</span></div>
                <div class="service-row"><span class="name">Снятие покрытия <span class="meta">(20 мин)</span></span><span class="price">200 ₽</span></div>
                <div class="service-row"><span class="name">Снятие покрытия + экспресс педикюр <span class="meta">(45 мин)</span></span><span class="price">1 300 ₽</span></div>
            </div>

            <div class="services-category">
                <h3>Комплексы</h3>
                <div class="service-row"><span class="name">Комплекс S <span class="meta">(2 ч 15 мин) — Маникюр + покрытие и педикюр пальчиков с покрытием</span></span><span class="price">3 100 ₽</span></div>
                <div class="service-row"><span class="name">Комплекс M <span class="meta">(2 ч 45 мин) — Моделирование и экспресс педикюр с покрытием</span></span><span class="price">3 300–3 500 ₽</span></div>
                <div class="service-row"><span class="name">Комплекс L <span class="meta">(2 ч 30 мин) — Маникюр с укреплением и полный педикюр с покрытием</span></span><span class="price">3 700 ₽</span></div>
                <div class="service-row"><span class="name">Комплекс XL <span class="meta">(3 ч) — Моделирование и полный педикюр с покрытием</span></span><span class="price">3 900–4 100 ₽</span></div>
            </div>

            <p class="service-note">* Точные цены и полный прайс — на странице онлайн-записи.</p>
        </div>
    </section>

    <!-- Портфолио -->
    <section class="portfolio" id="portfolio">
        <div class="container">
            <h2>Наши работы</h2>
            <div class="portfolio-grid">
                <div class="portfolio-item">Здесь будет фото</div>
                <div class="portfolio-item">Здесь будет фото</div>
                <div class="portfolio-item">Здесь будет фото</div>
                <div class="portfolio-item">Здесь будет фото</div>
            </div>
        </div>
    </section>

    <!-- Отзывы -->
    <section class="reviews">
        <div class="container">
            <h2>Отзывы</h2>
            <p><strong>23 отзыва</strong> на Яндекс Картах — средняя оценка 4.7 ★</p>
        </div>
    </section>

    <!-- Контакты -->
    <section class="contacts" id="contacts">
        <div class="container">
            <h2>Контакты</h2>
            <div class="contacts-inner">
                <div class="contact-block">
                    <strong>Адрес</strong>
                    <p>Оренбург, ул. Карагандинская, 49/1<br>ТД «Вояж»</p>
                </div>
                <div class="contact-block">
                    <strong>Телефон</strong>
                    <p><a href="tel:+70000000000">+7 (000) 000-00-00</a></p>
                </div>
                <div class="contact-block">
                    <strong>Онлайн-запись</strong>
                    <p><a href="https://n1348500.yclients.ru/" target="_blank">Записаться на приём</a></p>
                </div>
            </div>
        </div>
    </section>

    <!-- Подвал -->
    <footer>
        <div class="container">
            &copy; 2025 «На ногтях». Все права защищены.
        </div>
    </footer>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(debug=True)
