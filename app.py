

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import re
import fitz  # PyMuPDF
import docx
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Config
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max

# Load model once at startup
print("🚀 Loading AI model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded!")

# Skills database organized by category
SKILLS_DB = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "c", 
        "go", "rust", "kotlin", "swift", "ruby", "php", "scala", "r", "matlab"
    ],
    "Frontend": [
        "react", "vue", "angular", "html", "css", "tailwind", "bootstrap", 
        "next.js", "svelte", "sass", "webpack", "redux"
    ],
    "Backend": [
        "node.js", "django", "flask", "spring boot", "express", "fastapi", 
        "rails", ".net", "laravel", "graphql", "rest api"
    ],
    "Databases": [
        "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", 
        "dynamodb", "firebase", "oracle", "sqlite", "cassandra"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", 
        "jenkins", "ci/cd", "linux", "nginx", "serverless"
    ],
    "Data Science & AI": [
        "machine learning", "deep learning", "tensorflow", "pytorch", 
        "pandas", "numpy", "scikit-learn", "nlp", "computer vision",
        "data analysis", "statistics", "neural networks", "llm"
    ],
    "Tools & Methods": [
        "git", "agile", "scrum", "jira", "figma", "postman", 
        "microservices", "api design", "unit testing", "system design"
    ],
}

ALL_SKILLS = [skill for skills in SKILLS_DB.values() for skill in skills]

WEAK_PHRASES = [
    "responsible for", "helped with", "worked on", "assisted in",
    "participated in", "was involved in", "duties included", "tasked with"
]

STRONG_VERBS = [
    "Developed", "Engineered", "Designed", "Implemented", "Optimized",
    "Led", "Architected", "Automated", "Delivered", "Achieved",
    "Increased", "Reduced", "Launched", "Built", "Created", "Streamlined",
    "Spearheaded", "Transformed", "Orchestrated", "Pioneered"
]


def extract_text(filepath):
    """Extract text from PDF or DOCX."""
    try:
        if filepath.lower().endswith(".pdf"):
            text = ""
            with fitz.open(filepath) as doc:
                for page in doc:
                    text += page.get_text()
            return text.strip()
        elif filepath.lower().endswith(".docx"):
            doc = docx.Document(filepath)
            return "\n".join([p.text for p in doc.paragraphs]).strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
    return ""


def clean_text(text):
    """Clean and normalize text for comparison."""
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def compute_similarity(resume_text, job_text):
    """Compute semantic similarity using BERT."""
    embeddings = model.encode([resume_text, job_text], convert_to_tensor=True)
    score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
    return round(score * 100, 1)


def extract_skills(text):
    """Extract skills from text."""
    text_lower = text.lower()
    found = {}
    for category, skills in SKILLS_DB.items():
        category_skills = [s for s in skills if s in text_lower]
        if category_skills:
            found[category] = category_skills
    return found


def get_flat_skills(skills_dict):
    """Flatten skills dict to list."""
    return [s for skills in skills_dict.values() for s in skills]


def check_weak_phrases(text):
    """Check for weak action phrases."""
    text_lower = text.lower()
    return [phrase for phrase in WEAK_PHRASES if phrase in text_lower]


def count_strong_verbs(text):
    """Count strong action verbs."""
    text_lower = text.lower()
    return sum(1 for verb in STRONG_VERBS if verb.lower() in text_lower)


def calculate_ats_score(resume_text, job_text, resume_skills, job_skills):
    """Calculate ATS compatibility score with breakdown."""
    scores = {}
    
    # Contact info (15 points)
    contact_score = 0
    if re.search(r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b', resume_text):
        contact_score += 8
    if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume_text):
        contact_score += 7
    scores["Contact Info"] = contact_score
    
    # Skills match (35 points)
    flat_resume = get_flat_skills(resume_skills)
    flat_job = get_flat_skills(job_skills)
    if flat_job:
        matched = len([s for s in flat_job if s in flat_resume])
        skill_score = int((matched / len(flat_job)) * 35)
    else:
        skill_score = 20  # Default if no specific skills in job desc
    scores["Skills Match"] = skill_score
    
    # Keyword density (25 points)
    job_words = set(clean_text(job_text).split())
    resume_words = set(clean_text(resume_text).split())
    if job_words:
        overlap = len(job_words.intersection(resume_words))
        keyword_score = int(min((overlap / len(job_words)) * 50, 25))
    else:
        keyword_score = 15
    scores["Keywords"] = keyword_score
    
    # Formatting & length (15 points)
    word_count = len(resume_text.split())
    if 400 <= word_count <= 700:
        format_score = 15
    elif 300 <= word_count <= 900:
        format_score = 10
    else:
        format_score = 5
    scores["Formatting"] = format_score
    
    # Action verbs (10 points)
    verb_count = count_strong_verbs(resume_text)
    verb_score = min(verb_count * 2, 10)
    scores["Action Verbs"] = verb_score
    
    total = sum(scores.values())
    return {"total": min(total, 100), "breakdown": scores}


