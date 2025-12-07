# **📌 Backend API for Job Assistant Platform**

This repository contains the backend service for the **Job Assistant Platform** — an AI-powered system that helps users create resumes, analyze them, and receive vacancy recommendations from different job platforms (hh.ru, internal parsing sources, and AI scoring pipelines).

Backend is designed as a stateless API and communicates with a Telegram bot and with the automation platform (n8n).

---

## **🚀 Core Features**

### **1️⃣ User Profile Management**

Users fill a short profile through the Telegram bot.
The backend stores the following fields:

* First name
* Last name
* Age
* City
* Email
* Phone
* Telegram ID
* HH.ru profile URL (optional)

**Endpoints:**

* `POST /users/` — create or update user
* `GET /users/{telegram_id}` — return saved profile

---

### **2️⃣ Resume Management**

Users can create resumes in **three ways**:

#### ✔ Manual resume creation

The bot collects:

* Current position
* Desired position
* Years of experience
* Skills
* Preferred salary
* Preferred region
* Languages
* Education level

**Backend Endpoint:**

* `POST /resume/json/{telegram_id}` — save resume JSON

---

#### ✔ Resume file upload

User uploads `.pdf` or `.docx` via Telegram.

**Backend Endpoint:**

* `POST /resume/file/{telegram_id}`
  Saves file → forwards to n8n → performs parsing and skill extraction.

---

#### ✔ Automatic import from hh.ru (OAuth 2.0) — coming next

After receiving API access, backend will support:

* Obtaining access token
* Fetching user’s hh.ru resumes
* Parsing experience, skills, salary, region

**Planned Endpoint:**

* `GET /hh/import?telegram_id=123&code=oauth_code`

---

### **3️⃣ Vacancy Search Pipeline**

The search request is triggered by the Telegram bot:

**Process:**

1. Bot calls `POST /search/start/{telegram_id}`
2. Backend sends full user resume to n8n
3. n8n searches on hh.ru API + internal sources
4. n8n ranks vacancies with AI
5. Backend exposes next vacancy for the bot

**Endpoints:**

* `POST /search/start/{telegram_id}` — start pipeline
* `GET /search/next/{telegram_id}` — return next recommended vacancy
* `GET /search/details/{telegram_id}/{vacancy_id}` — full vacancy details

---

### **4️⃣ Vacancy Recommendation System**

Backend communicates with:

* **n8n** workflow for gathering vacancies
* **AI scoring module** (planned)
* **Redis** (optional) for caching vacancy queues per user

Vacancy format includes:

* Title
* Company
* Salary
* Short responsibilities
* Skills match %
* Vacancy ID (for details)

---

## **🛠 Tech Stack**

* **Python 3.10+**
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **Redis (optional)** — queue for vacancy recommendations
* **n8n** — automation & scraping
* **hh.ru API** (OAuth 2.0)
* **Docker** (deployment)

---

## **📁 Project Structure**

```
backend/
│── app/
│   ├── models/            # SQLAlchemy models (User, Resume, SearchQueue)
│   ├── routers/           # API routers: users, resume, search, hh
│   ├── services/          # hh.ru client, n8n client, parsing utils
│   ├── db/                # database session & config
│   └── main.py            # FastAPI app
│
│── migrations/            # Alembic migrations
│── README.md
│── requirements.txt
│── Dockerfile
```

---

## **📌 API Overview**

### **User**

| Method | Endpoint               | Description           |
| ------ | ---------------------- | --------------------- |
| POST   | `/users/`              | Create or update user |
| GET    | `/users/{telegram_id}` | Get user profile      |

---

### **Resume**

| Method | Endpoint                     | Description        |
| ------ | ---------------------------- | ------------------ |
| POST   | `/resume/json/{telegram_id}` | Save manual resume |
| POST   | `/resume/file/{telegram_id}` | Upload resume file |
| GET    | `/resume/{telegram_id}`      | Get resume         |

---

### **Search**

| Method | Endpoint                                     | Description          |
| ------ | -------------------------------------------- | -------------------- |
| POST   | `/search/start/{telegram_id}`                | Start vacancy search |
| GET    | `/search/next/{telegram_id}`                 | Get next vacancy     |
| GET    | `/search/details/{telegram_id}/{vacancy_id}` | Vacancy details      |

---

### **hh.ru Integration**

| Method | Endpoint        | Description                       |
| ------ | --------------- | --------------------------------- |
| GET    | `/hh/auth_link` | Generate OAuth login URL          |
| GET    | `/hh/import`    | Import resume after authorization |

---

## **🔐 Authentication & Security**

Since all requests come from Telegram bot, authentication is based on:

* Internal secret header `X-BOT-KEY`
* Telegram ID mapping

Later:

* JWT for web clients
* OAuth for hh.ru user login

---

## **📦 Deployment**

### Local:

```
uvicorn app.main:app --reload
```

### Docker:

```
docker compose up --build
```

---

## **📘 Future Improvements Roadmap**

### 🔜 Phase 1 — hh.ru Integration

* Auto-import resume via hh API
* Sync experience, skills, salary
* Match vacancy history

### 🔜 Phase 2 — AI Assistant

* Vacancy ranking by similarity
* Resume quality score
* Recommendations (skills to add, courses, missing keywords)

### 🔜 Phase 3 — User Dashboard (Web)

* Log in with Telegram
* View/edit resume
* Track vacancy matches
* Statistics & insights