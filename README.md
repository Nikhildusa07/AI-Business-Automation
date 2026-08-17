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

🚀 Installation
Clone Repository

git clone https://github.com/Nikhildusa07/AI-Business-Automation.git

cd AI-Business-Automation

Backend Setup
Create Virtual Environment
python -m venv venv
Activate Virtual Environment
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
⚙️ Environment Variables

## Admin dashboard

ADMIN_USERNAME=admin
ADMIN_PASSWORD=123456789

▶️ Run the Application

Start the FastAPI server:

python -m uvicorn app.main:app --reload

Application URL:

http://127.0.0.1:8000/

🔄 Automation Workflow
Customer Request
       ↓
Request Validation
       ↓
AI Analysis
       ↓
Priority Classification
       ↓
Database Storage
       ↓
Human Review
       ↓
Approval / Rejection
       ↓
Automated Action
       ↓
Email Notification
🤖 AI Processing

The system uses Gemini AI to analyze incoming business requests.

The AI determines the appropriate priority:

🟢 Low – General or non-urgent requests
🟡 Medium – Requests requiring attention
🔴 High – Urgent or critical requests

If the AI service is unavailable or the quota is exhausted, the application uses a deterministic local fallback mechanism to continue processing requests.

📩 Email Notifications

The system automatically sends email notifications to the customer after the required workflow action is completed.

Email delivery is handled using Brevo API.

The recipient email address is taken from the submitted business request.

🔐 Authentication

The application provides authentication for authorized users.

Features include:

Admin login
Session-based authentication
Protected dashboard
Request review and approval
Logout functionality

📊 Dashboard

The dashboard allows authorized users to:

View submitted requests
Check request priority
Review request details
Approve requests
Reject requests
Track request status
Trigger automated notifications

🧪 Testing

The application can be tested using different request priorities.

Low Priority
Customer needs general information about the available services.
Please provide details about pricing and available plans.
Medium Priority
Customer is experiencing an issue with their account
and needs assistance resolving the problem within the next few hours.
High Priority
URGENT: Customer is unable to access their account
and has an important business operation scheduled today.
Please resolve this issue immediately.

🌐 Deployment

The application is deployed using Render.

Live Application:

https://ai-business-automation-qfx0.onrender.com
🔮 Future Enhancements
📌 Additional business automation workflows
📌 Advanced AI decision-making
📌 Multiple user roles
📌 Email templates
📌 Real-time notifications
📌 Advanced analytics dashboard
📌 Docker support
📌 Cloud database integration
📌 More third-party integrations
📌 Workflow scheduling
💡 Why This Project?

This project demonstrates practical experience in building an AI-powered business automation platform using modern backend technologies.

It showcases:

AI integration
REST API development
Database management
Authentication
Business workflow automation
Email automation
Human-in-the-loop processing
Error handling
Cloud deployment

📄 License

This project is licensed under the MIT License.

👨‍💻 Author

Dusa Nikhil

📧 Email: dusanikhil3@gmail.com

💼 LinkedIn: https://www.linkedin.com/in/nikhil-dusa-71089b1a7

🐙 GitHub: https://github.com/Nikhildusa07

⭐ Support

If you found this project useful, please consider giving it a ⭐ Star on GitHub.



**This is the style you should use**: simple sections, emojis, installation steps, project structure, features, workflow, deployment, and author — similar to your Notes Management README, while still reflecting what you actually built.
