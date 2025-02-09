# 📝 Django Blog
![Django](https://img.shields.io/badge/Django-4.2-blue?style=for-the-badge) 
![Python](https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge)

## 🚀 Functionality
✔️ User registration
✔️ CRUD operations on posts
✔️ Sending emails
✔️ Followers, views, and likes  features
✔️ Showing actions performed by the user
✔️ Adding content to a post

## 🛠️ Technologies
- **Django**
- **PostgreSQL**
- **Celery + Redis**
- **Celery + Flower + Beat**
- **Cloudinary**
- **Docker**
- **Railway**

## 📌 Встановлення та запуск
```bash
git clone https://github.com/AMuhailo/Blog.git
cd Blog

python -m venv venv
source venv/bin/activate # для Linux/macOS
venv\Scripts\activate  # для Windows

pip install -r requirements.txt 
python manage.py migrate
python manage.py runserver