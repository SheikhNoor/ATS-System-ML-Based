# 🚀 ATS Resume Optimization System

<div align="center">

**An AI-Powered Resume Analysis Platform with Advanced OCR Support**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.35-000000?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **ATS Resume Optimization System** is an advanced, AI-powered platform designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). With support for both text-based and image-based PDFs (using OCR), the system provides intelligent analysis, scoring, and personalized suggestions to improve resume effectiveness.

### Why This Project?

- **90%+** of large companies use ATS to filter resumes
- **75%** of qualified candidates are rejected due to poor ATS optimization
- Our system helps bridge this gap with AI-powered analysis and actionable insights

---

## ✨ Key Features

### 🔍 **Intelligent Resume Analysis**
- ✅ **Multi-format Support**: PDF (text & scanned), DOCX
- ✅ **OCR Technology**: Tesseract OCR for image-based/scanned PDFs
- ✅ **Advanced Parsing**: Robust text extraction with pdfplumber and python-docx

### 🎯 **Smart Job Matching**
- ✅ **50+ Job Roles**: Across IT and Non-IT categories
- ✅ **Role-Specific Keywords**: Tailored keyword matching for each position
- ✅ **Experience-Based Analysis**: Separate evaluation for Freshers vs Experienced

### 🤖 **AI-Powered Features**
- ✅ **Summary Analysis**: Automatic detection and evaluation of professional summaries
- ✅ **Quality Scoring**: 0-100 score with detailed breakdowns
- ✅ **Smart Suggestions**: AI-generated recommendations for improvement
- ✅ **Example Generation**: Personalized summary examples based on target role

### 📊 **Comprehensive Scoring System**
- **Overall ATS Score** (0-100%)
  - 🔑 **Keyword Match**: 60% weight
  - 📄 **Formatting Quality**: 20% weight
  - 🎯 **Context Relevance**: 20% weight (TF-IDF)

### 💡 **Modern UI/UX**
- ✅ Dark gradient theme with glassmorphism
- ✅ Drag-and-drop file upload
- ✅ Real-time analysis with loading states
- ✅ Interactive visualizations and charts
- ✅ Fully responsive design

---

## 🛠️ Tech Stack

### **Backend**
```
Python 3.12.10
├── FastAPI 0.104.1          # Modern web framework
├── Uvicorn 0.24.0           # ASGI server
├── scikit-learn 1.8.0       # ML & NLP
├── pdfplumber 0.10.3        # PDF text extraction
├── python-docx 1.1.0        # DOCX parsing
├── pytesseract 0.3.13       # OCR wrapper
├── pdf2image 1.17.0         # PDF → Image conversion
└── Pillow 12.0.0            # Image processing
```

### **Frontend**
```
Node.js 18+
├── Next.js 14.2.35          # React framework
├── React 18.2.0             # UI library
└── Tailwind CSS 3.4.0       # Styling framework
```

### **External Tools**
- **Tesseract OCR** 5.3.3 - Optical Character Recognition
- **Poppler** 24.08.0 - PDF rendering library

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Dashboard Component                                │    │
│  │  - File Upload (Drag & Drop)                        │    │
│  │  - Category Selection (IT/Non-IT)                   │    │
│  │  - Job Role Dropdown (50+ roles)                    │    │
│  │  - Experience Level Toggle                          │    │
│  │  - Results Visualization                            │    │
│  └─────────────────────────────────────────────────────┘    │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP REST API
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  main.py - API Routes                               │    │
│  │  - POST /analyze                                    │    │
│  │  - GET /health                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │ ResumeParser     │  │ ATSEngine        │                 │
│  │ - PDF parsing    │  │ - Keyword match  │                 │
│  │ - DOCX parsing   │  │ - TF-IDF scoring │                 │
│  │ - OCR fallback   │  │ - Recommendations│                 │
│  └──────────────────┘  └──────────────────┘                 │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ SummaryAnalyzer                                      │   │
│  │ - Summary extraction & quality analysis              │   │
│  │ - AI-powered suggestions                             │   │
│  │ - Personalized example generation                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### **Prerequisites**

- ✅ Python 3.12+
- ✅ Node.js 18.0+
- ✅ npm or yarn
- ✅ Tesseract OCR (for scanned PDFs)
- ✅ Poppler (for PDF processing)

### **Step 1: Clone Repository**

```bash
git clone https://github.com/yourusername/ats-resume-optimization.git
cd ats-resume-optimization
```

### **Step 2: Backend Setup**

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Or use specific Python version
python -m pip install -r requirements.txt
```

**Requirements:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
pdfplumber==0.10.3
python-docx==1.1.0
scikit-learn==1.8.0
numpy==2.4.0
pytesseract==0.3.13
pdf2image==1.17.0
pillow>=10.0.0
```

### **Step 3: Install OCR Tools**

#### **Windows:**

**Tesseract OCR:**
```powershell
# Download and install
Invoke-WebRequest -Uri "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe" -OutFile "tesseract.exe"
.\tesseract.exe /S
```

