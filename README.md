# 🎓 EduPredict - Academic Success Predictor

**EduPredict** is an AI-powered academic performance prediction dashboard that helps identify students at risk of dropout or underperformance using machine learning and interactive visualizations.

---

## 📁 Project Structure

```
EduPredict_Project/
│
├── app/
│   └── edu_predict_app.py
├── data/
│   └── academic_cleaned.csv
├── models/
│   ├── rf_model.pkl
│   ├── anomaly_model.pkl
│   └── trend_model.pkl
├── assets/
│   ├── flowchart.png
│   └── dfd_level0.png
├── requirements.txt
└── README.md
```

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
| Language | Python 3.11                      |
| ML       | scikit-learn, XGBoost, joblib    |
| Dashboard| Streamlit, Plotly, Lottie        |
| Styling  | HTML, CSS, Google Fonts          |
| Hosting  | Local / Streamlit Cloud (Optional)|

---

## 📦 How to Run Locally

> Make sure you have Python 3.10+ and pip installed.

1. **Clone this repository or unzip it:**
   ```bash
   git clone https://github.com/yourusername/EduPredict_Project.git
   cd EduPredict_Project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app/edu_predict_app.py
   ```

4. **Login with:**
   - **Student:** `student` / `student123`
   - **Teacher:** `teacher` / `teach123`
   - **Counselor:** `counselor` / `counsel123`

---

## 📸 Dashboard Preview (Screenshots)

Attach visuals if using `.docx` or in submission PDF:

- Dashboard UI
- Role-based login
- Predict outcome
- Advanced analytics charts
- Report download
- Feedback form

---

## 📥 Feedback Integration

Google Form is integrated for collecting feedback: 
🔗 **[Submit Feedback Here](https://forms.google.com/your-feedback-link)**

---

## ✅ Final Deliverables

- ✅ Cleaned Dataset
- ✅ Trained Models (.pkl)
- ✅ Full Dashboard Code
- ✅ Flowchart & DFD Diagrams
- ✅ Feedback Integration
- ✅ Video Demonstration (optional)
- ✅ Documentation (README, Report)

---

## 📚 License

This project is built for academic & educational purposes only. All rights to the dataset belong to the UCI ML Repository.

---

## 🙌 Acknowledgments

- UCI Machine Learning Repository
- Streamlit Team
- Scikit-learn, XGBoost, Plotly
- Teachers & Evaluators guiding this project