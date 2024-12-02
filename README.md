# **RippleBytes Discord Bot**

This project is a Django-based Discord bot designed to handle user check-ins, check-outs, break management, and task tracking. It includes database integration (PostgreSQL) and is ready for production deployment using Docker Compose.

---

## **Features**
- **User Check-in/Check-out**: Log user sessions with tasks and timestamps.
- **Break Management**: Track breaks with reasons and timestamps.
- **Task Tracking**: Record tasks with a multi-line input for flexible management.
- **Discord Modal Integration**: User-friendly dialogs for data input.
- **Database Integration**: Stores all data in PostgreSQL.
- **Production-ready**: Deployable with Docker and Docker Compose.

---

## **Technologies Used**
- **Backend Framework**: Django 4.x
- **Database**: PostgreSQL
- **Bot Framework**: Discord.py 2.x
- **Deployment**: Docker, Docker Compose
- **Static File Management**: Whitenoise (for serving static files in production)

---

## **Prerequisites**
Before running the project, ensure you have the following installed:
- Docker and Docker Compose
- Python 3.11+
- PostgreSQL (optional, for local development)
- Discord Developer Account (for bot token)

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/discord-django-bot.git
cd discord-django-bot
```

### **2. Create `.env` File**
Create a `.env` file in the project root and populate it with the following variables:

```env
# Django settings
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token

# PostgreSQL settings
POSTGRES_DB=office_bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

### **3. Build and Run with Docker Compose**
1. **Build the Services**:
   ```bash
   docker-compose up --build -d
   ```
2. **Check Logs**:
   ```bash
   docker-compose logs -f
   ```

---

### **4. Run Django Migrations**
Ensure the database schema is created:
```bash
docker-compose exec bot python manage.py migrate
```

---

### **5. Collect Static Files**
For the admin interface to work correctly:
```bash
docker-compose exec bot python manage.py collectstatic --noinput
```

---

### **6. Access the Bot**
- The bot runs on your Discord server. Add it using your Discord bot token.
- For the Django admin panel, visit `http://127.0.0.1:8000/admin`.

---

## **Project Structure**
```plaintext
discord-django-bot/
│
├── bot/                     # Main Django app
│   ├── management/          # Custom management commands
│   ├── migrations/          # Database migrations
│   ├── models.py            # Database models
│   ├── views.py             # Bot logic
│   ├── tasks.py             # Task tracking logic
│   └── admin.py             # Admin interface
│
├── staticfiles/             # Collected static files
├── templates/               # HTML templates
├── manage.py                # Django entry point
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── .env                     # Environment variables (ignored in .gitignore)
```

---

## **Environment Variables**
- **`DJANGO_SECRET_KEY`**: The secret key for the Django app.
- **`DISCORD_TOKEN`**: Your Discord bot token.
- **`POSTGRES_DB`**: Database name.
- **`POSTGRES_USER`**: Database username.
- **`POSTGRES_PASSWORD`**: Database password.
- **`DJANGO_ALLOWED_HOSTS`**: Hosts allowed to serve the app (comma-separated).

---

## **Common Commands**

### **Run Server**
For development (non-Docker):
```bash
python manage.py runserver
```

### **Run Bot**
```bash
python manage.py runbot
```

### **Run Tests**
```bash
python manage.py test
```

### **Stop Services**
```bash
docker-compose down
```

---

## **Production Deployment**
- Use Docker Compose for production deployment.
- Configure a reverse proxy (e.g., Nginx) for handling static files and requests.
- Ensure environment variables in `.env` are correctly set.

---

## **Troubleshooting**

1. **Admin CSS Not Loading**:
   - Run `python manage.py collectstatic` to collect static files.
   - Use Whitenoise or Nginx to serve static files in production.

2. **Database Connection Issues**:
   - Verify `.env` file has correct database settings.
   - Ensure PostgreSQL container is running.

3. **Bot Not Responding**:
   - Check the Discord bot token in `.env`.
   - Ensure the bot is added to your Discord server.

---

## **Contributing**
Feel free to submit issues or pull requests to improve this project.
