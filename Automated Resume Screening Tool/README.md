# Automated Resume Screening Tool Using NLP

## 📌 Overview
The **Automated Resume Screening Tool** is designed to help recruiters efficiently screen resumes using **Natural Language Processing (NLP)**. It extracts key details from resumes, analyzes relevant information, and provides insights to assist in candidate selection.

## 🔥 Features
- 📄 Upload resumes in various formats (PDF, DOCX, etc.)
- 🔍 Extracts key information (Name, Email, Skills, Experience, etc.)
- 🏆 Uses **NLP techniques** to analyze and rank candidates
- 📊 Displays structured results for recruiters
- 🚀 User-friendly interface for easy interaction

## 🛠️ Tech Stack
- **Programming Language:** Python 🐍
- **Libraries Used:**
  - `spaCy` (NLP Processing)
  - `pdfminer` / `PyMuPDF` (PDF Parsing)
  - `docx2txt` (Extracting text from DOCX files)
  - `Flask` (For Web Interface)
  - `SQLite` / `MongoDB` (For Data Storage)

## 🚀 How to Run the Project
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Automated-Resume-Screening-NLP.git
   cd Automated-Resume-Screening-NLP
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Update Path for Pickle Files**
   - Ensure you update the path of the **pickle files** (`.pkl`) according to your local directory structure in the script before running the project.

4. **Run the Application**
   ```bash
   python app.py
   ```
5. **Access the Web App**
   Open your browser and go to `http://localhost:5000`

## 📸 Screenshots (Optional)
Include some screenshots of the tool’s interface to give users an idea of its functionality.
Automated Resume Screening Tool/Interface.png


## 🏆 Challenges & Solutions
### ✅ Challenges
- Handling different resume formats
- Extracting relevant skills from unstructured text
- Ensuring accurate ranking of candidates

### 💡 Solutions
- Used `pdfminer` and `docx2txt` to handle PDF and DOCX parsing
- Leveraged `spaCy` for Named Entity Recognition (NER)
- Implemented scoring based on keyword matching and experience analysis

## 🤝 Contributing
Contributions are welcome! Feel free to submit a **pull request** or open an **issue**.

## 📩 Contact
For any queries, reach out to me on **[LinkedIn](https://www.linkedin.com/in/racherla-krishnaprasad-1337b1245)**.

## ⭐ Acknowledgments
- Thanks to the open-source community for amazing libraries!
- Special thanks to my mentors and peers for their support.

If you find this project useful, don’t forget to ⭐ **star the repository**!
