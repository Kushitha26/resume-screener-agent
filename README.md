# 🤖 AI Resume Screener Agent

The **AI Resume Screener Agent** helps recruiters and HR teams quickly shortlist candidates by automatically evaluating resumes against a given Job Description (JD).

It reads multiple PDF resumes, compares them with the JD using an LLM (Llama 3 via Groq), and generates for each candidate:

- A match score (0–100)
- Fit level (Strong / Medium / Weak)
- Key strengths and gaps
- Final recommendation (Interview / Hold / Reject)

This reduces manual screening time and makes the process more consistent and explainable.

---

## 🚀 Features

- Upload **Job Description** (paste text or upload PDF)
- Upload **multiple candidate resumes** (PDF)
- Automatic evaluation of each resume against the JD
- For each candidate:
  - `match_score` (0–100)
  - `fit_level` (Strong / Medium / Weak)
  - `strengths` (bullet points)
  - `gaps` (missing skills/experience)
  - `recommendation` (Interview / Hold / Reject)
  - Short explanation (`reason_summary`)
- Ranked candidate table sorted by match score
- One-click **Download results as CSV**
- (Optional) Script to export results to **Google Sheets** using a service account

---

## 🧠 High-Level Architecture

1. **User / HR Recruiter**
   - Provides a Job Description (JD)
   - Uploads multiple PDF resumes

2. **UI Layer – Streamlit App (`app.py`)**
   - JD input: text area or JD PDF upload
   - Resume upload: multiple PDFs
   - Calls the screening logic for each resume and displays the ranked results in a table
   - Provides CSV download for offline analysis

3. **Processing Layer – Screening Logic (`resume_screener.py`)**
   - Extracts the JD text and resume text
   - Builds a structured prompt
   - Calls the **Groq Llama 3.1 8B** model with the JD and resume
   - Parses the JSON output into: score, fit level, strengths, gaps, recommendation, and summary

4. **Document Layer – PDF Text Extraction (`utils.py`)**
   - Uses `PyPDF2` to read and extract text from JD and resume PDFs

5. **Model API – Groq (Llama 3)**
   - Receives the prompt from the app
   - Returns a structured evaluation in JSON format

6. **Output Layer**
   - Combines all results into a `pandas` DataFrame
   - Displays a ranked table in Streamlit
   - Allows the user to download results as a CSV file

7. **(Optional) Data Export – Google Sheets**
   - A separate script `test_google.py` demonstrates how the same data can be pushed to a Google Sheet using the Google Sheets API and a service account.

---

## 🧰 Tech Stack & Tools

**Language & Runtime**
- Python 3.x

**AI Model**
- **Groq Llama 3.1 8B** (used as the LLM to compare JD and resumes)

**Framework & Libraries**
- **Streamlit** – UI for interaction and visualization
- **PyPDF2** – PDF parsing for resumes and JDs
- **pandas** – tabular data handling and CSV export
- **python-dotenv** – environment variable management
- **groq** – Python client for Groq API
- **gspread + oauth2client** (optional) – Google Sheets integration

**UI**
- **Streamlit** web interface (can be hosted on Streamlit Community Cloud)

**APIs**
- Groq API (for LLM)
- (Optional) Google Sheets API (via service account)

**Database / Storage**
- Local CSV export (`resume_screening_results.csv`)
- (Optional) Google Sheet named `Resume_Screener_Results`

---

## ⚙️ Setup & Local Run Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/resume-screener-agent.git
cd resume-screener-agent
