# 🤖 AI-Powered Business Operations Automation System

A Full Stack **AI-powered Business Automation System** built using **Python, FastAPI, Gemini AI, SQLAlchemy, and Brevo**. The application receives business requests, analyzes them using AI, determines their priority and required action, stores the request in a database, and sends email notifications automatically.

---

## 📌 Overview

The AI-Powered Business Operations Automation System is designed to automate common business workflows such as customer request processing, priority classification, human review, and email notifications.

The system uses an AI-powered workflow to analyze incoming requests and determine whether they require **Low, Medium, or High priority** handling.

It also provides a dashboard for reviewing and approving requests before completing the required business action.

---

## ✨ Features

- 🤖 AI-powered request analysis
- 📩 Customer email notifications
- 🔐 Admin authentication
- 📊 Business operations dashboard
- 🟢 Low priority request handling
- 🟡 Medium priority request handling
- 🔴 High priority request handling
- 👨‍💼 Human review and approval workflow
- 💾 Database storage
- 📋 Request tracking and status management
- ⚡ REST API integration
- 🛡️ Error handling and fallback processing
- 📧 Automated email notifications using Brevo
- 🚀 Deployment-ready FastAPI application
- ☁️ Deployed on Render

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

## AI

- Google Gemini API
- AI-powered request analysis
- Priority classification
- Deterministic fallback processing

## Email

- Brevo API
- Automated email notifications

## Frontend

- HTML5
- CSS3
- JavaScript

## Database

- SQLAlchemy
- Relational Database

## Deployment & Tools

- Git
- GitHub
- VS Code
- Render
- Postman

---

# 📂 Project Structure

```text
AI-Business-Automation
│
├── app
│   ├── main.py
│   ├── models
│   ├── schemas
│   ├── routes
│   ├── services
│   └── ...
│
├── templates
│   ├── login.html
│   ├── dashboard.html
│   └── ...
│
├── static
│   ├── css
│   └── js
│
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── ...
