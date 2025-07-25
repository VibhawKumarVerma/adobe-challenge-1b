# 🧠 Adobe India Hackathon - Challenge 1B (Persona-Driven Document Intelligence)

This project is a submission for **Challenge 1B** of the Adobe India Hackathon. It involves extracting and ranking the most relevant sections from a set of PDF documents based on a given **persona** and **job-to-be-done**.

---

## 🧾 Challenge Summary

- **Persona**: Travel Planner  
- **Job to be done**: Plan a trip of 4 days for a group of 10 college friends  
- **Documents**: Travel-related PDFs including cities, cuisine, history, tips, and activities in the South of France

---

## 🛠️ What the Code Does

- 📄 Reads all input PDFs from the `pdfs/` folder
- ✂️ Extracts section-style titles and nearby content using `PyPDF2`
- 🧠 Scores relevance using TF-IDF + cosine similarity based on a refined query
- ⬆️ Boosts scores for dinner/lunch/main/side sections
- ⬇️ Penalizes breakfast-related content
- 📤 Outputs a structured JSON with top 5 most relevant sections and summaries

---

## 📁 Project Structure
📂 adobe-challenge-1b
├── main.py # Python script to process PDFs and generate output
├── challenge1b_input.json # Input metadata including persona, job, and document list
├── challenge1b_output.json # Output JSON with ranked sections and summaries
├── pdfs/ # Folder containing all input PDFs
└── README.md # This file

## ▶️ How to Run

1. Ensure Python 3 is installed
2. Install required dependencies:

   ```bash
   pip install PyPDF2 scikit-learn
3. Place all your PDFs inside a folder named pdfs/ in the same directory.
4. Run the script:    python main.py
5. The output will be saved to challenge1b_output.json

### 💡 Techniques Used
- TF-IDF vectorization to convert sections into feature vectors
- Cosine similarity to match relevance to a task-specific query
- Heuristic boosting for dinner/main courses and penalty for breakfast
- Title-style text detection using regex

### 🧑‍💻 Author
Vibhaw Kumar Verma, Shahid Mansuri, Harshit Srivastava
Adobe India Hackathon 2025 Participants

### 📜 License
This project is open for non-commercial and educational use only.
