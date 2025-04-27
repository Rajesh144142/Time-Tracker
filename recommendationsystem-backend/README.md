# 🎟️ Ticket Assistant

A **Python-based** solution leveraging **Agentic AI** using **FastAPI**. This application aims to provide smart ticket handling capabilities through an API-first approach.

---

## 🚀 Features

- ⚡ FastAPI-powered backend
- 🧠 Agentic AI logic (via AutoGen)
- 📦 Modular architecture
- 🔐 Environment-based config
- 🛠️ Future support for MongoDB

---

## 📁 Project Structure

```
ticket_assistant/
├── app/                       # Main application package
│   ├── __init__.py            # Makes app a Python package
│   ├── main.py                # FastAPI app entry point
│   ├── config.py              # Environment/configuration variables
│   ├── routes/                # API route handlers
│   │   └── assistant.py       # Endpoints for AI assistant
│   ├── services/              # Core business logic
│   │   └── agent.py           # Agentic AI logic (AutoGen placeholder)
│   └── db/                    # Database utilities
│       └── mongo.py           # MongoDB connection (coming soon)
├── .env                       # Environment variables file
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
```

---

## 📋 Requirements

The application requires the following packages:
```
fastapi[standard]
uvicorn[standard]
pydantic
python-dotenv
```

---

## 🔧 Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/ticket-assistant.git
cd ticket-assistant
```

### Create a virtual environment

```bash
# For Unix/macOS
python -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up environment variables

Create a `.env` file in the root directory:

```
# .env example
API_KEY=your_api_key_here
DEBUG=True
MONGODB_URI=mongodb://localhost:27017/ticket_assistant
```

---

## 🚀 Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

