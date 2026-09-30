# PocketSmart AI

PocketSmart AI is a GenAI-powered budget and recommendation assistant.

The application supports:

- Home Interior Planning
- Party Budget Planning
- Jewelry Recommendations
- Optional outfit image analysis
- User registration
- User login
- JWT authentication
- Recommendation history
- Gemini AI integration
- Mock AI mode
- Amazon links
- Flipkart links
- IKEA links
- Swiggy links
- Zomato links
- OYO links
- FastAPI backend
- Jinja2 frontend
- SQLite database
- REST APIs
- Automated tests

---

# Project Structure

```text
PocketSmartAI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── web.py
│   │   ├── auth.py
│   │   └── planners.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── catalog.py
│   │   └── recommendation_service.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── home.html
│   │   ├── party.html
│   │   └── jewelry.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── tests/
│   └── test_app.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md