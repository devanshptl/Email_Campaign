#  Email Campaign Manager – Django + Celery + Redis

A production-ready Email Campaign Manager built with **Django**, **Celery**, and **Redis**. This system supports subscriber management, campaign creation, scheduled email delivery via SMTP, unsubscribe functionality, and performance optimization via multithreaded dispatch.

---

##  Features

-  Add subscribers via API or Django admin
-  Unsubscribe endpoint with `is_active=False` logic
-  Admin support for creating email campaigns
-  Campaign model with: `subject`, `preview_text`, `article_url`, `html_content`, `plain_text_content`, `published_date`
-  SMTP integration
-  Parallel email dispatch using `ThreadPoolExecutor`
- Render email content using Django HTML templates
- Asynchronous task execution using Celery + Redis
- `.env` support for credentials and settings

---


##  Installation

### 1. Clone the Repository

```bash
git clone https://github.com/devanshptl/Email_Campaign.git
cd Email_campaign
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Setup `.env` File

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit it to include your  SMTP credentials.

---

##  Running the Project

### 1. Start Redis Server

```bash
redis-server
```

### 2. Apply Migrations & Create Superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Start Django Server

```bash
python manage.py runserver
```

### 4. Start Celery Worker

```bash
celery -A Email_campaign worker -l info
```

---

## Sending Campaign Emails

Campaigns scheduled with `published_date = today` will be dispatched using:

### Option 1: Django Management Command

```bash
python manage.py send_campaigns
```

### Option 2: Call Celery Task

```python
from campaign.tasks import send_daily_campaign
send_daily_campaign.delay()
```
### Option 3: It will send campaigns on 7:30 am IST Everyday
---

##  API Endpoints

- `POST /api/subscribe/`  
  Add a new subscriber

- `POST /api/unsubscribe/`  
  Mark subscriber as inactive

---

##  Sample `.env.example`

```ini
DEFAULT_FROM_EMAIL=your@mail.com
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=postmaster@sandboxXXX.mailgun.org
EMAIL_HOST_PASSWORD=your-mailgun-password
```

---

##  Sample Template: `email_template.html`

```html
<h2>{{ subject }}</h2>
<p>{{ preview_text }}</p>
<a href="{{ article_url }}">Read full article</a>
<p>If you wish to unsubscribe, click <a href="{{ unsubscribe_link }}">here</a>.</p>
```

---


