AI-Powered Business Operations Automation System

XQORA Technologies — AI Automation Intern Advanced Project

An AI-powered business operations automation platform that receives business requests, validates and stores them, analyzes them with Google Gemini, applies priority-based decision logic, executes workflow actions, sends customer notifications through Brevo, and routes sensitive or uncertain requests to human review.

Live Demo

Production: https://ai-business-automation-qfx0.onrender.com

GitHub: https://github.com/Nikhildusa07/AI-Business-Automation

Project Objective

The system demonstrates a real AI-powered business automation workflow rather than a simple chatbot:

Request / Trigger
      |
      v
Validation
      |
      v
Database Storage
      |
      v
Gemini AI Analysis
      |
      v
Priority + Confidence
      |
      v
Decision Engine
   +--+---------+---------+
   |            |         |
  LOW        MEDIUM      HIGH
   |            |         |
Auto Action  Follow-up  Human Review
   |            |         |
   +------------+---------+
                |
                v
        Automation Actions
                |
                v
       Brevo Email Notification
                |
                v
        Activity / Audit Log
                |
                v
        Administrative Dashboard

Key Features

Multiple Triggers

Web-based request submission

REST API request processing

AI Processing

Google Gemini analyzes requests and produces:

Intent

Priority: HIGH, MEDIUM, or LOW

Confidence score

Summary

Priority Logic

Priority

Example

Typical Action

HIGH

Fraud, unauthorized transaction, security issue, account compromise

Human review / escalation

MEDIUM

Subscription change, profile update, billing question, normal support

Follow-up / conditional processing

LOW

Business hours, general information, routine enquiries

Automated processing

AI-Agent / Multi-Step Workflow

Request
  -> Tool Selection
  -> Business Data Retrieval
  -> AI Reasoning
  -> Decision
  -> Action / Human Review
  -> Verification / Activity Tracking

Business tools include:

Business hours

Payment/refund support

Customer profile support

General business support

Human-in-the-Loop

Administrators can review pending requests and approve or reject them when additional validation is required.

Email Notifications

Production email delivery uses Brevo. Customer notifications are sent to the email supplied with the request.

Database

SQLAlchemy is used for persistence and workflow tracking, including request information, decisions, reviews, automation activity, notifications, status, and timestamps.

Dashboard

The admin dashboard provides visibility into:

Requests

Status

Pending reviews

High-priority cases

Approval/rejection actions

Recent workflow activity

Automation results

Error Handling

The system includes deterministic fallbacks:

Gemini unavailable/quota exhausted -> local analysis fallback

AI tool-selection failure -> deterministic tool-selection fallback

Email failures -> captured and reported by the notification service

Technology Stack

Technology

Purpose

Python 3.11+

Core language

FastAPI

Backend and REST API

Uvicorn

ASGI server

Pydantic

Validation and schemas

SQLAlchemy 2.x

ORM/database

Jinja2

Server-side templates

Google Gemini

AI analysis

Google GenAI SDK

Gemini integration

Starlette Sessions

Session management

python-dotenv

Environment configuration

Brevo

Email notifications

Render

Production deployment

System Architecture

User
 |
 +--> Web Form
 |
 +--> REST API
       |
       v
    FastAPI
       |
       +--> Pydantic Validation
       |
       +--> Database
       |
       +--> AI Service --> Gemini
       |
       +--> Agent Service
       |      |
       |      +--> Tool Selection
       |      +--> Data Retrieval
       |      +--> Reasoning
       |
       +--> Decision Service
       |
       +--> Automation Service
       |
       +--> Notification Service --> Brevo
       |
       +--> Human Review
       |
       +--> Admin Dashboard

End-to-End Workflow

User submits a request through the web form or REST API.

FastAPI receives and validates the request.

Request data is persisted.

Gemini analyzes the request.

Intent, priority, confidence, and summary are generated.

The agent workflow selects a suitable business tool.

Relevant business information is retrieved.

The workflow reasons about the request.

The decision service determines the next action.

Suitable requests are processed automatically.

High-priority or low-confidence cases can enter human review.

Brevo sends workflow notifications.

Activity and status are recorded.

Administrators monitor the workflow through the dashboard.

