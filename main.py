import os
import json
import re
from datetime import datetime
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === Config ===
pdf_dir = "./pdfs"
input_json_path = "challenge1b_input.json"
output_json_path = "challenge1b_output.json"
TOP_K = 5

# === Load input
with open(input_json_path, "r", encoding="utf-8") as f:
    input_data = json.load(f)

persona = input_data["persona"]["role"]
job = input_data["job_to_be_done"]["task"]
document_list = input_data["documents"]
filenames = [doc["filename"] for doc in document_list]

# === Keywords
bias_keywords = ["vegetarian", "gluten-free", "buffet", "dinner", "corporate", "main", "side", "entree"]
penalty_keywords = ["breakfast", "pancake", "toast", "scrambled egg", "morning"]
boost_keywords = ["dinner", "lunch", "main", "side", "entree", "buffet"]

# === Extract section-style blocks
def extract_sections_from_pdf(filepath):
    reader = PdfReader(filepath)
    all_sections = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for j, line in enumerate(lines):
            if re.match(r"^[A-Z][\w\s\-]{3,50}$", line):  # likely a title
                body = "\n".join(lines[j+1:j+6])
                section = {
                    "document": os.path.basename(filepath),
                    "section_title": line,
                    "text": body,
                    "page_number": i + 1
                }
                all_sections.append(section)
    return all_sections

# === Extract and filter sections
all_sections = []
for file in filenames:
    pdf_path = os.path.join(pdf_dir, file)
    all_sections.extend(extract_sections_from_pdf(pdf_path))

# === TF-IDF scoring
corpus = [s["section_title"] + " " + s["text"] for s in all_sections]
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(corpus)

# 🎯 Refined query
query = (
    "Vegetarian gluten-free dishes suitable for a buffet-style dinner at a corporate event. "
    "Exclude breakfast. Prefer sides and mains. "
    "Focus on falafel, lasagna, baba ganoush, ratatouille, sushi."
)
query_vec = vectorizer.transform([query])
scores = cosine_similarity(query_vec, X).flatten()

# === Apply boosting/penalizing
for i, sec in enumerate(all_sections):
    score = scores[i]

    # Penalty for breakfast terms
    if any(kw in sec["text"].lower() for kw in penalty_keywords):
        score -= 0.2

    # Boost if filename contains dinner/lunch/side/main
    if any(kw in sec["document"].lower() for kw in boost_keywords):
        score += 0.1

    sec["score"] = score

# === Select top K sections
top_sections = sorted(all_sections, key=lambda s: -s["score"])[:TOP_K]

# === Build output
output = {
    "metadata": {
        "input_documents": filenames,
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": datetime.now().isoformat()
    },
    "extracted_sections": [],
    "subsection_analysis": []
}

for rank, sec in enumerate(top_sections, start=1):
    refined_text = sec["text"].replace("\n", " ").strip()
    if len(refined_text) > 1000:
        refined_text = refined_text[:1000].rsplit(".", 1)[0] + "."

    output["extracted_sections"].append({
        "document": sec["document"],
        "section_title": sec["section_title"],
        "importance_rank": rank,
        "page_number": sec["page_number"]
    })
    output["subsection_analysis"].append({
        "document": sec["document"],
        "refined_text": refined_text,
        "page_number": sec["page_number"]
    })

# === Save output
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print(f"✅ Output written to {output_json_path}")
