# Telegram Career Bot — FastAPI Backend

Backend REST API for a Telegram bot that automates task and workflow management for a career center.  
Built with **FastAPI**, **MySQL**, **Pydantic (DTOs)**, and **pytest**.

> 💼 This project was developed during my internship at IT Career Hub GmbH (January–March 2026).

---

## Features

- ✅ Full CRUD for task management
- ✅ Status tracking: `pending` → `in_progress` → `done`
- ✅ Input validation with Pydantic DTOs
- ✅ Unit tests with pytest and mocked DB
- ✅ Auto-generated Swagger UI at `/docs`
- ✅ Environment-based DB config via `.env`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | MySQL |
| Validation | Pydantic v2 |
| Testing | pytest, httpx |
| Runtime | Python 3.11 |

---

## Project Structure

```
telegram-career-bot/
├── app/
│   ├── main.py        # FastAPI app, routes
│   ├── schemas.py     # Pydantic DTOs
│   └── database.py    # MySQL connection
├── tests/
│   └── test_tasks.py  # Unit tests
├── schema.sql         # DB setup
├── requirements.txt
└── .env.example
```

---

## Getting Started

### 1. Clone & install

```bash
git clone https://github.com/YeKnysh/telegram-career-bot.git
cd telegram-career-bot
pip install -r requirements.txt
```

### 2. Set up database

```bash
mysql -u root -p < schema.sql
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your DB credentials
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create new task |
| GET | `/tasks/{id}` | Get task by ID |
| PATCH | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Author

**Yevhen Knysh** — [LinkedIn](https://linkedin.com/in/yevhen-knysh-96310b377) · [GitHub](https://github.com/YeKnysh)
