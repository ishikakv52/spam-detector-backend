# Smart Spam Message Detection System — Backend

Django + Django REST Framework backend for the BCA minor project.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env            # then edit .env:
#  - set DB_* to your local PostgreSQL credentials
#  - set GEMINI_API_KEY to your key from https://aistudio.google.com/app/apikey

createdb spam_detector          # or create it via psql/pgAdmin

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver         # http://localhost:8000
```

Run tests: `python manage.py test`

## API Endpoints

| Method | Endpoint                     | Auth | Description                          |
|--------|-------------------------------|------|---------------------------------------|
| POST   | /api/auth/register/           | No   | Create account                        |
| POST   | /api/auth/login/               | No   | Get {access, refresh} JWT tokens      |
| POST   | /api/auth/token/refresh/       | No   | Refresh access token                  |
| GET/PUT| /api/auth/profile/             | Yes  | View/update own profile               |
| GET    | /api/messages/                 | Yes  | List own messages (paginated)         |
| POST   | /api/messages/analyze/         | Yes  | Send text to Gemini, save + return result |
| GET    | /api/messages/{id}/            | Yes  | Message detail                        |
| PATCH  | /api/messages/{id}/            | Yes  | Update own notes                      |
| DELETE | /api/messages/{id}/            | Yes  | Delete a record                       |
| GET    | /api/dashboard/                | Yes  | Totals + spam % + recent messages     |

All JWT-authenticated endpoints expect: `Authorization: Bearer <access_token>`

## Architecture

```
config/            settings, root urls
apps/accounts/      register, login (JWT), profile
apps/detector/       constants -> validators -> models -> selectors -> services -> serializers -> views
  services.py        the only file that talks to Gemini
```
# spam-detector-backend
