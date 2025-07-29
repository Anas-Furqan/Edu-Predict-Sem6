# 🎓 EduPredict - Academic Success Predictor

**EduPredict** is an AI-powered academic performance prediction dashboard that helps identify students at risk of dropout or underperformance using machine learning and interactive visualizations.

---

## 📁 Project Structure
EduPredict_Project/
│
├── app/
│ └── edu_predict_app.py
├── data/
│ ├── academic_raw.csv  
│ └── academic_cleaned.csv
├── models/
│ ├── rf_model.pkl
│ ├── anomaly_model.pkl
│ └── trend_model.pkl
├── assets/
│ ├── flowchart.svg
│ └── dfd_level0.svg
├── requirements.txt
└── README.md

---

## 🚀 Key Features

- 🔐 Role-based Login (Student / Teacher / Counselor)
- 🔮 Predict Academic Status: Dropout / Enrolled / Graduate
- 🚨 Anomaly Detection (Isolation Forest)
- 📈 Semester Grade Forecasting (Trend Prediction)
- 📊 Interactive Visualizations and Advanced Analytics
- 📄 Report Download as TXT
- 📬 Google Form Feedback Integration
- ✨ Modern UI Styling (Streamlit + CSS + Animations)

---

## 🧠 Machine Learning Models Used

| Purpose                | Model Used           |
|------------------------|----------------------|
| Academic Status        | Random Forest        |
| Anomaly Detection      | Isolation Forest     |
| Grade Trend Prediction | Linear Regression    |

---

## 📊 Dataset Details

- 📌 **Source:** UCI ML Repository (#697)
- 👥 **Records:** ~4500 Students
- 🧾 **Features:** Age, Grades, Gender, Economic Indicators, Course Info
- 🎯 **Target:** Dropout / Enrolled / Graduate

---

## 🛠️ Tech Stack

| Area     | Tools / Libraries                |
|----------|----------------------------------|
| Language | Python                           |
| ML       | scikit-learn, XGBoost, joblib    |
| Dashboard| Streamlit, Plotly, Lottie        |
| Styling  | HTML, CSS, Google Fonts          |
| Hosting  | Streamlit Cloud                  |

---

## 📦 How to Run Locally

> Make sure you have Python 3.10+ and pip installed.

1. Clone this repository or unzip it:
```bash
git clone https://github.com/yourusername/EduPredict_Project.git