**Poppler:**
```powershell
# Download from: https://github.com/oschwartz10612/poppler-windows/releases/
# Extract to: C:\Users\<username>\poppler\
```

#### **Linux:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

#### **macOS:**
```bash
brew install tesseract poppler
```

### **Step 4: Frontend Setup**

```bash
cd frontend
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

---

## 🚀 Usage

### **Starting the Application**

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload
```
✅ Backend: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
✅ Frontend: http://localhost:3000

### **Using the System**

1. **Open Browser** → http://localhost:3000
2. **Upload Resume** → Drag & drop or click (PDF/DOCX, max 10MB)
3. **Select Category** → IT or Non-IT
4. **Choose Job Role** → 50+ options available
5. **Set Experience** → Fresher (0-2 years) or Experienced (2+ years)
6. **Click Analyze** → Wait 3-5 seconds for results
7. **Review Results:**
   - Overall ATS Score
   - Keyword Match Details
   - Professional Summary Analysis
   - AI-Generated Suggestions
   - Improvement Recommendations

---

## 📚 API Documentation

### **Base URL**: `http://localhost:8000`

### **Endpoints**

#### **1. Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-28T12:00:00.000000"
}
```

#### **2. Analyze Resume**
```http
POST /analyze
Content-Type: multipart/form-data
```

**Parameters:**

| Field | Type | Required | Values |
|-------|------|----------|--------|
| file | File | ✅ Yes | PDF/DOCX (max 10MB) |
| job_category | String | ✅ Yes | "IT" or "Non-IT" |
| job_role | String | ✅ Yes | Any supported role |
| experience_level | String | ✅ Yes | "Fresher" or "Experienced" |

**Example Request (cURL):**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@resume.pdf" \
  -F "job_category=IT" \
  -F "job_role=Full Stack Developer" \
  -F "experience_level=Experienced"
```

**Example Response:**
```json
{
  "overall_score": 75.5,
  "breakdown": {
    "keyword_score": 80.25,
    "formatting_score": 85.0,
    "context_score": 60.0
  },
  "verdict": "Strong",
  "matched_keywords": ["javascript", "react", "nodejs", "api", "git"],
  "missing_keywords": ["docker", "kubernetes", "aws"],
  "recommendations": [
    "Add cloud technologies: docker, kubernetes, aws",
    "Include quantifiable achievements with metrics",
    "Improve resume formatting consistency"
  ],
  "job_category": "IT",
  "job_role": "Full Stack Developer",
  "experience_level": "Experienced",
  "summary_analysis": {
    "has_summary": true,
    "summary_text": "Experienced Full Stack Developer with 5+ years...",
    "score": 85.0,
    "quality": "Excellent",
    "suggestions": [
      "✓ Add more action words like 'led', 'architected'",
      "✓ Include specific metrics and numbers"
    ],
    "analysis": {
      "word_count": 65,
      "sentence_count": 3,
      "action_words": ["developed", "led", "implemented"],
      "has_numbers": true,
      "role_mentioned": true,
      "length_category": "Good"
    },
    "improved_example": "Results-driven Full Stack Developer with 5+ years..."
  }
}
```

### **Supported Job Roles**

**IT Categories:**
- Software Development (7 roles)
- Data & AI (6 roles)
- Cloud & Infrastructure (5 roles)
- Security (4 roles)
- Quality Assurance (3 roles)
- Product & Design (3 roles)
- IT Management (3 roles)
- Specialized IT (4 roles)

**Non-IT Categories:**
- Management & Leadership (5 roles)
- Business & Finance (6 roles)
- Healthcare & Medicine (4 roles)
- Education & Training (3 roles)
- Creative & Media (4 roles)
- Sales & Marketing (5 roles)
- Legal & Compliance (3 roles)
- Operations & Logistics (4 roles)

---

## 📁 Project Structure

```
ATS System/
│
├── backend/                          # FastAPI Backend
│   ├── main.py                       # API entry point & routes
│   ├── ats_engine.py                 # Scoring algorithm
│   ├── resume_parser.py              # PDF/DOCX parsing with OCR
│   ├── summary_analyzer.py           # AI summary analysis
│   ├── requirements.txt              # Python dependencies
│   ├── test_api.py                   # API testing script
│   ├── test_api_docx.py             # DOCX testing script
│   ├── README.md                     # Backend documentation
│   └── __pycache__/                  # Python bytecode cache
│
├── frontend/                         # Next.js Frontend
│   ├── components/
│   │   └── Dashboard.js              # Main UI component (800+ lines)
│   ├── pages/
│   │   ├── _app.js                   # App wrapper with global styles
│   │   ├── _document.js              # Custom HTML document
│   │   └── index.js                  # Home page (mounts Dashboard)
│   ├── styles/
│   │   └── globals.css               # Tailwind imports & custom styles
│   ├── public/                       # Static assets
│   ├── package.json                  # Node.js dependencies
│   ├── next.config.js                # Next.js configuration
│   ├── tailwind.config.js            # Tailwind CSS config
│   ├── postcss.config.js             # PostCSS config
│   ├── jsconfig.json                 # JavaScript paths
│   └── .env.local                    # Environment variables
│
├── README.md                         # Main documentation (this file)
├── OCR_SETUP_COMPLETE.md            # OCR installation guide
├── LICENSE                           # MIT License
└── start.bat                         # Windows startup script (optional)
```

