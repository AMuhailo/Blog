# 📝 Django Blog
[![Django](https://img.shields.io/badge/Django-5.1.6-darkgreen?style=for-the-badge)](https://www.djangoproject.com/)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)

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

## 📌 Installation and launch
```bash
git clone https://github.com/AMuhailo/Blog.git
cd Blog

python -m venv venv
source venv/bin/activate # for Linux/macOS
venv\Scripts\activate  # for Windows

pip install -r requirements.txt 
python manage.py migrate
python manage.py runserver
```


## 📈 Connect Redis
- **Open a new terminal to create a __docker container__**
```bash
docker pull redis
```
> You have created a docker container for __Redis__, now you need to run it.

- **Open a new terminal for running redis server**
```bash
docker run -it --rm --name redis -p 6379:6379 redis
```
> You run redis server.Nice!

## 📊 Launch Celery Worker
- **Open a new terminal for launch Celery**
```bash
celery -A myblog worker -E -i INFO
or 
celery -A myblog worker --pool=solo --loglevel=info
```

- **Open a new terminal for launch Flower**
```bash
celery -A myblog.celery_app flower
```

- **Open a new terminal for launch Beat**
```bash
celery -A myblog beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```