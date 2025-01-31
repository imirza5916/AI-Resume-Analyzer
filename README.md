# AI Resume Analyzer

🚀 **AI-powered tool that analyzes resumes, matches them against job descriptions, and provides recommendations for improvement.**

## 📌 Features
- **Resume Parsing**: Extracts text from PDF and DOCX resumes.
- **Job Matching**: Compares resume content with job descriptions using NLP & AI models.
- **AI-Based Recommendations**: Suggests missing skills, certifications, and areas for improvement.
- **Keyword Analysis**: Detects industry-relevant keywords and matches them with the job description.
- **Web Interface**: Clean, interactive UI for easy resume upload & analysis.

## 🛠️ Technologies Used
- **Python** (Flask, NLP libraries, PyMuPDF, SpaCy, SentenceTransformers)
- **Machine Learning** (BERT-based similarity models)
- **Frontend** (HTML, CSS, Bootstrap)
- **Document Parsing** (PyMuPDF, python-docx)

## 📂 Project Structure
```
AI Resume Analyzer/
│── app.py                   # Main Flask application
│── job_matching.py          # AI model for job matching
│── resume_recommendations.py # Generates resume improvement suggestions
│── extract_text.py          # Extracts text from PDFs/DOCX
│── resume_parser.py         # Parses structured resume data
│── keyword_matching.py      # Identifies relevant keywords
│── requirements.txt         # Required Python packages
│
├── templates/
│   ├── index.html           # Frontend UI
│
├── uploads/                 # Folder for uploaded resumes (ignored in Git)
│
└── static/                  # (Optional) CSS, JS files for styling/UI enhancements
```

## 🚀 Installation & Usage
### 🔹 1. Clone the Repository
```sh
git clone https://github.com/imirza5916/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 🔹 2. Create a Virtual Environment (Optional but Recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 🔹 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 🔹 4. Run the Flask App
```sh
python app.py
```
Visit **http://127.0.0.1:5000/** in your browser to upload a resume and analyze it.

## 🎯 How It Works
1. **Upload your resume** (PDF or DOCX format).
2. **Enter a job description** for comparison.
3. **The AI analyzes your resume** and computes a **Job Matching Score**.
4. **It suggests missing skills** and **improvements** to tailor your resume better.

## 🛠️ Future Enhancements
- 🔹 Improve job matching with a **custom-trained model**
- 🔹 Expand AI feedback for **better career insights**
- 🔹 Integrate **LinkedIn & Indeed job scraping**

## 💡 Contributing
Pull requests are welcome! Feel free to fork the repo, create a feature branch, and submit a PR.

## 📜 License
MIT License. Feel free to use and improve this project!

---
💡 **Made with passion by Ibrahim Mirza(https://github.com/imirza5916)** 🚀
