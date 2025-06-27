# 🛍️ MenStyle — Интернет-магазин мужской одежды

**MenStyle** — это современный интернет-магазин стильной мужской одежды, разработанный на Django с использованием Tailwind CSS. Проект поддерживает корзину, просмотр товаров, фильтрацию и адаптивный дизайн.

---

## 🚀 Возможности

- 📦 Каталог с фильтрацией по цене, бренду и категориям
- 🖼️ Детальная страница товара
- 🛒 Корзина с добавлением и редактированием количества
- 👤 Сессии для гостей и авторизация
- 💡 Красивый UI на Tailwind CSS (через CDN)
- ⚙️ Админ-панель для управления товарами и заказами

---

## 🛠️ Установка

```bash
git clone https://github.com/NurikD/shop.git
cd shop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
