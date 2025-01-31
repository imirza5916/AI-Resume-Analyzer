import re
import pandas as pd
from collections import Counter

def load_resume_text(file_path):
    """Load the cleaned resume text from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().lower()

# Define job-related keywords
job_keywords = {
    "AI/ML": {
        "high": ["machine learning", "deep learning", "neural networks", "nlp", "tensorflow", "pytorch"],
        "medium": ["classification models", "clustering", "computer vision", "scikit-learn"],
        "low": ["artificial intelligence", "data science"]
    },
    "Cybersecurity": {
        "high": ["cryptography", "penetration testing", "network security", "firewall", "vulnerability assessment"],
        "medium": ["security protocols", "threat detection", "ethical hacking"],
        "low": ["cybersecurity", "encryption"]
    },
    "Software Development": {
        "high": ["java", "c++", "python", "software development", "full stack", "backend"],
        "medium": ["javascript", "api", "framework", "cloud computing"],
        "low": ["frontend", "programming", "development"]
    },
    "Analytics": {
        "high": ["sql", "power bi", "tableau", "data visualization", "business intelligence"],
        "medium": ["data analysis", "predictive modeling", "statistics"],
        "low": ["analytics", "reporting", "excel"]
    }
}

def keyword_matching(resume_text):
    """Counts occurrences of job-related keywords in the resume with weight adjustments."""
    keyword_counts = {category: 0 for category in job_keywords}

    for category, levels in job_keywords.items():
        for level, keywords in levels.items():
            weight = 3 if level == "high" else 2 if level == "medium" else 1  # Assign weights
            
            for keyword in keywords:
                keyword_counts[category] += len(re.findall(r"\b" + re.escape(keyword) + r"\b", resume_text)) * weight

    return keyword_counts

if __name__ == "__main__":
    # Load cleaned resume text
    resume_text = load_resume_text("resume_text.txt")

    # Perform keyword matching
    keyword_results = keyword_matching(resume_text)

    # Convert results to a DataFrame for visualization
    df = pd.DataFrame(list(keyword_results.items()), columns=["Category", "Keyword Match Count"])

    # Print results in a clean format
    print("\nKeyword Matching Results:")
    print(df.to_string(index=False))  # Print DataFrame in a table format