---

## 🎨 Features in Detail

### **1. Resume Parsing**
- Supports PDF (text-based and scanned/image-based)
- Supports DOCX format
- OCR fallback for scanned documents
- Handles various resume layouts and formats

### **2. ATS Scoring Algorithm**

**Keyword Matching (60%):**
- Role-specific keyword database (50+ roles)
- Experience-level keywords (Fresher vs Experienced)
- Case-insensitive matching
- Frequency-based scoring

**Formatting Quality (20%):**
- Section detection (Education, Experience, Skills)
- Structure consistency
- Professional formatting elements

**Context Relevance (20%):**
- TF-IDF vectorization
- Cosine similarity scoring
- Semantic relevance to job role

### **3. Summary Analysis**

**Detection:**
- Automatic extraction from common headers
- Supports: Summary, Objective, Profile, About Me

**Quality Metrics:**
- Word count (optimal: 50-80 words)
- Action word density
- Quantifiable metrics presence
- Role mention verification
- Professional terminology usage

**AI Suggestions:**
- Specific improvements based on analysis
- Weak phrase detection and alternatives
- Length optimization recommendations
- Industry-specific terminology suggestions

---

## 🐛 Troubleshooting

### **Issue: "Failed to fetch"**
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify CORS settings in backend/main.py
# Ensure frontend .env.local has correct API URL
```

### **Issue: OCR not working**
```bash
# Windows - Check Tesseract installation
Test-Path "C:\Program Files\Tesseract-OCR\tesseract.exe"

# Verify Poppler path
# Should be in: C:\Users\<username>\poppler\

# Check resume_parser.py for correct paths
```

### **Issue: Port already in use**
```bash
# Windows
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force
Get-Process | Where-Object {$_.ProcessName -eq "node"} | Stop-Process -Force

# Linux/macOS
killall python
killall node
```

### **Issue: Module import errors**
```bash
# Clear Python cache
cd backend
rm -rf __pycache__
find . -name "*.pyc" -delete

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 🔮 Future Enhancements

- [ ] **User Accounts**: Save and track multiple analyses
- [ ] **Resume Comparison**: Compare multiple versions
- [ ] **PDF Export**: Generate detailed analysis reports
- [ ] **LinkedIn Integration**: Import profile data
- [ ] **Job Scraper**: Match with real job postings
- [ ] **Cover Letter Generator**: AI-powered cover letters
- [ ] **Interview Prep**: Generate interview questions
- [ ] **Multi-language**: Support for multiple languages
- [ ] **Mobile App**: React Native implementation
- [ ] **Browser Extension**: Chrome/Firefox extension
- [ ] **A/B Testing**: Test different resume versions
- [ ] **Analytics Dashboard**: Track improvements over time

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit** your changes: `git commit -m 'Add AmazingFeature'`
4. **Push** to the branch: `git push origin feature/AmazingFeature`
5. **Open** a Pull Request

### **Development Guidelines**

- Follow **PEP 8** for Python code
- Use **ESLint** for JavaScript/React
- Write **clear commit messages**
- Add **tests** for new features
- Update **documentation**

---

## 📝 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 ATS Resume Optimization System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 👨‍💻 Author & Contact

**Your Name**
- 🐙 GitHub: [@SheikhNoor](https://github.com/SheikhNoor)
- 💼 LinkedIn: [Md Nurullah](https://linkedin.com/in/md-nurullah-1481b7253/)
- 📧 Email: [mdnurullah.co@gmail.com](mdnurullah.co@gmail.com)
- 🌐 Website: [yourwebsite.com](https://yourwebsite.com)

---

## 🙏 Acknowledgments

Special thanks to:

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - The React Framework
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR Engine
- [scikit-learn](https://scikit-learn.org/) - Machine Learning library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Poppler](https://poppler.freedesktop.org/) - PDF rendering
- All open-source contributors

---

## 📊 Project Stats

![Stars](https://img.shields.io/github/stars/SheikhNoor/ats-resume-optimization?style=social)
![Forks](https://img.shields.io/github/forks/SheikhNoor/ats-resume-optimization?style=social)
![Issues](https://img.shields.io/github/issues/SheikhNoor/ats-resume-optimization)
![Pull Requests](https://img.shields.io/github/issues-pr/SheikhNoor/ats-resume-optimization)
![Contributors](https://img.shields.io/github/contributors/SheikhNoor/ats-resume-optimization)

---

<div align="center">

### ⭐ **Star this repository if you find it helpful!**

### 🔗 **[Live Demo](#)** | **[Documentation](#)** | **[Report Bug](../../issues)** | **[Request Feature](../../issues)**

Made with ❤️ for job seekers worldwide

**© 2025 ATS Resume Optimization System. All rights reserved.**

</div>
