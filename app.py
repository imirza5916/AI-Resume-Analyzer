from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from extract_text import extract_text_from_file
from job_matching import compute_similarity, clean_text
from resume_recommendations import generate_recommendations

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"pdf", "docx"}

def allowed_file(filename):
    """Check if uploaded file is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PDF and DOCX allowed."}), 400

    if not job_description:
        return jsonify({"error": "Job description is required."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Extract text from resume
    resume_text = extract_text_from_file(filepath)

    # Process text
    cleaned_resume = clean_text(resume_text)
    cleaned_job_desc = clean_text(job_description)

    # Compute similarity score
    similarity_score = compute_similarity(cleaned_resume, cleaned_job_desc)

    # Generate recommendations
    recommendations = generate_recommendations(cleaned_resume, cleaned_job_desc)

    # Return JSON response
    return jsonify({
        "similarity_score": round(similarity_score, 2),
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)