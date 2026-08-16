AI-Powered Business Operations Automation System

<p align="center">
  <strong>AI Automation Intern — Advanced Project</strong><br>
  XQORA Technologies
</p>

<p align="center">
  <a href="https://ai-business-automation-qfx0.onrender.com">Live Demo</a> •
  <a href="https://github.com/Nikhildusa07/AI-Business-Automation">GitHub Repository</a>
</p>

Overview

The AI-Powered Business Operations Automation System is a production-deployed backend automation platform that converts incoming business requests into structured, traceable workflows.

The system combines FastAPI, Google Gemini, SQLAlchemy, an AI-agent workflow, conditional decision logic, automated notifications, human review, activity logging, authentication, and an administrative dashboard.

Instead of simply generating an AI response, the system uses AI as one stage of a complete business workflow:

Request
   │
   ├── Web Form
   └── REST API
          │
          ▼
   Input Validation
          │
          ▼
   Database Persistence
          │
          ▼
   Gemini AI Analysis
          │
          ▼
   AI Agent Workflow
          │
          ├── Tool Selection
          ├── Data Retrieval
          ├── Reasoning
          └── Verification
          │
          ▼
   Decision Engine
          │
      ┌───┼───────────┐
      ▼   ▼           ▼
     LOW MEDIUM      HIGH
      │   │           │
      ▼   ▼           ▼
   Auto  Follow-up  Human Review
   Action / Conditional
          │
          ▼
   Automated Actions
          │
          ▼
   Brevo Notification
          │
          ▼
   Activity / Audit Log
          │
          ▼
   Admin Dashboard

The architecture directly addresses the XQORA assignment requirement for a genuinely functional automation workflow, rather than a chatbot or basic API demonstration. fileciteturn10file1L1-L8

Live Application

Production URL:
https://ai-business-automation-qfx0.onrender.com

Source Code:
https://github.com/Nikhildusa07/AI-Business-Automation

The deployed application has been tested through the complete request workflow, including production email delivery through Brevo.

Problem Statement

Business teams frequently spend time manually:

Reading incoming requests

Identifying intent

Determining priority

Deciding the appropriate next action

Updating records

Sending customer notifications

Escalating critical cases

Tracking workflow activity

This creates repetitive work and makes it difficult to maintain consistent, auditable processes.

Goal

Build an automation system that can:

Receive a business request.

Understand and classify it using AI.

Determine priority and confidence.

Select the appropriate workflow.

Execute automated actions.

Escalate sensitive or uncertain cases.

Notify the relevant customer.

Store the complete workflow history.

Key Capabilities

1. Multiple Request Triggers

The system supports two input mechanisms:

Web form submission

REST API request

This satisfies the requirement for multiple triggers. fileciteturn10file1L8-L12

2. AI-Powered Request Analysis

Google Gemini is used to perform meaningful processing rather than simply generating text.

The AI workflow analyzes:

Request intent

Priority

Confidence score

Request summary

Relevant business context

Example classification:

Priority

Typical Request

Workflow

LOW

Business hours / general enquiry

Automated response

MEDIUM

Profile, subscription, billing or normal support

Follow-up / conditional processing

HIGH

Fraud, unauthorized transaction, security or account compromise

Human review / escalation

The assignment specifically requires AI to perform meaningful work such as classification, intent detection, priority scoring, information extraction, or decision support. fileciteturn10file1L8-L12

3. AI-Agent / Multi-Step Workflow

The application includes an agent-oriented workflow:

User Request
     │
     ▼
AI Analysis
     │
     ▼
Tool Selection
     │
     ▼
Business Data Retrieval
     │
     ▼
Reasoning
     │
     ▼
Decision
     │
     ▼
Action / Human Review
     │
     ▼
Verification

The agent can select from business-support tools such as:

business_hours

payment_support

profile_support

general_support

The tool-selection layer attempts AI-based selection and includes deterministic fallback logic when the AI service is unavailable.

This corresponds to the assignment's advanced requirement of:

User Request → AI Agent → Tool/API Selection → Data Retrieval → Reasoning → Decision → Action → Verification. fileciteturn10file11L1-L8

4. Conditional Decision Engine

The decision layer converts AI analysis into an operational workflow.

                    AI Analysis
                         │
                         ▼
                 Decision Engine
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
         LOW           MEDIUM          HIGH
          │              │              │
          ▼              ▼              ▼
   Automated Action   Follow-up     Human Review

Low-confidence or failed workflow conditions can also be routed toward safe human-review handling.

The assignment requires multiple decision branches, including priority-based processing and human review for uncertain cases. fileciteturn10file11L1-L8

5. Human-in-the-Loop Review

