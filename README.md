# 🤖 AI-Powered Business Operations Automation System

> An AI-powered business operations platform that transforms incoming business requests into structured, actionable workflows using **FastAPI, Gemini AI, automated decision-making, human-in-the-loop review, database persistence, notifications, activity logging, and an administrative dashboard.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini%20AI-Google-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.x-E92063?style=for-the-badge)](https://docs.pydantic.dev/)
[![Jinja2](https://img.shields.io/badge/Jinja2-Templates-B41717?style=for-the-badge)](https://jinja.palletsprojects.com/)

---

# 📌 Project Status

**Status: Completed — XQORA Technologies AI Automation Intern Project**

The core AI-powered business automation workflow has been implemented, tested, and deployed publicly.

### Current implementation includes:

- FastAPI backend
- REST API trigger
- Web-based request submission
- Pydantic validation
- Gemini AI integration
- AI request analysis
- LOW / MEDIUM / HIGH priority classification
- Confidence-based decision processing
- AI-agent workflow
- Automated business actions
- Conditional decision logic
- Human-in-the-loop review
- Database persistence
- Activity and audit logging
- Customer email notifications
- Brevo email integration
- Authentication and session management
- Administrative dashboard
- Action verification
- Error handling and fallback processing
- Automated component tests
- Public Render deployment

---

# 🌐 Live Demo

**Live Application:**

https://ai-business-automation-qfx0.onrender.com

**GitHub Repository:**

https://github.com/Nikhildusa07/AI-Business-Automation

---

# 📌 Overview

Modern businesses receive a continuous stream of operational requests such as:

- Customer support requests
- Internal operational tasks
- Approval requests
- Business process requests
- Administrative actions
- Follow-up activities
- Requests requiring prioritization or review

Handling these requests manually can result in:

- Delayed responses
- Repetitive work
- Inconsistent decision-making
- Poor visibility into request status
- Lack of centralized activity tracking
- Increased operational overhead

The **AI-Powered Business Operations Automation System** introduces an intelligent automation layer between incoming business requests and operational execution.

The system accepts a business request, validates and stores the request, analyzes it using AI, determines an appropriate workflow, identifies cases requiring human review, executes automated actions, sends notifications, and records the resulting activity for administrative visibility.

---

# 🎯 Project Objective

The primary objective of this project is to demonstrate how **Artificial Intelligence can be integrated with traditional backend systems to automate business operations while maintaining human oversight where necessary.**

The system is designed around five core principles:

1. **Capture** business requests through APIs or web forms.
2. **Understand** requests using AI.
3. **Decide** the appropriate workflow or action.
4. **Execute** suitable automated actions.
5. **Review and Track** sensitive decisions through human approval and persistent activity records.

This creates a practical **AI-assisted business workflow rather than a standalone chatbot.**

---

# ✨ Key Features

## 📨 1. Business Request Intake

The platform provides structured request intake through REST APIs and a web interface.

### Capabilities

- REST API request handling
- Web-based request submission
- Input validation
- Structured request schemas
- Database persistence
- Request status tracking

---

# 🧠 2. Gemini-Powered AI Analysis

The application integrates Google's Gemini AI through the Google GenAI SDK.

The AI layer analyzes incoming business information and generates structured insights used by the automation and decision layers.

### AI responsibilities

- Understand request content
- Analyze business requests
- Extract relevant information
- Assist business decision-making
- Determine workflow requirements
- Support priority classification
- Provide confidence information where available

The AI functionality is separated into its own service layer so that AI-specific logic remains independent from API routes and database logic.

---

# 🎯 3. Priority Classification

Incoming requests are classified into three business priority levels:

```text
LOW
MEDIUM
HIGH
