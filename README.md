**Project**: Django Authentication & Todo API

- **Description**: Minimal Django project providing user signup (email-based auth), JWT authentication, and a simple todo app. It uses PostgreSQL for persistence, Redis as the Celery broker, and Celery for background tasks (email sending, OTP cleanup).

**Prerequisites**
- **Python**: 3.10+ (virtual environment recommended)
- **Docker & Docker Compose**: to run PostgreSQL and Redis locally (optional but recommended)
- **Git**: to clone the repository (optional if you already have the sources)

**Quick start (recommended - using Docker Compose for DB + Redis)**
1. From the project root open a terminal (PowerShell recommended on Windows).
2. Start PostgreSQL and Redis:

```powershell
docker-compose up -d
```

The repo ships `docker-compose.yaml` that defines two services:
- `postgres-db` (Postgres, DB name `auth_db`, user `master`, password `12345678`) on port `5432`
- `redis` (Redis broker) on port `6379`

3. Create and activate a virtual environment, then install Python dependencies:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1   # PowerShell
pip install --upgrade pip
pip install -r requirements.txt
```

4. (Optional) If you won't use Docker you must ensure a PostgreSQL instance is available and match the settings in `auth/settings.py` (`DB NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`) or change them accordingly.

5. Apply migrations and create a superuser:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

6. Run the development server:

```powershell
python manage.py runserver 0.0.0.0:8000
```

7. Start Celery worker (in a separate terminal) and Celery beat for scheduled tasks:

```powershell
# from project root, with the same virtualenv activated
celery -A auth worker --loglevel=info
# and in another terminal (beat scheduler)
celery -A auth beat --loglevel=info
```

Notes: Celery broker URL is set to `redis://localhost:6379/0` by default (see `auth/settings.py`).

**Environment & Credentials**
- `auth/settings.py` contains several values currently hard-coded for development (e.g., `SECRET_KEY`, DB credentials, Gmail SMTP settings, JWT keys). For production you should move these into environment variables or a .env file and load them securely.
- The SMTP settings in `auth/settings.py` are configured for Gmail. If you plan to actually send email, update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`, or use a local email testing tool (e.g., `mailhog`) for development.

**Running with only Python (no Docker)**
- Ensure PostgreSQL and Redis are running and accessible from your machine and that `auth/settings.py` is updated to point to them.
- Then follow steps 3-7 above.

**Running tests**

```powershell
python manage.py test
```

**Project structure (high level)**
- `manage.py`: Django CLI entrypoint.
- `auth/`: Django project settings and WSGI/ASGI/celery entrypoints. See [auth/settings.py](auth/settings.py) and [auth/celery.py](auth/celery.py#L1-L50).
- `signup/`: App implementing custom `User` model, signup flow, OTP handling, and email-sending Celery tasks (see [signup/tasks.py](signup/tasks.py#L1-L200)).
- `todo/`: A simple todo app (models, serializers, views) used as an example protected resource.

**Key files**
- [manage.py](manage.py#L1)
- [requirements.txt](requirements.txt#L1-L200)
- [docker-compose.yaml](docker-compose.yaml#L1-L200)
- [auth/settings.py](auth/settings.py#L1-L400)
- [auth/celery.py](auth/celery.py#L1-L50)
- [signup/tasks.py](signup/tasks.py#L1-L200)

**Troubleshooting / Tips**
- If you see DB connection errors, confirm Postgres is running and that `HOST`/`PORT` in `auth/settings.py` match your environment. The provided `docker-compose.yaml` exposes Postgres on `localhost:5432`.
- For Celery task failures, confirm Redis is running and reachable at `redis://localhost:6379/0`.
- If email sending fails during development, either provide valid SMTP credentials or switch Django's `EMAIL_BACKEND` to `django.core.mail.backends.console.EmailBackend` to print emails to console.

**Security reminder**
This repository currently contains secrets (e.g., `SECRET_KEY`, SMTP password) in plain text inside `auth/settings.py`. Do NOT use these values in production. Move secrets to environment variables and rotate them.

**Next steps & improvements**
- Replace hard-coded credentials with environment-based configuration (e.g., using `python-dotenv` or Django-environ).
- Add a `Makefile` or scripts for common tasks (`setup`, `start`, `stop`, `test`).
- Add CI workflow to run tests and linters.

If you want, I can now (1) replace secrets with environment variable usage and add a sample `.env.example`, or (2) run the project tests here. Which would you like me to do next?
