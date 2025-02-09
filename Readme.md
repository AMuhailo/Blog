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
## 👨‍💻 Author: Mikhail Ishkov