from docx import Document
import re

def extract_results(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    
    pattern = r"^([AB])\s+([\w\s\-/]+?)\s+([\d\.]+)\s+([\w/]+)\s+(.+)$"
    results = []
    for line in text.split("\n"):
        line = line.strip()
        match = re.match(pattern, line)
        if match:
            flag = match.group(1)
            test_name = match.group(2).strip()
            result = match.group(3)
            unit = match.group(4)
            ref_range = match.group(5)
            abnormal = "**" in line or "Low" in ref_range or "High" in ref_range
            results.append({
                "test": test_name,
                "result": result,
                "unit": unit,
                "reference": ref_range,
                "abnormal": abnormal
            })
    return results
def extract_patient_info(text):
    """Extract patient name, DOB, NHS number from text."""
    name = None
    dob = None
    nhs = None
    # Example: look for common patterns
    name_match = re.search(r"Patient\s*[:\-]?\s*([A-Za-z\s]+)", text, re.IGNORECASE)
    if name_match:
        name = name_match.group(1).strip()
    dob_match = re.search(r"DOB\s*[:\-]?\s*(\d{2}[\/\-]\d{2}[\/\-]\d{4})", text, re.IGNORECASE)
    if dob_match:
        dob = dob_match.group(1)
    nhs_match = re.search(r"NHS\s*[:\-]?\s*(\d{10})", text, re.IGNORECASE)
    if nhs_match:
        nhs = nhs_match.group(1)
    return {"name": name, "dob": dob, "nhs": nhs}