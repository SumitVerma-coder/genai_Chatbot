# GitLab Handbook Chatbot

A Generative AI chatbot that helps users ask questions about GitLab's public Handbook and Direction pages. The chatbot retrieves relevant GitLab documentation chunks from MongoDB, sends them to a Gemini-powered RAG pipeline, and returns grounded answers with source references.

---

## 🚀 Features

### Core Features

- **GitLab Handbook Q&A**  
  Ask questions about GitLab's mission, values, remote work culture, asynchronous communication, DRI ownership, handbook-first approach, product direction, engineering, security, and more.

- **RAG-based Answer Generation**  
  The backend retrieves the most relevant chunks from MongoDB and generates answers using Gemini based only on the retrieved context.

- **Source-backed Responses**  
  Each answer can include source links so users can verify where the information came from.

- **Guardrailing**  
  If the user asks something unrelated to GitLab, the chatbot responds with:

  ```txt
  I'm only able to answer questions about GitLab's Handbook.
  ```

- **Suggested Questions**  
  Starter prompts are shown on load to help users begin quickly.

- **View Source Toggle**  
  Users can expand or collapse sources for each assistant response.

- **Authentication**  
  Users can sign up, log in, and log out.

- **Saved Chat History**  
  Authenticated users can save and reload previous conversations.

- **Persistent Current Chat**  
  The current chat is preserved across page refreshes.

- **Improved React UI**  
  Modern frontend built with React, Vite, and Tailwind CSS.

---

## 🧠 How It Works

```txt
User asks a question
        ↓
Frontend sends question to FastAPI backend
        ↓
Backend checks guardrails
        ↓
Relevant GitLab Handbook chunks are retrieved from MongoDB
        ↓
Gemini generates an answer using retrieved chunks only
        ↓
Frontend displays answer + sources
```

---

## 🛠️ Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS
- Axios / Fetch API
- LocalStorage for feedback and chat persistence

### Backend

- FastAPI
- Python
- Uvicorn
- Pydantic
- PyMongo
- BeautifulSoup
- Requests
- python-dotenv

### AI / RAG

- Google Gemini API
- Gemini embeddings
- MongoDB Atlas for chunk storage

### Database

- MongoDB Atlas

Collections used:

```txt
gitlab_chatbot
├── handbook_chunks
├── users
└── chats
```

---

## 📁 Project Structure

```txt
gitlab-handbook-chatbot/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── chat.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── rag_pipeline.py
│   │   │   ├── embeddings.py
│   │   │   ├── mongodb.py
│   │   │   └── guardrails.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py
│   │
│   ├── scripts/
│   │   └── ingest.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── InputBar.jsx
│   │   │   ├── SuggestedQuestions.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── FeedbackButtons.jsx
│   │   │   ├── SourceCard.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Signup.jsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useChat.js
│   │   │   └── useAuth.js
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── .env
│
└── README.md
```

---

## ⚙️ Backend Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/gitlab-handbook-chatbot.git
cd gitlab-handbook-chatbot
```

### 2. Go to Backend Folder

```bash
cd backend
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

#### Windows PowerShell

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

If `pip` is missing, run:

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### 5. Create `.env` File

Inside the `backend/` folder, create a `.env` file:

```env
MONGODB_URI=your_mongodb_atlas_connection_string
DATABASE_NAME=gitlab_chatbot
COLLECTION_NAME=handbook_chunks
GOOGLE_API_KEY=your_google_gemini_api_key
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## 🗄️ MongoDB Setup

Create a MongoDB Atlas database named:

```txt
gitlab_chatbot
```

Create these collections:

```txt
handbook_chunks
users
chats
```

### Collection Purpose

| Collection | Purpose |
|---|---|
| `handbook_chunks` | Stores scraped GitLab Handbook text chunks, embeddings, URLs, and metadata |
| `users` | Stores user account information |
| `chats` | Stores user chat sessions and messages |

MongoDB collections are created automatically when data is inserted, but you can also create them manually from MongoDB Atlas.

---

## 📥 Data Ingestion

The ingestion script scrapes selected GitLab Handbook URLs, chunks the text, creates embeddings, and stores the data in MongoDB.

Run:

```bash
python scripts/ingest.py
```

Recommended important GitLab Handbook URLs:

```txt
https://handbook.gitlab.com/handbook/company/mission/
https://handbook.gitlab.com/handbook/values/
https://handbook.gitlab.com/handbook/company/culture/all-remote/
https://handbook.gitlab.com/handbook/company/culture/all-remote/asynchronous/
https://handbook.gitlab.com/handbook/company/culture/all-remote/handbook-first/
https://handbook.gitlab.com/handbook/people-group/directly-responsible-individuals/
https://handbook.gitlab.com/handbook/product/
https://handbook.gitlab.com/handbook/engineering/
https://handbook.gitlab.com/handbook/security/
```

For broader coverage, you can parse GitLab's sitemap and filter URLs under useful paths such as:

```txt
/handbook/company/
/handbook/values/
/handbook/people-group/
/handbook/product/
/handbook/engineering/
/handbook/security/
```

---

## ▶️ Run Backend Locally

From the `backend/` folder:

```bash
python -m uvicorn app.main:app --reload
```

Backend will run at:

```txt
http://127.0.0.1:8000
```

Health check endpoint:

```txt
http://127.0.0.1:8000/health
```

---

## 🎨 Frontend Setup

### 1. Go to Frontend Folder

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Create `.env` File

Inside the `frontend/` folder, create:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### 4. Run Frontend

```bash
npm run dev
```

Frontend will run at:

```txt
http://localhost:5173
```

---

## 💬 Suggested Questions

The chatbot shows starter questions like:

```txt
What is GitLab's mission?
How does GitLab work remotely?
What are GitLab's values?
What is asynchronous communication at GitLab?
What is a DRI at GitLab?
What is GitLab's handbook-first approach?
```

These questions are based on high-value GitLab Handbook sections and help demonstrate the chatbot's core functionality.

---

## 🔐 Authentication Flow

The app supports:

- User signup
- User login
- JWT-based authentication
- Saved chat history per user
- Sidebar profile information
- Logout

Basic flow:

```txt
User signs up / logs in
        ↓
