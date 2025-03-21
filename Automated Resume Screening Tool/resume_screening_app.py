import streamlit as st
import pickle
import nltk
import re
from nltk.corpus import stopwords
import fitz  # PyMuPDF

# Downloading NLTK resources if not already done
nltk.download("punkt")
nltk.download("stopwords")

# Loading model
def load_model():
    try:
        clf = pickle.load(open(r"C:\Users\rache\OneDrive\Desktop\Automated Resume Screening Tool\clf.pkl", "rb"))
        tfidf = pickle.load(open(r"C:\Users\rache\OneDrive\Desktop\Automated Resume Screening Tool\tfidf.pkl", "rb"))
        return clf, tfidf
    except (FileNotFoundError, IOError) as e:
        st.error("Model or TF-IDF file not found. Please check the file paths and try again.")
        return None, None

# Load model and transformer
clf, tfidf = load_model()
if clf is None or tfidf is None:
    st.stop()  # Stop if model loading fails

# Stopwords for text cleaning
STOPWORDS = set(stopwords.words('english'))

# Clean text (including stopwords removal)
def clean_resume(resume_text):
    clean_text = re.sub(r'http\S+\s*', ' ', resume_text)
    clean_text = re.sub(r'RT|cc', ' ', clean_text)
    clean_text = re.sub(r'#\S+', '', clean_text)
    clean_text = re.sub(r'@\S+', '  ', clean_text)
    clean_text = re.sub('[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', r' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    clean_text = ' '.join([word for word in clean_text.split() if word.lower() not in STOPWORDS])
    return clean_text

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_document = fitz.open("pdf", pdf_file)
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text("text")
    pdf_document.close()
    return text

# Validate resume content
def validate_resume_content(resume_text):
    # Common sections found in resumes
    required_sections = ["experience", "education", "skills", "summary", "profile", "objective"]
    matched_sections = [section for section in required_sections if section in resume_text.lower()]
    return len(matched_sections) >= 2  # At least two sections should match

# Calculate resume score based on presence of relevant keywords
def calculate_resume_score(cleaned_resume, required_skills):
    if not required_skills:  # Check if the required_skills list is empty
        return 0  # Return 0 if no skills are defined for the category
    
    score = sum([1 for skill in required_skills if re.search(r'\b' + re.escape(skill.lower()) + r'\b', cleaned_resume.lower())])
    max_score = len(required_skills)
    return (score / max_score) * 100  # Score out of 100

# Web app
def main():
    st.title("Resume Screening Tool")
    upload_file = st.file_uploader("Upload Resume", type=["txt", "pdf"])

    if upload_file is not None:
        try:
            resume_bytes = upload_file.read()
            if upload_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(resume_bytes)
            else:
                resume_text = resume_bytes.decode("utf-8")
        except UnicodeDecodeError:
            resume_bytes = upload_file.read()
            resume_text = resume_bytes.decode("latin-1")

        cleaned_resume = clean_resume(resume_text)

        # Validation checks
        if len(cleaned_resume.split()) < 0:
            st.error("The uploaded document is too short to be a valid resume.")
            st.stop()
        if not validate_resume_content(cleaned_resume):
            st.error("The uploaded document does not appear to be a valid resume. Please upload a proper resume.")
            st.stop()

        input_feature = tfidf.transform([cleaned_resume])
        predictions = clf.predict(input_feature)[0]

        # Full Category Mapping with Skills
        category_mapping = {
            15: ("Java Developer", ["java", "spring", "hibernate", "sql", "j2ee"]),
            23: ("Testing", ["selenium", "automation", "junit", "testng", "manual testing"]),
            8: ("DevOps Engineer", ["docker", "kubernetes", "jenkins", "ci/cd", "aws"]),
            20: ("Python Developer", ["python", "django", "flask", "machine learning", "pandas"]),
            24: ("Web Designing", ["html", "css", "javascript", "photoshop", "ui/ux"]),
            12: ("HR", ["recruitment", "talent acquisition", "employee relations", "performance management"]),
            13: ("Hadoop", ["hadoop", "hive", "pig", "mapreduce", "big data"]),
            3: ("Blockchain", ["blockchain", "smart contracts", "ethereum", "cryptocurrency"]),
            10: ("ETL Developer", ["etl", "data warehouse", "sql", "informatica", "data integration"]),
            18: ("Operations Manager", ["operations", "logistics", "supply chain", "management", "inventory"]),
            6: ("Data Science", ["data science", "machine learning", "statistics", "python", "r"]),
            22: ("Sales", ["sales", "business development", "lead generation", "crm", "negotiation"]),
            16: ("Mechanical Engineer", ["mechanical", "cad", "solidworks", "engineering", "manufacturing"]),
            1: ("Arts", ["drawing", "painting", "sculpture", "design", "visual arts"]),
            7: ("Database", ["sql", "database", "oracle", "mysql", "postgresql"]),
            11: ("Electrical Engineering", ["electrical", "circuit design", "power systems", "electronics"]),
            14: ("Health and fitness", ["nutrition", "exercise", "personal training", "wellness"]),
            19: ("PMO", ["project management", "planning", "coordination", "risk management"]),
            4: ("Business Analyst", ["business analysis", "requirements gathering", "stakeholder", "agile"]),
            9: ("DotNet Developer", [".net", "c#", "asp.net", "mvc", "sql server"]),
            2: ("Automation Testing", ["automation", "selenium", "robot framework", "test automation"]),
            17: ("Network Security Engineer", ["network security", "firewalls", "vpn", "security policies"]),
            21: ("SAP Developer", ["sap", "abap", "sap hana", "fiori", "sap modules"]),
            5: ("Civil Engineer", ["civil engineering", "construction", "autocad", "surveying"]),
            0: ("Advocate", ["legal", "law", "court", "contracts", "litigation"])
        }

        # Get category name and skills for the prediction
        category_name, required_skills = category_mapping.get(predictions, ("Other", []))

        # Calculate resume score
        resume_score = calculate_resume_score(cleaned_resume, required_skills)

        # Display results
        st.success(f"Predicted Category: {category_name}")
        st.info(f"Resume Score: {resume_score:.2f}%")

        # Display key skills matched
        matched_skills = [skill for skill in required_skills if re.search(r'\b' + re.escape(skill.lower()) + r'\b', cleaned_resume.lower())]
        st.subheader("Matched Skills")
        st.write(", ".join(matched_skills) if matched_skills else "No key skills matched.")

        # Display additional evaluation aspects
        st.subheader("Additional Evaluation")
        st.write("Resume Length:", len(cleaned_resume.split()), "words")
        st.write("Overall Relevance:", f"{resume_score:.2f}%")

# Python main
if __name__ == "__main__":
    main()