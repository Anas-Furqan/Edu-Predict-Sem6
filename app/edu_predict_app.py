import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from datetime import datetime
import time
import socket

def is_localhost():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        return local_ip.startswith("127.") or local_ip.startswith("192.168.") or local_ip == "localhost"
    except:
        return False


st.set_page_config(
    page_title="EduPredict - Academic Success Predictor", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎓"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main { 
        background: linear-gradient(135deg, #f0f2f6 0%, #e8ecf4 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #28a745);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        color: white;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #1f77b4, #17a2b8);
        color: white;
        font-weight: 600;
        border-radius: 25px;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        font-weight: 600;
        border-radius: 25px;
        border: none;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
    }
    
    .prediction-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(31, 38, 135, 0.4);
        margin: 1rem 0;
        text-align: center;
    }
    
    .success-card {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: white;
    }
    
    .error-card {
        background: linear-gradient(135deg, #dc3545, #e83e8c);
        color: white;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(31, 38, 135, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='main-header'>
    <h1>🎓 EduPredict</h1>
    <p style='font-size: 1.2rem; margin: 0;'>AI-Powered Academic Success Predictor</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background-color:#fff3cd;padding:15px;border-radius:10px;border:1px solid #ffeeba;margin-bottom:20px;'>
    <h4 style='color:#856404;margin:0;'>📢 Important: Predictions are advisory only. For academic support, consult your mentors.</h4>
</div>
""", unsafe_allow_html=True)

auth_users = {
    "student": "student123",
    "teacher": "teach123",
    "counselor": "counsel123"
}

st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #1f77b4, #28a745); 
     border-radius: 15px; margin-bottom: 1rem; color: white;'>
    <h2>🔐 Login</h2>
</div>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.sidebar.text_input("👤 Username", key="user", placeholder="Enter username")
    password = st.sidebar.text_input("🔒 Password", type="password", key="pass", placeholder="Enter password")
    
    if st.sidebar.button("🚀 Login", use_container_width=True):
        if username in auth_users and password == auth_users[username]:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.sidebar.success("✅ Login successful!")
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid credentials")
    
    with st.sidebar.expander("🔍 Demo Accounts"):
        st.write("**Student:** student / student123")
        st.write("**Teacher:** teacher / teach123") 
        st.write("**Counselor:** counselor / counsel123")

if st.session_state.logged_in:
    role = st.session_state.username.capitalize()
    
    st.sidebar.markdown(f"""
    <div style='background: linear-gradient(135deg, #28a745, #20c997); padding: 1rem; 
         border-radius: 15px; text-align: center; color: white; margin-bottom: 1rem;'>
        <h3>👤 {role}</h3>
        <p>Welcome back!</p>
        <small>Session: {datetime.now().strftime('%H:%M')}</small>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    def load_lottieurl(url):
        try:
            r = requests.get(url, timeout=5)
            return r.json()
        except:
            return None

    lottie_animation = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_ydo1amjm.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=160, key="logo")

    try:
        df = pd.read_csv("data/academic_cleaned.csv")
        model = joblib.load("models/rf_model.pkl")
        anomaly_model = joblib.load("models/anomaly_model.pkl")
        trend_model = joblib.load("models/trend_model.pkl")
        models_loaded = True
    except Exception as e:
        st.error(f"⚠️ Error loading models: {str(e)}")
        st.info("Please ensure 'data/academic_cleaned.csv' and model files exist in the correct directories.")
        models_loaded = False

    if models_loaded:
        def rebuild_target(row):
            if row["Target_Graduate"] == 1:
                return "Graduate"
            elif row["Target_Enrolled"] == 1:
                return "Enrolled"
            else:
                return "Dropout"

        df["Grade"] = df.apply(rebuild_target, axis=1)

        tab1, tab2 = st.tabs(["🎯 Prediction & Insights", "📈 Advanced Analytics"])

        with tab1:
            col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h3 style='color: #1f77b4; margin-bottom: 1rem;'>🧾 Student Profile</h3>
            </div>
            """, unsafe_allow_html=True)
            
            age = st.slider("📅 Age at Enrollment", 17, 60, 22)
            admission_grade = st.slider("📝 Admission Grade", 0.0, 200.0, 120.0)
            gender = st.selectbox("👥 Gender", ["male", "female"])
            scholarship = st.selectbox("🎓 Scholarship Holder", ["yes", "no"])
            tuition_paid = st.selectbox("💰 Tuition Fees Up to Date", ["yes", "no"])
            sem1_grade = st.slider("📚 1st Sem Grade", 0.0, 20.0, 12.0)
            sem2_grade = st.slider("📖 2nd Sem Grade", 0.0, 20.0, 12.0)
            unemployment = st.slider("📉 Unemployment Rate", 0.0, 20.0, 7.5)
            inflation = st.slider("💹 Inflation Rate", 0.0, 10.0, 3.0)
            gdp = st.slider("🏦 GDP", 0.0, 200000.0, 100000.0)
            
            if st.button("🔮 Predict Academic Outcome", use_container_width=True):
                base_input = df.drop(columns=[col for col in df.columns if "Target" in col or col == "Grade"])
                model_columns = base_input.columns.tolist()
                input_template = pd.DataFrame(columns=model_columns)
                input_template.loc[0] = 0

                input_template["Age at enrollment"] = age
                input_template["Admission grade"] = admission_grade
                input_template["Gender"] = 1 if gender == "male" else 0
                input_template["Scholarship holder"] = 1 if scholarship == "yes" else 0
                input_template["Tuition fees up to date"] = 1 if tuition_paid == "yes" else 0
                input_template["Curricular units 1st sem (grade)"] = sem1_grade
                input_template["Curricular units 2nd sem (grade)"] = sem2_grade
                input_template["Unemployment rate"] = unemployment
                input_template["Inflation rate"] = inflation
                input_template["GDP"] = gdp

                input_template = input_template[model_columns]

                prediction = model.predict(input_template)[0]
                probabilities = model.predict_proba(input_template)[0]
                confidence = round(probabilities[prediction] * 100, 2)
                label_map = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}
                result = label_map[prediction]

                if anomaly_model.predict(input_template)[0] == -1:
                    st.error("🚨 Unusual academic profile detected (Anomaly)!")

                if result == "Dropout":
                    st.markdown(f"""
                    <div class='prediction-card error-card'>
                        <h2>❌ Predicted: {result}</h2>
                        <h3>Confidence: {confidence}%</h3>
                    </div>
                    """, unsafe_allow_html=True)
                elif sem1_grade < 8 or sem2_grade < 8:
                    st.markdown(f"""
                    <div class='prediction-card warning-card'>
                        <h2>⚠️ Predicted: {result} (Low Academic Performance)</h2>
                        <h3>Confidence: {confidence}%</h3>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='prediction-card success-card'>
                        <h2>🎓 Predicted: {result}</h2>
                        <h3>Confidence: {confidence}%</h3>
                    </div>
                    """, unsafe_allow_html=True)

                st.info(f"Confidence Score: {confidence}%")

                sem2_pred = trend_model.predict([[sem1_grade]])[0]
                st.info(f"Predicted Semester-2 Grade (Trend Model): {round(sem2_pred, 2)}")

                report = f"""
                ═══════════════════════════════════════
                🎓 EDUPREDICT ACADEMIC ANALYSIS REPORT
                ═══════════════════════════════════════
                
                Role: {role}
                Prediction: {result}
                Confidence: {confidence}%
                Anomaly: {"Yes" if anomaly_model.predict(input_template)[0] == -1 else "No"}
                Predicted Sem-2 Grade: {round(sem2_pred, 2)}
                
                Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                EduPredict - AI-Powered Academic Success Predictor
                By Muhammad Anas (2209E01)
                ═══════════════════════════════════════
                """
                st.download_button("📄 Download Report", report, 
                                 file_name="edu_predict_report.txt", use_container_width=True)

        with col2:
            st.markdown("""
            <div class='metric-card'>
                <h3 style='color: #1f77b4; margin-bottom: 1rem;'>📊 Performance Insights</h3>
            </div>
            """, unsafe_allow_html=True)

            chart_type = st.selectbox("Choose Chart", ["Class Distribution", "Gender vs Grade", "Semester Grade Trend"])

            if chart_type == "Class Distribution":
                fig = px.pie(df, names="Grade", title="Class Distribution",
                           color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1'])
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type == "Gender vs Grade":
                fig = px.box(df, x="Gender", y="Admission grade", title="Admission Grade by Gender")
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type == "Semester Grade Trend":
                fig = px.line(df[["Curricular units 1st sem (grade)", "Curricular units 2nd sem (grade)"]].reset_index(),
                              title="Semester-wise Grade Progress")
                st.plotly_chart(fig, use_container_width=True)

            with st.expander("📌 Summary"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("📊 Total Records", df.shape[0])
                    st.metric("🎓 Graduates", df[df['Grade'] == "Graduate"].shape[0])
                with col_b:
                    st.metric("❌ Dropouts", df[df['Grade'] == "Dropout"].shape[0])
                    st.metric("📝 Avg Admission Grade", round(df["Admission grade"].mean(), 2))

        with tab2:
            st.subheader("📊 Deep Dive into Academic Patterns")

            st.markdown("#### 🔹 Enrollment Count by Course")
            fig_course = px.histogram(df, x="Course", color="Grade", barmode="group")
            st.plotly_chart(fig_course, use_container_width=True)
            if is_localhost():
                st.download_button("📥 Download Enrollment Chart", fig_course.to_image(format="png"), file_name="course_chart.png")
            else:
                st.info("📥 Chart downloads are only available in the local version.")

            st.markdown("#### 🔹 Dropout Ratio by Age Group")
            df["Age Group"] = pd.cut(df["Age at enrollment"], bins=[16, 20, 25, 30, 40, 60],
                             labels=["17–20", "21–25", "26–30", "31–40", "41+"])
            dropout_by_age = df[df["Grade"] == "Dropout"]["Age Group"].value_counts(normalize=True).sort_index()
            fig_age = px.bar(x=dropout_by_age.index, y=dropout_by_age.values * 100,
                     labels={"x": "Age Group", "y": "Dropout %"}, title="Dropout Percentage by Age Group")
            st.plotly_chart(fig_age, use_container_width=True)
            if is_localhost():
                st.download_button("📥 Download Dropout Chart", fig_age.to_image(format="png"), file_name="dropout_age_chart.png")
            else:
                st.info("📥 Chart downloads are only available in the local version.")

            st.markdown("#### 🔹 Average Grade by Scholarship Status")
            df["Scholarship Label"] = df["Scholarship holder"].map({1: "Yes", 0: "No"})
            grade_scholar = df.groupby("Scholarship Label")[["Curricular units 1st sem (grade)", 
                                                     "Curricular units 2nd sem (grade)"]].mean().reset_index()
            fig_scholar = px.bar(grade_scholar, x="Scholarship Label", y=["Curricular units 1st sem (grade)", 
                                                                   "Curricular units 2nd sem (grade)"],
                         barmode="group", title="Average Grades: Scholarship vs Non-Scholarship")
            st.plotly_chart(fig_scholar, use_container_width=True)
            if is_localhost():
                st.download_button("📥 Download Scholarship Chart", fig_scholar.to_image(format="png"), file_name="scholarship_chart.png")
            else:
                st.info("📥 Chart downloads are only available in the local version.")

            st.markdown("#### 🔹 Impact of GDP on Admission Grades")
            fig_gdp = px.scatter(df, x="GDP", y="Admission grade", color="Grade",
                         title="GDP vs Admission Grade", trendline="ols")
            st.plotly_chart(fig_gdp, use_container_width=True)
            if is_localhost():
                st.download_button("📥 Download GDP Chart", fig_gdp.to_image(format="png"), file_name="gdp_chart.png")
            else:
                st.info("📥 Chart downloads are only available in the local version.")

        st.markdown("---")
        if role == "Student":
            st.info("📚 Use this dashboard to monitor your academic standing and get early warnings.")
        elif role == "Teacher":
            st.info("👩‍🏫 Guide students better by tracking their academic progress and predicting risks.")
        else:
            st.info("🧠 Identify high-risk cases and intervene proactively as a counselor.")

        st.markdown("### 📬 Feedback & Support")
        st.markdown("[📩 Submit Feedback](https://forms.gle/Am71U3oEjHG42sJ59)")
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); 
             border-radius: 15px; margin-top: 2rem;'>
            <p><strong>EduPredict</strong> | Built with ❤️ for Academic Insight</p>
            <p><em>Made By Muhammad Anas</em></p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("🚫 Cannot proceed without loading the required models and data files.")
        st.info("Please check if these files exist:")
        st.code("""
        📁 Project Structure:
        ├── data/
        │   └── academic_cleaned.csv
        ├── models/
        │   ├── rf_model.pkl
        │   ├── anomaly_model.pkl
        │   └── trend_model.pkl
        └── app/
            └── edu_predict_app.py
        """)

else:
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: rgba(255,255,255,0.1); 
         border-radius: 20px; margin: 2rem 0;'>
        <h2 style='color: #1f77b4;'>🔐 Please Login</h2>
        <p>Please log in with a valid username and password to continue.</p>
    </div>
    """, unsafe_allow_html=True)