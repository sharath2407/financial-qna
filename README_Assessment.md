# Financial Document Q&A — Streamlit (Assessment Submission)

## 📌 About the Project  
This project was developed as part of my **assessment assignment**.  
The goal was to build a **Streamlit web application** that can:  
- Accept **PDF/Excel financial documents**  
- Extract and process relevant **financial data (Revenue, Expenses, Profit, Assets, Liabilities, Cash Flow, etc.)**  
- Provide an **interactive Q&A system** using natural language queries  
- Run locally using **Ollama (local small language models)**  

---

## 🛠️ Steps I Followed During Development  

1. **Project Setup**  
   - Created a new Python virtual environment  
   - Installed required packages (`streamlit`, `pandas`, `pdfplumber`, `openpyxl`, `requests`)  
   - Set up a clean folder structure  

2. **Document Processing**  
   - Implemented `extractor.py` to handle **PDF parsing** with `pdfplumber`  
   - Added support for **Excel files** using `pandas` and `openpyxl`  
   - Wrote regex-based logic to extract **key financial metrics** (Revenue, Net Income, Assets, etc.)  

3. **Question-Answering System**  
   - Implemented `qna.py` to connect with **Ollama’s local API**  
   - Designed a custom prompt template for financial Q&A  
   - Ensured fallback handling when answers cannot be found in documents  

4. **Streamlit Web App**  
   - Built `app.py` with:  
     - **File uploader** for PDF/Excel  
     - **Extraction preview** with metrics and tables  
     - **Interactive chat interface** for asking questions  
   - Added status indicators and error handling  

5. **Testing**  
   - Tested with multiple **sample financial documents** (Income Statements, Balance Sheets, Cash Flow Statements)  
   - Verified extraction accuracy and Q&A responses  

6. **Final Deployment (Local)**  
   - Configured **Ollama** locally with `llama2` model  
   - Integrated with the Streamlit app  
   - Packaged the project and prepared it for GitHub submission  

---

## 🚀 How to Run  

### 1. Clone Repo & Setup  
```bash
git clone <your-repo-url>
cd financial-qna
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Ollama (for local LLM)  
```bash
ollama pull llama2
ollama run llama2
```

### 3. Start the Streamlit App  
```bash
streamlit run app.py
```

---

## 📊 Example Workflow  
1. Upload a **financial PDF or Excel**  
2. Preview extracted tables and metrics (Revenue, Profit, Assets, etc.)  
3. Click **“Index Document”**  
4. Ask a question in natural language, e.g.:  
   - *“What was the Net Income in 2022?”*  
   - *“Compare Total Assets and Liabilities.”*  
   - *“Show me the Revenue trend.”*  

---

## ✅ Success Criteria Achieved  
- [x] Document Upload (PDF/Excel)  
- [x] Extraction of financial metrics & tables  
- [x] Interactive Q&A with Ollama (local SLMs)  
- [x] Clean UI with Streamlit  
- [x] Error handling & user feedback  

---

## 📂 Project Structure  
```
financial-qna/
├─ app.py                # Streamlit app
├─ extractor.py          # PDF & Excel extraction
├─ qna.py                # Q&A with Ollama
├─ requirements.txt
├─ README.md
└─ sample_files/         # (optional test docs)
```

---

## ⚠️ Notes & Limitations  
- Extraction accuracy depends on document formatting.  
- Current regex logic works best on clean text-based PDFs/Excels.  
- For scanned PDFs, OCR would be needed (future improvement).  