Automation is not allowed to blindly execute every decision.

The administrative workflow provides a human-review stage for requests requiring additional validation.

Administrators can:

View requests

Review request details

Inspect AI analysis

Approve requests

Reject requests

Continue the workflow after review

This provides operational control over sensitive business cases.

6. Automated Notifications

The production notification system uses Brevo.

The notification service is isolated from the application routes so that email delivery remains a separate workflow component.

Customer notifications are sent to the recipient email supplied with the request.

Production testing confirmed successful email delivery.

7. Database Persistence

SQLAlchemy is used for ORM-based persistence.

The workflow stores information required for traceability, including:

Request ID

Customer information

Customer email

Original request

AI intent

Priority

Confidence score

AI summary

Action taken

Workflow status

Review information

Activity records

Timestamps

Failure information

The assignment requires persistent storage of request and workflow information. fileciteturn10file11L1-L8

8. Activity and Audit Logging

Major workflow stages are recorded as activity events.

Examples include:

AI_ANALYSIS
AGENT_TOOL_SELECTED
AGENT_DATA_RETRIEVED
AGENT_REASONING
DECISION_MADE
AUTOMATION
NOTIFICATION
HUMAN_REVIEW

This allows an administrator to understand:

What happened

When it happened

Which stage executed

Whether the stage succeeded or failed

What action was performed

The assignment explicitly requires major workflow executions to be logged. fileciteturn10file11L1-L8

9. Error Handling and Fallbacks

External services can fail, so the application includes fallback mechanisms.

Gemini Failure

Gemini Request
      │
 ┌────┴────┐
 │         │
Success   Failure
 │         │
 ▼         ▼
AI Result  Local Deterministic Fallback
             │
             ▼
       Continue Workflow

The application handles situations such as:

Gemini quota exhaustion

AI client/request failure

Tool-selection failure

Notification failure

Workflow exceptions

Failures are captured and logged rather than silently terminating the complete workflow.

The assignment requires error detection, fallback/retry behavior, failure logging, notification, and human-review handling where appropriate. fileciteturn10file11L1-L8

Technology Stack

Layer

Technology

Language

Python

Backend

FastAPI

Server

Uvicorn

Validation

Pydantic

ORM

SQLAlchemy 2.x

Templates

Jinja2

AI

Google Gemini

AI SDK

Google GenAI SDK

Authentication

Session-based authentication

Email

Brevo API

Configuration

python-dotenv

Deployment

Render

Testing

Python component tests

Architecture

                         ┌─────────────────────┐
                         │       Client        │
                         │ Web Form / REST API │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │  Request Handling   │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │      Pydantic       │
                         │    Validation       │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │      Database       │
                         │    SQLAlchemy       │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │      AI Service     │
                         │   Google Gemini     │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │    Agent Service    │
                         │ Tool → Data →       │
                         │ Reasoning → Verify  │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │   Decision Service  │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
             Automation         Follow-up       Human Review
                  │                 │                 │
                  └─────────────────┼─────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Automation Service  │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Notification Service│
                         │       Brevo         │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Activity / Audit Log│
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │  Admin Dashboard    │
                         └─────────────────────┘

Project Structure

AI-Business-Automation/
│
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── requests.py
│   │   ├── reviews.py
│   │   └── web_form.py
│   │
│   ├── services/
│   │   ├── agent_service.py
│   │   ├── ai_service.py
│   │   ├── automation_service.py
│   │   ├── decision_service.py
│   │   └── notification_service.py
│   │
│   ├── templates/
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
├── requirements.txt
├── .gitignore
└── README.md

Service Layer

AI Service

app/services/ai_service.py

Responsible for Gemini-based request analysis and structured AI results.

Agent Service

app/services/agent_service.py

Responsible for tool selection, business-data retrieval, reasoning, and verification.

Decision Service

app/services/decision_service.py

Responsible for converting request priority and confidence into workflow decisions.

Automation Service

app/services/automation_service.py

Responsible for executing workflow actions and updating workflow state.

Notification Service

app/services/notification_service.py

Responsible for sending business workflow emails through Brevo.

This separation keeps business logic independent from FastAPI route handlers.

API and Application Interfaces

Web Application

The primary user-facing workflow is available through the deployed web application:

https://ai-business-automation-qfx0.onrender.com

REST API

FastAPI provides interactive API documentation.

Swagger UI

/docs

Local:

http://127.0.0.1:8000/docs

ReDoc

http://127.0.0.1:8000/redoc

Configuration

Create a .env file in the project root for local development.

SECRET_KEY=your-secret-key

GEMINI_API_KEY=your-gemini-api-key

