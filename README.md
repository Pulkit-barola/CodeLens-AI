# 🧠 CodeLens AI

CodeLens AI is an AI-powered code analysis platform that helps developers understand, debug, and improve code quality across multiple programming languages. It combines static analysis, runtime execution, AI-powered explanations, quality scoring, complexity estimation, and analytics into a single dashboard.

---

## 🚀 Features

### 🔍 AI Code Analysis
- AI-generated code explanations
- Bug detection and debugging assistance
- Code improvement suggestions
- Warning and risk identification

### ⚡ Runtime Execution
- Execute Python code directly
- View runtime output
- Runtime error detection

### ⭐ Code Quality Report
- Overall quality score
- Readability analysis
- Maintainability analysis
- Performance analysis
- Security analysis
- Detailed progress indicators

### ⏱ Complexity Analysis
- Estimated Time Complexity
- Estimated Space Complexity
- Complexity Level Classification

### 📊 Analytics Dashboard
- Total analyses tracking
- Language usage statistics
- Interactive visualizations
- Download analytics data
- Export charts as images

### 📜 Analysis History
- Store previous analyses
- View code history
- Track quality scores

### 🗑 Data Management
- Reset analytics data
- Reset history data

### 🌍 Multi-Language Support
- Python
- JavaScript
- Java
- C++
- SQL

---

## 🛠 Tech Stack

### Frontend
- Streamlit
- Streamlit Ace Editor

### Backend
- Python

### Data Visualization
- Plotly
- Pandas

### AI & Analysis
- Groq API
- Static Code Analysis
- Runtime Execution Engine

### Storage
- JSON-based local storage

---

## 📂 Project Structure

```text
CodeLensAI/
│
├── main.py
├── analyzer.py
├── detector.py
├── executor.py
│
├── data/
│   ├── history.json
│   └── stats.json
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/CodeLensAI.git

cd CodeLensAI
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_API_KEY
```

Never commit API keys to GitHub.

---

## ▶ Run Application

```bash
streamlit run main.py
```

Application will start at:

```text
http://localhost:8501
```

---

## 📈 Dashboard Features

- Total analyses counter
- Language-wise usage tracking
- Interactive analytics charts
- JSON export
- CSV export
- PNG chart export

---

## 📊 Quality Metrics

The application evaluates code based on:

- Readability
- Maintainability
- Performance
- Security

An overall score is generated automatically.

---

## ⏱ Complexity Metrics

The system estimates:

- Time Complexity
- Space Complexity
- Complexity Difficulty Level

Examples:

| Pattern | Complexity |
|----------|----------|
| Single Loop | O(n) |
| Nested Loop | O(n²) |
| Fibonacci Recursion | O(2ⁿ) |
| Constant Operations | O(1) |

---

## 🔒 Security Checks

The analyzer detects risky patterns such as:

- eval()
- exec()
- Infinite loops
- Unsafe system calls
- Suspicious code structures

---

## 📸 Screenshots

Add screenshots here after deployment.

### Analyzer

![Analyzer](screenshots/analyzer.png)

### Dashboard

![Dashboard](screenshots/dashboard.png)

---

## 🚀 Future Improvements

- PDF Report Export
- Monaco Editor Integration
- Team Collaboration
- Cloud Database
- Advanced Complexity Detection
- AI Code Refactoring

---

## 👨‍💻 Author

Pulkit Barola

B.Tech CSE Student

AI • Full Stack Development • Automation

---

## 📜 License

This project is licensed under the MIT License.
