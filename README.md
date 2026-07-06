# 🏛️ Government Scheme Assistant 
### AI-Powered Multi-Agent Platform for Government Welfare Scheme Discovery

An agentic AI app that helps citizens discover which government schemes
they qualify for, what documents they need, and how to apply — now with
accounts, an admin panel, bilingual support, and usage analytics.

## Features

- **6 AI Agents**: Profile, Eligibility, Document Verification, Application
  Guide, Deadline, and FAQ (LLM-powered)
- **Bilingual**: Full English / Tamil support, including PDF reports
- **User Accounts**: Citizens can sign up, log in, and save profiles to
  revisit results later (guests can still use the app without an account)
- **Admin Panel**: Add, edit, or delete schemes through a form — no code
  or JSON editing required
- **Analytics Dashboard**: See which schemes are matched most often, which
  documents citizens most commonly lack, and basic demographic breakdowns
- **PDF Export**: Downloadable report of eligible schemes, documents, and
  application steps (always generated in English for reliability)

## Architecture

| Component | File | Job |
|---|---|---|
| 👤 Citizen Profile Agent | `agents/profile_agent.py` | Structures form input |
| 📋 Eligibility Agent | `agents/eligibility_agent.py` | Matches profile against scheme rules |
| 📄 Document Verification Agent | `agents/document_agent.py` | Checks missing documents |
| 🗺️ Application Guide Agent | `agents/guide_agent.py` | Step-by-step apply instructions |
| 📅 Deadline Agent | `agents/deadline_agent.py` | Flags urgent deadlines |
| 💬 FAQ Agent | `agents/faq_agent.py` | Answers open questions (Groq LLM) |
| 📑 PDF Report Agent | `agents/pdf_agent.py` | Generates downloadable PDF summary |
| 🗄️ Database Layer | `db.py` | Users, saved profiles, schemes, analytics |
| 🔐 Auth | `auth.py` | Login / signup / guest access |
| 🛠️ Admin Panel | `admin.py` | Add/edit/delete schemes via UI |
| 📊 Analytics | `analytics_page.py` | Usage dashboard |
| 🎛️ Orchestrator | `orchestrator.py` | Coordinates all agents, logs searches |

Schemes now live in a **SQLite database** (`scheme_app.db`, auto-created on
first run) instead of a static JSON file, so admins can edit them live.
`data/schemes.json` is only used once, to seed the database the very first
time the app runs.

## How to Run

### 1. Install dependencies (one-time)
```
pip install -r requirements.txt
```

### 2. Run the app
```
streamlit run app.py
```

### 3. First-time Login

An administrator account is initialized during the first setup. The administrator credentials are managed securely by the application owner and are not publicly disclosed.

Citizens can create their own account from the **Sign Up** tab or continue as a guest without registering.

### 4. Using the Admin Panel

Log in as `admin` → select "🛠️ Admin Panel" in the sidebar → you can:
- **View All Schemes**: see every scheme currently in the system
- **Add New Scheme**: fill in a form (name, eligibility rules, documents,
  steps, both languages) — saved instantly to the database
- **Edit / Delete a Scheme**: pick any scheme, change any field, or remove
  it entirely

Changes take effect immediately for every citizen using the app — no
restart needed.

### 5. Using the Analytics Dashboard

Log in as `admin` → select "📊 Analytics" → see:
- Total searches performed
- Most frequently matched schemes (bar chart)
- Most commonly missing documents (bar chart) — useful for identifying
  which documents citizens most need help obtaining
- Occupation and age breakdowns of who's using the app

All analytics data is anonymous — only demographic fields and match
results are logged, never names or contact details.

### 6. Project Structure
```
scheme-app/
├── app.py                    # Main entry point: auth gate + navigation
├── auth.py                   # Login / signup / guest UI
├── admin.py                  # Admin panel UI
├── analytics_page.py         # Analytics dashboard UI
├── orchestrator.py           # Coordinates all agents, logs searches
├── db.py                     # SQLite database layer
├── scheme_app.db             # Auto-created on first run (SQLite file)
├── requirements.txt
├── .env.example
├── data/
│   └── schemes.json          # One-time seed data for the database
├── fonts/                    # (optional) Tamil font files for PDF
└── agents/
    ├── profile_agent.py
    ├── eligibility_agent.py
    ├── document_agent.py
    ├── guide_agent.py
    ├── deadline_agent.py
    ├── faq_agent.py
    └── pdf_agent.py
```

### 7. Technologies Used
- Python
- Streamlit
- SQLite
- Groq LLM
- ReportLab
- dotenv
- JSON

### 8. Authors
PK Keerthika
S Sangavi
S Praveena
