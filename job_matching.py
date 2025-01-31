import re
from sentence_transformers import SentenceTransformer, util

# Load BERT Model
model = SentenceTransformer("all-MiniLM-L6-v2")

def clean_text(text):
    """Removes special characters, numbers, and extra spaces, and expands job description terms."""
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip().lower()

    # Expanded synonym mapping for various tech fields
    synonyms = {
        "cybersecurity": "cyber network security penetration testing firewall ethical hacking encryption malware",
        "software development": "programming coding python java c++ javascript software engineer backend frontend full-stack",
        "analytics": "data analysis sql tableau power bi statistics visualization big data",
        "AI": "artificial intelligence machine learning deep learning neural networks nlp tensorflow pytorch scikit-learn llms",
        "data science": "data analytics pandas numpy statistics regression modeling big data databases",
        "IT tools": "cloud computing aws azure gcp databases sql nosql devops ci/cd",
        "problem-solving": "critical thinking debugging optimization troubleshooting software architecture",
        "networking": "network engineer CCNA network security TCP/IP cloud security infrastructure",
        "cloud computing": "aws azure gcp cloud security kubernetes docker serverless computing devops",
        "cyber defense": "penetration testing vulnerability assessment SIEM IDS IPS security operations",
        "mobile development": "android ios swift kotlin flutter react-native mobile ui",
        "blockchain": "cryptocurrency smart contracts ethereum solidity defi web3 blockchain security"
    }

    for key, value in synonyms.items():
        text = text.replace(key, value)

    return text

def extract_skills(text):
    """Extracts common technical skills from text."""
    skill_list = [
        "python", "java", "c++", "machine learning", "deep learning", "neural networks",
        "tensorflow", "pytorch", "nlp", "cybersecurity", "sql", "power bi", "tableau",
        "data analysis", "cloud computing", "android development", "web development",
        "javascript", "api", "encryption", "penetration testing", "database management",
        "object-oriented programming", "html", "css", "xgboost", "kotlin", "ui/ux",
        "aws", "azure", "gcp", "kubernetes", "docker", "network security", "blockchain"
    ]
    
    found_skills = [skill for skill in skill_list if skill in text.lower()]
    return list(set(found_skills))

def compute_similarity(resume_text, job_description):
    """Computes semantic similarity using BERT embeddings."""
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
    return round(similarity_score * 100, 2)

if __name__ == "__main__":
    # Load the extracted resume text
    with open("resume_text.txt", "r", encoding="utf-8") as file:
        resume_text = file.read()

    # Ask the user to input a job description
    print("\n🔹 Enter a job description:")
    job_description = input("> ")

    # Clean both texts
    resume_text_cleaned = clean_text(resume_text)
    job_description_cleaned = clean_text(job_description)

    # Compute similarity score
    similarity_score = compute_similarity(resume_text_cleaned, job_description_cleaned)

    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Find missing skills
    missing_skills = list(set(job_skills) - set(resume_skills))

    # Print results
    print("\n🔹 Job Matching Results:")
    print(f"🔹 Resume Similarity to Job Description: {similarity_score}%")

    if similarity_score > 80:
        print("✅ Strong match! Your resume is highly relevant to the job.")
    elif similarity_score > 50:
        print("⚡ Moderate match. Consider adding missing skills to improve relevance.")
    else:
        print("🚀 Low match. Try tailoring your resume with more relevant keywords.")

    # Display missing skills
    if missing_skills:
        print(f"\n⚠️ Missing Skills: {', '.join(missing_skills)}")
        print("📌 Recommendation: Consider adding projects or certifications related to these skills.")
    else:
        print("\n✅ Your resume covers all required skills!")
