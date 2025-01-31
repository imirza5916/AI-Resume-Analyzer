from sentence_transformers import SentenceTransformer, util

# Load a lightweight sentence similarity model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_recommendations(resume_text, job_description):
    """
    Generates AI-based recommendations for improving the resume based on a single job description.
    """
    # Convert texts into embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    # Compute similarity score
    similarity_score = round(util.pytorch_cos_sim(resume_embedding, job_embedding).item() * 100, 2)

    # **Initialize recommendations with Job Matching Score (ONLY ONCE)**
    recommendations = [f"🔹 Job Matching Score: {similarity_score}%"]

    # **Feedback based on score range**
    if similarity_score < 50:
        recommendations.append("🔹 Your resume has a low match with the job description. Consider adding relevant skills, certifications, or projects.")
    elif similarity_score < 70:
        recommendations.append("🔹 Your resume matches moderately. You can improve it by emphasizing key skills and tailoring descriptions to match the job.")
    else:
        recommendations.append("✅ Strong match! Ensure your resume highlights key achievements and aligns with the job requirements.")

    # **Expanded keyword list across multiple tech fields**
    important_keywords = [
        # Software Development
        "Python", "Java", "C++", "JavaScript", "TypeScript", "Node.js", "React", "Django", "Spring Boot",
        "Full Stack Development", "Backend Development", "Frontend Development", "REST APIs", "Microservices",
        
        # Data Science & Analytics
        "Machine Learning", "Deep Learning", "Neural Networks", "TensorFlow", "PyTorch", "Data Engineering",
        "Big Data", "Data Analysis", "SQL", "PostgreSQL", "NoSQL", "MongoDB", "ETL Pipelines", "Hadoop", "Apache Spark",

        # Cybersecurity
        "Cybersecurity", "Network Security", "Penetration Testing", "Ethical Hacking", "Incident Response",
        "Encryption", "Firewalls", "SIEM", "Threat Intelligence", "Risk Management",

        # Cloud Computing & DevOps
        "Cloud Computing", "AWS", "Azure", "Google Cloud Platform", "DevOps", "CI/CD Pipelines", "Kubernetes",
        "Docker", "Terraform", "Cloud Security", "Serverless Computing", "Load Balancing",

        # AI & NLP
        "Artificial Intelligence", "NLP", "Computer Vision", "LLMs", "Chatbots", "Reinforcement Learning",
        "Transformer Models", "Text Processing", "Sentiment Analysis", "Speech Recognition", 

        # Miscellaneous
        "Blockchain", "Web3", "IoT", "AR/VR", "Embedded Systems", "Quantum Computing"
    ]

    # Convert resume text to lowercase and find existing skills
    resume_lower = resume_text.lower()
    existing_skills = {kw.lower() for kw in important_keywords if kw.lower() in resume_lower}

    # Find missing skills based on job description
    job_keywords = {kw.lower() for kw in important_keywords if kw.lower() in job_description.lower()}
    missing_keywords = list(job_keywords - existing_skills)

    # **Ensure missing keywords are always displayed**
    if missing_keywords:
        recommendations.append(f"📝 Consider adding some of these key skills or technologies: {', '.join(missing_keywords[:10])}.")
    else:
        recommendations.append("✅ Your resume already contains most of the required skills.")

    # **Check for weak action words**
    weak_phrases = ["responsible for", "helped with", "worked on"]
    if any(phrase in resume_lower for phrase in weak_phrases):
        recommendations.append("💡 Use stronger action words like 'Developed', 'Designed', 'Implemented', 'Optimized', 'Engineered', 'Led'.")

    # **Final return with correct formatting**
    return "\n".join(recommendations)