BREVO_API_KEY=your-brevo-api-key
BREVO_SENDER_EMAIL=your-verified-sender-email

ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-admin-password

Never commit .env, API keys, passwords, or other secrets to GitHub.

For production, configure secrets through the Render environment-variable settings.

Local Development

1. Clone the repository

git clone https://github.com/Nikhildusa07/AI-Business-Automation.git
cd AI-Business-Automation

2. Create a virtual environment

Windows

python -m venv venv
venv\Scriptsctivate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create .env using the configuration shown above.

5. Run the application

python -m uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000

Testing

The repository contains component-level tests covering core application functionality.

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

Testing covers:

AI processing

Gemini integration

Decision logic

Automation logic

Database-backed automation

Email notification functionality

Example Test Scenarios

LOW Priority

Request

What are your business working hours?

Expected

Priority: LOW
Workflow: Automated processing

MEDIUM Priority

Request

I want to update my profile and change my subscription plan.

Expected

Priority: MEDIUM
Workflow: Follow-up / conditional processing

HIGH Priority

Request

I see an unauthorized transaction and believe my account
may have been compromised. Please investigate immediately.

Expected

Priority: HIGH
Workflow: Human review / escalation

Deployment

The application is deployed as a FastAPI web service on Render.

Internet
   │
   ▼
Render
   │
   ▼
FastAPI Application
   ├── Google Gemini
   ├── SQLAlchemy / Database
   └── Brevo Email API

Production URL

https://ai-business-automation-qfx0.onrender.com

Production testing confirmed that the workflow can complete successfully and send customer email notifications through Brevo.

Security

The application follows basic security practices:

Secrets are supplied through environment variables.

.env should not be committed.

API keys are not embedded in frontend code.

Administrative routes require authentication.

Request input is validated.

Production communication uses HTTPS.

Sensitive or uncertain cases can be routed to human review.

Known Limitations

Gemini availability and quota can affect AI-powered analysis.

A deterministic fallback is used when Gemini is unavailable.

The current implementation is designed as an internship-level real-world automation platform and can be extended for larger production workloads.

Future Improvements

Potential future enhancements include:

Role-based access control

OAuth / SSO

More AI tools and external integrations

Configurable workflow definitions

Multi-step approval workflows

SLA monitoring and automated escalation

PostgreSQL for larger deployments

Redis/background workers

Docker-based deployment

CI/CD pipelines

Advanced analytics

Slack / Microsoft Teams integration

CRM and ERP integrations

Assignment Alignment

The project was built to address the mandatory requirements of the XQORA Technologies Advanced Project Assignment.

Assignment Requirement

Implementation

2+ triggers

Web form + REST API

Meaningful AI processing

Gemini analysis, intent, priority, confidence

4+ automated workflow actions

Validation, persistence, AI analysis, agent processing, decision, notification, logging

Conditional logic

LOW / MEDIUM / HIGH + review handling

Database storage

SQLAlchemy persistence

Error handling

Fallbacks, failure handling, logging

Dashboard / monitoring

Administrative dashboard

Activity logging

Workflow activity records

AI-agent workflow

Tool selection → data retrieval → reasoning → verification

Human-in-the-loop

Admin review and approval/rejection

Public deployment

Render

Email notification

Brevo

The assignment requires a working public application, functional AI, automation, database storage, error handling, dashboard/monitoring, and no major broken mandatory features. fileciteturn10file8L1-L8

Project Status

Completed

Web request trigger

REST API trigger

Input validation

Database persistence

Gemini AI integration

Priority classification

Confidence scoring

AI-agent workflow

Tool selection

Business data retrieval

Reasoning and verification

Conditional decision engine

Automated workflow actions

Human review

Email notifications

Activity/audit logging

Authentication

Administrative dashboard

Error handling and fallbacks

Component-level testing

Render deployment

Production email testing

Author

Nikhil

AI & ML Engineer • Python Backend Developer • AI Automation Developer

License

This project was developed for educational, internship, demonstration, and portfolio purposes.

Final Summary

The AI-Powered Business Operations Automation System demonstrates how generative AI can be integrated into a real backend workflow to automate business operations while maintaining traceability and human oversight.

             BUSINESS REQUEST
                    │
                    ▼
             FASTAPI / REST
                    │
                    ▼
              AI ANALYSIS
                    │
                    ▼
             AI AGENT WORKFLOW
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
       AUTOMATION         HUMAN REVIEW
          │                   │
          └─────────┬─────────┘
                    ▼
              NOTIFICATION
                    │
                    ▼
             ACTIVITY LOG
                    │
                    ▼
             ADMIN DASHBOARD

Intelligent automation with AI, decision logic, human oversight, and complete workflow traceability.