def generate_recommendations(match_score, ats_score, resume_skills, job_skills, weak_phrases, word_count):
    """Generate actionable recommendations."""
    recommendations = []
    
    # Match score feedback
    if match_score >= 75:
        recommendations.append({
            "type": "success",
            "icon": "✅",
            "title": "Strong Match!",
            "description": "Your resume aligns well with this job. Focus on highlighting your most relevant achievements."
        })
    elif match_score >= 50:
        recommendations.append({
            "type": "warning",
            "icon": "⚡",
            "title": "Moderate Match",
            "description": "Your resume has potential. Tailor it more specifically by incorporating keywords from the job description."
        })
    else:
        recommendations.append({
            "type": "error",
            "icon": "🎯",
            "title": "Needs Improvement",
            "description": "Consider restructuring your resume to better align with this role's requirements."
        })
    
    # Missing skills
    flat_resume = get_flat_skills(resume_skills)
    flat_job = get_flat_skills(job_skills)
    missing = [s for s in flat_job if s not in flat_resume]
    
    if missing:
        recommendations.append({
            "type": "skills",
            "icon": "🔧",
            "title": "Add Missing Skills",
            "description": f"Consider adding these skills if you have them: {', '.join(missing[:6]).title()}",
            "items": missing[:8]
        })
    
    # Weak phrases
    if weak_phrases:
        recommendations.append({
            "type": "warning",
            "icon": "💪",
            "title": "Strengthen Your Language",
            "description": f"Replace weak phrases like \"{weak_phrases[0]}\" with powerful action verbs.",
            "items": STRONG_VERBS[:6]
        })
    
    # Length check
    if word_count < 300:
        recommendations.append({
            "type": "info",
            "icon": "📝",
            "title": "Add More Detail",
            "description": "Your resume seems brief. Consider adding more details about your projects and achievements."
        })
    elif word_count > 900:
        recommendations.append({
            "type": "info",
            "icon": "✂️",
            "title": "Consider Trimming",
            "description": "Your resume is quite long. Focus on the most relevant experiences for this specific role."
        })
    
    # ATS optimization
    if ats_score["total"] < 70:
        recommendations.append({
            "type": "info",
            "icon": "🤖",
            "title": "Boost ATS Compatibility",
            "description": "Use more exact keywords from the job description. Avoid graphics, tables, and unusual formatting."
        })
    
    return recommendations


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Main analysis endpoint."""
    try:
        # Check for file
        if "resume" not in request.files:
            return jsonify({"error": "No resume file uploaded"}), 400
        
        file = request.files["resume"]
        job_description = request.form.get("job_description", "").strip()
        
        if not file or not file.filename:
            return jsonify({"error": "No file selected"}), 400
        
        if not job_description:
            return jsonify({"error": "Job description is required"}), 400
        
        # Check file type
        filename = file.filename.lower()
        if not (filename.endswith(".pdf") or filename.endswith(".docx")):
            return jsonify({"error": "Only PDF and DOCX files are supported"}), 400
        
        # Save and extract text
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
        file.save(filepath)
        
        resume_text = extract_text(filepath)
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        if not resume_text:
            return jsonify({"error": "Could not extract text from resume"}), 400
        
        # Analysis
        clean_resume = clean_text(resume_text)
        clean_job = clean_text(job_description)
        
        match_score = compute_similarity(clean_resume, clean_job)
        
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)
        
        ats_score = calculate_ats_score(resume_text, job_description, resume_skills, job_skills)
        
        weak_phrases = check_weak_phrases(resume_text)
        word_count = len(resume_text.split())
        
        recommendations = generate_recommendations(
            match_score, ats_score, resume_skills, job_skills, weak_phrases, word_count
        )
        
        return jsonify({
            "success": True,
            "match_score": match_score,
            "ats_score": ats_score,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "missing_skills": [s for s in get_flat_skills(job_skills) if s not in get_flat_skills(resume_skills)],
            "recommendations": recommendations,
            "stats": {
                "word_count": word_count,
                "skills_count": len(get_flat_skills(resume_skills)),
                "strong_verbs": count_strong_verbs(resume_text)
            }
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "model_loaded": True})


if __name__ == "__main__":
    print("\n📄 AI Resume Analyzer API running at http://localhost:5000\n")
    app.run(debug=True, port=5000)