Project Structure

AI-Business-Automation/
|
+-- app/
|   +-- routes/
|   |   +-- auth.py
|   |   +-- dashboard.py
|   |   +-- requests.py
|   |   +-- reviews.py
|   |   +-- web_form.py
|   |
|   +-- services/
|   |   +-- agent_service.py
|   |   +-- ai_service.py
|   |   +-- automation_service.py
|   |   +-- decision_service.py
|   |   +-- notification_service.py
|   |
|   +-- templates/
|   +-- database.py
|   +-- models.py
|   +-- schemas.py
|   +-- main.py
|
+-- test_ai.py
+-- test_automation.py
+-- test_automation_db.py
+-- test_decision.py
+-- test_gemini.py
+-- test_smtp.py
+-- requirements.txt
+-- .gitignore
+-- README.md

Application Routes

Module

Responsibility

auth.py

Authentication and login/logout

requests.py

Business request operations

web_form.py

Web request submission

reviews.py

Human review workflow

dashboard.py

Administrative dashboard

Environment Configuration

Create .env locally:

SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
BREVO_API_KEY=your-brevo-api-key
BREVO_SENDER_EMAIL=your-verified-sender-email
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-admin-password

Never commit .env, API keys, passwords, or other secrets to GitHub.

For Render, configure the required values in the service Environment Variables.

Local Setup

git clone https://github.com/Nikhildusa07/AI-Business-Automation.git
cd AI-Business-Automation

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

Create .env, then run:

python -m uvicorn app.main:app --reload

Application:

http://127.0.0.1:8000

API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

Testing

Available component tests:

test_ai.py
test_automation.py
test_automation_db.py
test_decision.py
test_gemini.py
test_smtp.py

Example:

python test_ai.py
python test_automation.py
python test_automation_db.py
python test_decision.py
python test_gemini.py
python test_smtp.py

Test areas include AI processing, Gemini integration, decision logic, automation, database-backed automation, and email functionality.

Production Deployment

The application is deployed as a FastAPI service on Render.

Internet
   |
   v
Render
   |
   v
FastAPI
   +--> Gemini AI
   +--> Database
   +--> Brevo

Production URL: https://ai-business-automation-qfx0.onrender.com

Production testing confirmed successful customer email delivery through Brevo.

Example Test Requests

LOW

Customer email: customer@example.com

What are your business working hours?

Expected: LOW -> automated processing.

MEDIUM

Customer email: customer@example.com

I want to update my profile and change my subscription plan.

Expected: MEDIUM -> follow-up / conditional processing.

HIGH

Customer email: customer@example.com

I see an unauthorized transaction and believe my account may be compromised. Please investigate immediately.

Expected: HIGH -> human review / escalation.

Security

Keep secrets in environment variables.

Never commit .env.

Never expose API keys in frontend code.

Use HTTPS in production.

Use strong administrator credentials.

Validate incoming data.

Protect administrative routes with authentication.

Use human review for sensitive decisions.

Known Limitations

Gemini availability and quota can affect AI analysis.

Deterministic fallback logic is used when Gemini is unavailable.

The project is designed as an internship/portfolio automation platform rather than a large-scale enterprise system.

Future Enhancements

Role-based access control

OAuth / SSO

Advanced AI agents

More external API/tool integrations

Configurable workflows

Multi-step approvals

SLA monitoring

PostgreSQL

Redis/background workers

Docker and CI/CD

Advanced analytics

Slack / Microsoft Teams integration

CRM/ERP integrations

Project Status

Completed — Core Internship Project

Implemented:

FastAPI backend

Web form trigger

REST API trigger

Pydantic validation

SQLAlchemy persistence

Gemini AI integration

AI-agent/multi-step workflow

Tool selection and data retrieval

Decision service

Conditional logic

Automation service

Human-in-the-loop review

Authentication

Admin dashboard

Brevo email notifications

Error handling and fallback

Testing

Environment-based configuration

Render deployment

Author

Nikhil

AI & ML Engineer | Python Backend Developer | AI Automation Developer

License

Educational, development, and portfolio purposes.

Turn repetitive business operations into intelligent, traceable, and human-supervised automated workflows.