Backend returns JWT token
        ↓
Frontend stores token
        ↓
Token is sent with chat/history requests
        ↓
User chats are saved and loaded from MongoDB
```

---

## 🧪 API Endpoints

Example backend endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check backend status |
| `POST` | `/chat` | Ask a chatbot question |
| `POST` | `/auth/signup` | Create new user account |
| `POST` | `/auth/login` | Log in user |
| `GET` | `/chats` | Get user's chat history |
| `GET` | `/chats/{chat_id}` | Load a specific chat |
| `DELETE` | `/chats/{chat_id}` | Delete a chat |

---

## 🧾 Example Chat Request

```json
{
  "question": "What is GitLab's mission?"
}
```

Example response:

```json
{
  "answer": "GitLab's mission is to make it so everyone can contribute...",
  "sources": [
    {
      "title": "GitLab Mission",
      "url": "https://handbook.gitlab.com/handbook/company/mission/"
    }
  ]
}
```

---

## 🛡️ Guardrailing

The chatbot is designed to answer only GitLab Handbook-related questions.

Example:

```txt
User: What is the capital of France?
Bot: I'm only able to answer questions about GitLab's Handbook.
```

This keeps the chatbot focused, transparent, and aligned with the project objective.


## 🌐 Deployment

Recommended deployment setup:

### Frontend

Deploy React frontend on:

- Vercel
- Netlify

### Backend

Deploy FastAPI backend on:

- Render
- Railway
- Fly.io

### Database

Use:

- MongoDB Atlas

### Environment Variables for Deployment

Backend deployment variables:

```env
MONGODB_URI=your_mongodb_atlas_connection_string
DATABASE_NAME=gitlab_chatbot
COLLECTION_NAME=handbook_chunks
GOOGLE_API_KEY=your_google_gemini_api_key
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

Frontend deployment variable:

```env
VITE_API_BASE_URL=https://your-backend-url.com
```

After deploying the backend, update the frontend API URL to point to the deployed backend instead of localhost.

---

## ⚠️ Common Issues

### 1. Gemini API Quota Error

If you see an error like:

```txt
429 You exceeded your current quota
```

It means the Gemini API free-tier request limit has been reached. Wait for quota reset, reduce repeated calls, or switch to a different model/API key if allowed.

### 2. PowerShell npm.ps1 Error

If PowerShell blocks npm:

```txt
running scripts is disabled on this system
```

Run PowerShell as administrator and use:

```bash
Set-ExecutionPolicy RemoteSigned
```

Or use Command Prompt/Git Bash instead.

### 3. npm Version Error

If installing latest npm fails because of Node version mismatch, either upgrade Node.js or continue using the compatible npm version already installed.

### 4. VS Code `.env` Warning

If VS Code shows:

```txt
An environment file is configured but terminal environment injection is disabled.
```

Enable this setting in VS Code:

```json
"python.terminal.useEnvFile": true
```

### 5. Backend Changes Not Reflecting

If running with:

```bash
python -m uvicorn app.main:app --reload
```

most backend changes reload automatically. However, restart the server manually after changing `.env`, installing packages, or changing major app startup logic.

---

## 📌 Future Improvements

- Add semantic vector search using MongoDB Atlas Vector Search
- Add admin dashboard for feedback analytics
- Add streaming responses
- Add better source ranking
- Add document refresh scheduler
- Add role-based user access
- Add public deployment URL in README after deployment

---

## 📄 Project Objective Summary

This chatbot improves access to GitLab's public knowledge base by allowing users to ask natural language questions and receive grounded, source-backed answers. It combines data scraping, RAG, generative AI, FastAPI, MongoDB, and React into a practical full-stack GenAI application.

---

## 🙋 Author

**Sumit Verma**  

---

## 📜 License

This project is licensed under the MIT License.
