# 📝 Django Blog
![Django](https://img.shields.io/badge/Django-5.1.6-blue?style=for-the-badge) 
![Python](https://img.shields.io/badge/Python-3.12-yellow?style=for-the-badge)

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

## 📌 Installation and launch
```bash
git clone https://github.com/AMuhailo/Blog.git
cd Blog

python -m venv venv
source venv/bin/activate # для Linux/macOS
venv\Scripts\activate  # для Windows

pip install -r requirements.txt 
python manage.py migrate
python manage.py runserver
```

## 📊 Launch Celery Worker
- **Open new terminal for launch Celery**
```bash
celery -A myblog worker -E -i INFO
or 
celery -A myblog worker --pool=solo --loglevel=info
```
- **Open new terminal for launch Flower**
```bash
celery -A myblog.celery_app flower
```
- **Open new terminal for launch Beat**
```bash
celery -A myblog beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
## 👨‍💻 Author: Mikhail Ishkov