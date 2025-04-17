# Django Mini Blog

A simple blog application built with Django that allows users to create, read, update, and delete blog posts. Features include user authentication, comments, likes/dislikes, and a search functionality.

## Features

- User Authentication (Register, Login, Logout)
- Create, Read, Update, and Delete Blog Posts
- Comments on Blog Posts
- Like/Dislike Posts
- Search Posts by Title, Content, or Author
- User Profiles
- Responsive Design with Bootstrap
- Share Posts via URL

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/django-mini-blog.git
cd django-mini-blog
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/ in your browser

## Technologies Used

- Python 3.x
- Django 4.2
- Bootstrap 5
- Font Awesome
- SQLite (default database)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 