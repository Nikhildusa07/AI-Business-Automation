AI-Powered Business Operations Automation System

An AI-powered business operations platform that converts incoming business requests into structured, actionable workflows using FastAPI, Google Gemini AI, automated decision-making, human-in-the-loop review, database persistence, notifications, and an administrative dashboard.

Overview

Businesses receive operational requests that require classification, prioritization, decision-making, approval, and follow-up. This project demonstrates how AI can be integrated into a backend workflow to automate suitable business operations while maintaining human oversight for cases that require approval.

Core Workflow

Business Request
       ↓
Validation
       ↓
Database Persistence
       ↓
AI Analysis
       ↓
Decision Engine
       ↓
 ┌───────────────┐
 │               │
 ▼               ▼
Automation   Human Review
 │               │
 ▼               ▼
Execution    Approve / Reject
       \         /
        \       /
         ▼     ▼
      Notification
           ↓
      Activity Tracking
           ↓
    Admin Dashboard

Project Objectives

The system is designed to:

Capture business requests through APIs and web forms

Validate and store incoming requests

Analyze requests using Google Gemini AI

Generate AI-assisted workflow decisions

Automatically execute suitable workflows

Route sensitive or uncertain requests for human review

Send workflow notifications

Maintain database records and activity history

Provide an administrative dashboard

Key Features

Business Request Intake

REST API request handling

Web-based request submission

Pydantic input validation

Structured request processing

Database persistence

Request status tracking

Gemini AI Integration

Google Gemini is integrated through the google-genai SDK.

The AI service is responsible for:

Understanding business requests

Extracting relevant information

Analyzing request content

Supporting operational decisions

Producing structured AI-related output

AI logic is isolated inside a dedicated service layer instead of being directly coupled to API routes.

Automated Decision Making

A dedicated decision service evaluates request information and AI analysis to determine the appropriate workflow.

Request
   ↓
AI Analysis
   ↓
Decision Engine
   ↓
Low Risk ──────→ Automatic Action
   │
   ├── Medium ──→ Review / Conditional Action
   │
   └── High ────→ Human Review

Human-in-the-Loop Review

The system does not blindly execute every AI recommendation. Requests requiring additional validation can be reviewed by an administrator.

AI Recommendation
        ↓
Needs Review?
     /       \
   No         Yes
   ↓           ↓
Automation   Human Review
                ↓
          Approve / Reject

Administrative Dashboard

The dashboard provides visibility into:

Business requests

Request status

Pending reviews

Approval/rejection actions

Workflow activity

Automation results

Notification System

A dedicated notification service handles workflow emails. Notifications can be triggered for important workflow events such as request submission, review decisions, approval, rejection, and workflow completion.

Authentication & Sessions

Administrative access is protected using authentication and session management. The application uses Starlette SessionMiddleware and environment-based configuration for sensitive values such as SECRET_KEY, admin credentials, API keys, and notification credentials.

Database Persistence

SQLAlchemy 2.x is used for database interaction and ORM-based persistence. Database records support tracking of business requests, workflow status, decisions, reviews, automation activity, and notifications.

System Architecture

                    User / Admin
                         │
                         ▼
              Web Forms / REST API
                         │
                         ▼
                    FastAPI
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      AI Service    Decision Service   Automation
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                    SQLAlchemy
                         │
                         ▼
                     Database
                         │
                         ▼
                Notification Service
                         │
                         ▼
                 Admin Dashboard

End-to-End Workflow

1. User submits a business request
                ↓
2. FastAPI receives the request
                ↓
3. Pydantic validates the input
                ↓
4. Request is stored in the database
                ↓
5. Gemini AI analyzes the request
                ↓
6. Decision service evaluates the request
                ↓
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
 Automatic Action    Human Review
       │                 │
       │          ┌──────┴──────┐
       │          │             │
       │       Approved       Rejected
       │          │             │
       └──────────┴─────────────┘
                    ↓
          Workflow status updated
                    ↓
             Notification sent
                    ↓
             Activity recorded
                    ↓
             Admin Dashboard

Project Structure

AI-Business-Automation/
│
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── requests.py
│   │   ├── reviews.py
│   │   └── web_form.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py
│   │   ├── ai_service.py
│   │   ├── automation_service.py
│   │   ├── decision_service.py
│   │   └── notification_service.py
│   │
│   ├── templates/
│   │   └── ...
│   │
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── test_ai.py
├── test_automation.py
├── test_automation_db.py
├── test_decision.py
├── test_gemini.py
├── test_smtp.py
│
├── .gitignore
├── requirements.txt
└── README.md

Technology Stack

Technology

Purpose

Python 3.11+

Core programming language

FastAPI

Backend API and application framework

Uvicorn

ASGI server

Pydantic

Data validation

SQLAlchemy 2.x

ORM and database interaction

Jinja2

Server-side HTML templates

Google Gemini

AI-powered request analysis

Google GenAI SDK

Gemini API integration

Starlette Sessions

Session management

python-dotenv

Environment configuration

Brevo

Email notifications

Service Layer

AI Service — app/services/ai_service.py: Handles AI-related request analysis and Gemini integration.

Agent Service — app/services/agent_service.py: Contains agent-oriented application logic.

Decision Service — app/services/decision_service.py: Processes request information and determines the appropriate workflow.

Automation Service — app/services/automation_service.py: Handles automated workflow execution.

Notification Service — app/services/notification_service.py: Handles business workflow notifications and email delivery.

The service layer keeps business logic independent from FastAPI route handlers.

Application Routes

