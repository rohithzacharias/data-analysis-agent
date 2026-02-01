# 🧠 Data Analysis Agent
### Efficient Exploratory Data Analysis with Schema & History Compression

## 🚀 Overview
The **Data Analysis Agent** is an AI-powered system designed to automate **Exploratory Data Analysis (EDA)** while minimizing Large Language Model (LLM) token usage.

Traditional AI-driven data analysis tools repeatedly resend entire dataset schemas and analysis histories, leading to high token costs.  
This project solves that problem by introducing **intelligent compression techniques** for both dataset structure and analytical context.

---

## 🎯 Key Objectives
- Automate exploratory data analysis
- Compress dataset schema without losing semantic meaning
- Compress analysis history while retaining insights
- Reduce LLM token consumption
- Enable scalable, iterative data analysis using AI agents

---

## 🧩 Core Components

### 1️⃣ Schema Compression Module
Summarizes dataset structure by extracting:
- Column names
- Data types
- Missing value ratios
- Basic statistics (mean, min, max)
- Cardinality for categorical features

📉 **Benefit:**  
Reduces large datasets into compact, LLM-friendly representations.

---

### 2️⃣ Analysis History Compression
Condenses previous analytical steps into:
- Key insights
- Important conclusions
- Eliminated redundant context

📉 **Benefit:**  
Prevents repeated token-heavy prompts while preserving reasoning flow.

---

### 3️⃣ EDA AI Agent
An intelligent agent that:
- Reads compressed schema
- Refers to compressed history
- Suggests next analytical steps
- Generates visualizations and insights

---

## 🛠️ Tech Stack

| Category | Tools |
|--------|------|
| Language | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| AI Agent Logic | Custom Rule-based + LLM-ready architecture |
| Notebook | Jupyter |

---

## 📁 Project Structure


---

## 📊 Example Workflow
1. Load dataset
2. Generate compressed schema
3. Perform initial EDA
4. Compress analysis history
5. Iteratively analyze with minimal token overhead

---

## 🔍 Use Cases
- Large dataset exploration
- AI-powered analytics assistants
- Cost-efficient LLM-based data analysis
- Educational data science agents

---

## 📈 Future Enhancements
- LLM integration (OpenAI / Open-source models)
- Vector-based memory for history compression
- Automatic anomaly detection
- Interactive dashboard (Streamlit)

---

## 🤝 Contribution
Contributions are welcome. Please fork the repository and submit a pull request.

---

## 📜 License
This project is licensed under the MIT License.
