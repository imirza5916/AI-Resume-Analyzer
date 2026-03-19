# 🎯 AI Resume Analyzer

An AI-powered tool that analyzes your resume against job descriptions, providing match scores, ATS compatibility ratings, and actionable recommendations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **AI Match Score** — Semantic similarity using BERT embeddings
- **ATS Compatibility** — Score breakdown across 5 categories
- **Skills Analysis** — Detects your skills vs. job requirements
- **Missing Skills** — Highlights what to add to your resume
- **Smart Recommendations** — Actionable tips to improve
- **Weak Phrase Detection** — Replace passive language with strong verbs
- **Modern Dark UI** — Clean, responsive React frontend
- **Drag & Drop Upload** — Easy PDF/DOCX handling

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask (API server)
- Sentence-Transformers (BERT - all-MiniLM-L6-v2)
- PyMuPDF (PDF parsing)
- python-docx (DOCX parsing)

**Frontend:**
- React 18
- Modern CSS (dark theme, no frameworks)

## 📁 Project Structure

```
ai-resume-analyzer/
├── app.py                 # Flask backend API
├── requirements.txt       # Python dependencies
├── package.json           # React dependencies
├── public/
│   └── index.html         # HTML template
└── src/
    ├── App.js             # Main React component
    ├── App.css            # Styles (dark theme)
    ├── index.js           # React entry point
    └── index.css          # Base styles
```

## 🚀 Quick Start

### 1. Set up the Backend

```bash
# Navigate to project folder
cd ai-resume-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python app.py
```

The API will run at `http://localhost:5000`

### 2. Set up the Frontend

Open a **new terminal**:

```bash
# Navigate to project folder
cd ai-resume-analyzer

# Install dependencies
npm install

# Start React dev server
npm start
```

The app will open at `http://localhost:3000`

## 📸 How It Works

1. **Upload your resume** (PDF or DOCX)
2. **Paste a job description**
3. **Click Analyze** — AI compares your resume to the job
4. **View results:**
   - Match Score (0-100%)
   - ATS Compatibility Score
   - Skills breakdown
   - Missing skills
   - Recommendations

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze` | POST | Analyze resume against job description |
| `/api/health` | GET | Health check |

### Example Request

```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "resume=@resume.pdf" \
  -F "job_description=Looking for a Python developer..."
```

## 📊 Scoring Breakdown

**Match Score** — Semantic similarity between resume and job description using BERT embeddings.

**ATS Score** (100 points total):
- Contact Info: 15 pts
- Skills Match: 35 pts
- Keywords: 25 pts
- Formatting: 15 pts
- Action Verbs: 10 pts

## 🎨 Customization

### Change Colors

Edit `src/App.css` — key color variables:
```css
/* Accent colors */
#667eea  /* Primary purple */
#764ba2  /* Secondary purple */
#00d4aa  /* Success green */
#ff4757  /* Error red */
#fbbf24  /* Warning yellow */
```

### Add More Skills

Edit `app.py` — add to `SKILLS_DB` dictionary:
```python
SKILLS_DB = {
    "Your Category": ["skill1", "skill2", "skill3"],
    ...
}
```

## 📝 License

MIT License — free to use and modify!

---

Made with ❤️ by Ibrahim Mirza
