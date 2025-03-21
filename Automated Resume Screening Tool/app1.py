import streamlit as st
import fitz  # PyMuPDF for PDF extraction
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Function to extract text from PDF resumes
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf_document:
        for page in pdf_document:
            text += page.get_text("text")
    return text

# Function to clean extracted text
def clean_resume(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"\W", " ", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip().lower()  # Remove extra spaces

    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words("english")]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens)

# Function to display raw and cleaned text side by side
def display_raw_and_cleaned_text(raw_text, cleaned_text):
    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        st.subheader("📄 Raw Extracted Text")
        st.text_area("Raw Text", value=raw_text, height=300)

    with col2:
        st.subheader("✅ Cleaned Text")
        st.text_area("Cleaned Text", value=cleaned_text, height=300)

# Main function
def main():
    st.title("📂 Resume Screening Tool")
    upload_file = st.file_uploader("Upload Resume", type=["txt", "pdf"])

    if upload_file is not None:
        try:
            if upload_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(upload_file)
            else:
                resume_text = upload_file.read().decode("utf-8")
        except UnicodeDecodeError:
            resume_text = upload_file.read().decode("latin-1")

        if resume_text:
            cleaned_resume = clean_resume(resume_text)
            display_raw_and_cleaned_text(resume_text, cleaned_resume)
        else:
            st.error("⚠️ No text was extracted. Please upload a valid resume.")

if __name__ == "__main__":
    main()