Route Module

Responsibility

auth.py

Authentication

requests.py

Business request operations

web_form.py

Web-based request submission

reviews.py

Human review workflow

dashboard.py

Administrative dashboard

Environment Configuration

Create a .env file in the project root.

SECRET_KEY=your-secret-key

GEMINI_API_KEY=your-gemini-api-key

BREVO_API_KEY=your-brevo-api-key
BREVO_SENDER_EMAIL=your-verified-sender-email

ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-admin-password

Never commit .env files, API keys, passwords, or other secrets to GitHub.

For production deployment, configure environment variables directly in the hosting platform.

Local Setup

1. Clone the Repository

git clone https://github.com/Nikhildusa07/AI-Business-Automation.git
cd AI-Business-Automation

2. Create Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create .env and add the required configuration values.

5. Start the Application

uvicorn app.main:app --reload

Application:

http://127.0.0.1:8000

API Documentation

FastAPI provides automatic interactive documentation.

Swagger UI

http://127.0.0.1:8000/docs

ReDoc

http://127.0.0.1:8000/redoc

Testing

The project contains component-level tests covering key application functionality:

test_ai.py
test_automation.py
test_automation_db.py
test_decision.py
test_gemini.py
test_smtp.py

Run individual tests:

python test_ai.py
python test_automation.py
python test_automation_db.py
python test_decision.py
python test_gemini.py
python test_smtp.py

Test areas include:

AI processing

Gemini integration

Decision logic

Automation logic

Database-backed automation

Email/notification functionality

Deployment

The application is deployed as a FastAPI web service on Render.

Production environment variables must be configured in the hosting platform.

Internet
   ↓
Render
   ↓
FastAPI Application
   ├── Gemini AI
   ├── Database
   └── Brevo Notifications

Production application:

https://ai-business-automation-qfx0.onrender.com

Security Considerations

For production usage:

Never commit .env files

Never expose API keys in frontend code

Use HTTPS

Use secure session configuration

Use strong admin credentials

Validate external inputs

Protect public API endpoints

Use secure secret management

Monitor application logs

Review sensitive AI-generated actions before execution

Example Business Scenario

Traditional Process

Request
   ↓
Employee reads request
   ↓
Employee decides action
   ↓
Employee performs action
   ↓
Employee sends notification
   ↓
Employee updates records

Automated Process

Request
   ↓
FastAPI
   ↓
Gemini AI
   ↓
Decision Engine
   ↓
Automation / Human Review
   ↓
Notification
   ↓
Database
   ↓
Admin Dashboard

The system demonstrates an AI-assisted operational workflow, rather than simply providing a chatbot interface.

Benefits

Faster Processing: Automates repetitive business workflows and reduces unnecessary manual intervention.

AI-Assisted Decisions: Uses Gemini AI to analyze incoming business requests and support operational decisions.

Human Oversight: Provides human review for requests that should not be automatically processed.

Operational Visibility: Database persistence and the administrative dashboard provide visibility into workflow status and activity.

Maintainable Architecture: Routes, services, database logic, schemas, and templates are separated into dedicated modules.

Secure Configuration: Sensitive configuration is handled through environment variables rather than hard-coded credentials.

Future Enhancements

Potential improvements include:

Role-based access control

OAuth / SSO authentication

Advanced AI agents

Tool calling and function execution

Configurable workflow definitions

Multi-step approval workflows

SLA monitoring

Automated escalation

PostgreSQL

Redis and background task processing

Docker deployment

CI/CD pipelines

Advanced analytics

Slack / Microsoft Teams integration

CRM and ERP integrations

External REST API integrations

Project Status

Status: Completed Core Internship Project

Implemented capabilities include:

FastAPI backend

REST API request processing

Web-based request submission

Pydantic validation

SQLAlchemy database persistence

Gemini AI integration

AI service layer

Decision service

Automation service

Human-in-the-loop review

Authentication and sessions

Administrative dashboard

Email notification system

Component-level testing

Environment-based configuration

Production deployment

What This Project Demonstrates

This project demonstrates practical experience in:

Python backend development

FastAPI

REST API development

Pydantic validation

SQLAlchemy ORM

Database-driven workflows

Generative AI integration

Google Gemini API

AI-assisted decision making

Business process automation

Human-in-the-loop systems

Authentication and sessions

Server-side templating

Email notification systems

Modular software architecture

Automated testing

Environment-based configuration

Cloud deployment

Author

Nikhil

AI & ML Engineer | Python Backend Developer | AI Automation Developer

Focused on building practical systems combining:

Python
+
Backend Engineering
+
Artificial Intelligence
+
Automation
+
Full-Stack Development

Repository

GitHub:

https://github.com/Nikhildusa07/AI-Business-Automation

License

This project is intended for educational, development, and portfolio purposes.

Acknowledgements

This project was developed as a practical implementation of AI-powered business operations automation, combining modern Python backend development, generative AI, workflow automation, database persistence, notifications, and human oversight.

Final Takeaway

The AI-Powered Business Operations Automation System demonstrates how generative AI can be integrated into a real backend application to transform business requests into structured, traceable workflows.

Business Request
       ↓
     FastAPI
       ↓
   Gemini AI
       ↓
 Decision Engine
       ↓
 ┌─────┴─────┐
 ↓           ↓
Automation  Human Review
 ↓           ↓
 └─────┬─────┘
       ↓
 Notification
       ↓
   Database
       ↓
Admin Dashboard

Turn repetitive business operations into intelligent, traceable, and human-supervised automated workflows.
