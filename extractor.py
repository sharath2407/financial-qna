# extractor.py
import pdfplumber
import pandas as pd
import os
import re
from typing import Dict, Any

def extract_from_pdf(path: str) -> Dict[str, Any]:
    metrics = {}
    tables = []
    text_chunks = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            text_chunks.append(text)
            try:
                for table in page.extract_tables():
                    df = pd.DataFrame(table[1:], columns=table[0]) if table and len(table) > 1 else None
                    if df is not None:
                        tables.append(df)
            except Exception:
                pass
    full_text = "\n\n".join(text_chunks)
    metrics.update(extract_metrics_from_text(full_text))
    return {"text": full_text, "metrics": metrics, "tables": tables}

def extract_from_excel(path: str) -> Dict[str, Any]:
    xls = pd.ExcelFile(path)
    tables = []
    text_chunks = []
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        tables.append(df)
        text_chunks.append(f"Sheet: {sheet}\n" + df.head(20).to_string())
    full_text = "\n\n".join(text_chunks)
    metrics = extract_metrics_from_text(full_text)
    return {"text": full_text, "metrics": metrics, "tables": tables}

def extract_from_file(path: str) -> Dict[str, Any]:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return extract_from_pdf(path)
    elif ext in ('.xls', '.xlsx'):
        return extract_from_excel(path)
    else:
        raise ValueError("Unsupported file type")

def extract_metrics_from_text(text: str) -> Dict[str, Any]:
    metrics = {}
    patterns = {
        'Total Revenue': r"(Total\s+Revenue|Revenue)\s*[:\-]?\s*\$?([0-9,\.]+)",
        'Net Income': r"(Net\s+Income|Net\s+Profit|Profit)\s*[:\-]?\s*\$?([0-9,\.]+)",
        'Gross Profit': r"(Gross\s+Profit)\s*[:\-]?\s*\$?([0-9,\.]+)",
        'Total Assets': r"(Total\s+Assets)\s*[:\-]?\s*\$?([0-9,\.]+)",
        'Total Liabilities': r"(Total\s+Liabilities)\s*[:\-]?\s*\$?([0-9,\.]+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = m.group(2)
            metrics[key] = _parse_number(val)
    return metrics

def _parse_number(s: str):
    try:
        return float(s.replace(',',''))
    except Exception:
        return s