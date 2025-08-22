import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from datetime import datetime
import time


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
        anomaly_model = joblib.load("models/anomaly_model.pkl")
        trend_model = joblib.load("models/trend_model.pkl")

        models_dir = "models"
        candidate_files = [
            ("Tuned Logistic Regression", os.path.join(models_dir, "tuned_logistic_regression_model.pkl")),
            ("Tuned Random Forest", os.path.join(models_dir, "tuned_random_forest_model.pkl")),
            ("Tuned XGBoost", os.path.join(models_dir, "tuned_xgboost_model.pkl")),
            ("Baseline Random Forest", os.path.join(models_dir, "rf_model.pkl")),
        ]

        available_models = {}
        for display_name, path in candidate_files:
            if os.path.exists(path):
                try:
                    available_models[display_name] = joblib.load(path)
                except Exception:
                    pass

        default_model_name = None
        tuned_report_path = os.path.join("reports", "model_comparison_tuned.csv")
        if os.path.exists(tuned_report_path):
            try:
                comp_df = pd.read_csv(tuned_report_path)
                if {"Model", "F1 Score"}.issubset(comp_df.columns):
                    best_row = comp_df.sort_values("F1 Score", ascending=False).iloc[0]
                    name_map = {
                        "Tuned Logistic Regression": "Tuned Logistic Regression",
                        "Tuned Random Forest": "Tuned Random Forest",
                        "Tuned XGBoost": "Tuned XGBoost",
                    }
                    best_name_in_report = str(best_row["Model"]).strip()
                    if best_name_in_report in name_map and name_map[best_name_in_report] in available_models:
                        default_model_name = name_map[best_name_in_report]
            except Exception:
                pass

        if default_model_name is None:
            
            for preferred in [
                "Tuned Random Forest",
                "Tuned Logistic Regression",
                "Tuned XGBoost",
                "Baseline Random Forest",
            ]:
                if preferred in available_models:
                    default_model_name = preferred
                    break

        models_loaded = len(available_models) > 0 and anomaly_model is not None and trend_model is not None
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
            
            model_names = list(available_models.keys()) if models_loaded else []
            selected_model_name = None
            selected_model = None
            if model_names:
                if len(model_names) == 1:
                    selected_model_name = model_names[0]
                    selected_model = available_models[selected_model_name]
                else:
                    try:
                        default_index = model_names.index(default_model_name) if default_model_name in model_names else 0
                    except Exception:
                        default_index = 0
                    with st.expander(f"⚙️ Advanced: Choose model (recommended: {default_model_name})", expanded=False):
                        selected_model_name = st.selectbox("🤖 Select Model", model_names, index=default_index)
                    selected_model = available_models[selected_model_name]

            if st.button("🔮 Predict Academic Outcome", use_container_width=True):
                base_input = df.drop(columns=[col for col in df.columns if "Target" in col or col == "Grade"])
                model_columns = base_input.columns.tolist()
                input_template = pd.DataFrame(columns=model_columns)
                defaults = {}
                for col in model_columns:
                    try:
                        if pd.api.types.is_numeric_dtype(df[col]):
                            defaults[col] = float(df[col].median())
                        else:
                            mode_series = df[col].mode()
                            defaults[col] = mode_series.iloc[0] if not mode_series.empty else df[col].iloc[0]
                    except Exception:
                        defaults[col] = 0
                input_template.loc[0] = defaults

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

                for col in input_template.columns:
                    if pd.api.types.is_integer_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
                        input_template[col] = np.round(input_template[col]).astype(df[col].dtype)
                prediction = selected_model.predict(input_template)[0]
                probabilities = selected_model.predict_proba(input_template)[0]
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
                Model: {selected_model_name}
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
            # st.download_button("📥 Download Enrollment Chart", fig_course.to_image(format="png"), file_name="course_chart.png")

            st.markdown("#### 🔹 Dropout Ratio by Age Group")
            df["Age Group"] = pd.cut(df["Age at enrollment"], bins=[16, 20, 25, 30, 40, 60],
                             labels=["17–20", "21–25", "26–30", "31–40", "41+"])
            dropout_by_age = df[df["Grade"] == "Dropout"]["Age Group"].value_counts(normalize=True).sort_index()
            fig_age = px.bar(x=dropout_by_age.index, y=dropout_by_age.values * 100,
                     labels={"x": "Age Group", "y": "Dropout %"}, title="Dropout Percentage by Age Group")
            st.plotly_chart(fig_age, use_container_width=True)
            # st.download_button("📥 Download Dropout Chart", fig_age.to_image(format="png"), file_name="dropout_age_chart.png")

            st.markdown("#### 🔹 Average Grade by Scholarship Status")
            df["Scholarship Label"] = df["Scholarship holder"].map({1: "Yes", 0: "No"})
            grade_scholar = df.groupby("Scholarship Label")[["Curricular units 1st sem (grade)", 
                                                     "Curricular units 2nd sem (grade)"]].mean().reset_index()
            fig_scholar = px.bar(grade_scholar, x="Scholarship Label", y=["Curricular units 1st sem (grade)", 
                                                                   "Curricular units 2nd sem (grade)"],
                         barmode="group", title="Average Grades: Scholarship vs Non-Scholarship")
            st.plotly_chart(fig_scholar, use_container_width=True)
            # st.download_button("📥 Download Scholarship Chart", fig_scholar.to_image(format="png"), file_name="scholarship_chart.png")

            st.markdown("#### 🔹 Impact of GDP on Admission Grades")
            fig_gdp = px.scatter(df, x="GDP", y="Admission grade", color="Grade",
                         title="GDP vs Admission Grade", trendline="ols")
            st.plotly_chart(fig_gdp, use_container_width=True)
            # st.download_button("📥 Download GDP Chart", fig_gdp.to_image(format="png"), file_name="gdp_chart.png")            

            st.markdown("#### 🔹 Correlation Heatmap (Numeric Features)")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr().round(2)
                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    color_continuous_scale="RdBu",
                    zmin=-1,
                    zmax=1,
                    title="Feature Correlations",
                )
                st.plotly_chart(fig_corr, use_container_width=True)

            st.markdown("#### 🔹 3D Performance Scatter")
            if all(c in df.columns for c in [
                "Admission grade", "Curricular units 1st sem (grade)", "Curricular units 2nd sem (grade)"
            ]):
                fig_3d = px.scatter_3d(
                    df,
                    x="Admission grade",
                    y="Curricular units 1st sem (grade)",
                    z="Curricular units 2nd sem (grade)",
                    color="Grade",
                    title="Admission vs Sem-1 vs Sem-2 Grades (3D)",
                )
                fig_3d.update_traces(marker=dict(size=4, opacity=0.85), selector=dict(type='scatter3d'))
                fig_3d.update_layout(scene=dict(
                    xaxis_title='Admission grade',
                    yaxis_title='Sem-1 grade',
                    zaxis_title='Sem-2 grade'
                ))
                st.plotly_chart(fig_3d, use_container_width=True)

            st.markdown("#### 🔹 Dropout Heatmap by Age Group and Scholarship")
            if "Age Group" in df.columns and "Scholarship Label" in df.columns:
                dropout_df = df.copy()
                dropout_df["is_dropout"] = (dropout_df["Grade"] == "Dropout").astype(int)
                pivot = dropout_df.pivot_table(
                    index="Age Group", columns="Scholarship Label", values="is_dropout", aggfunc="mean"
                ).reindex(index=["17–20", "21–25", "26–30", "31–40", "41+"], columns=["Yes", "No"]) * 100
                fig_dropout_heat = px.imshow(
                    pivot,
                    text_auto=True,
                    color_continuous_scale="YlOrRd",
                    origin="upper",
                    labels=dict(color="Dropout %"),
                    title="Dropout % by Age Group × Scholarship",
                )
                st.plotly_chart(fig_dropout_heat, use_container_width=True)

            st.markdown("#### 🔹 Course-wise Grade Distribution (Normalized)")
            if all(c in df.columns for c in ["Course", "Grade"]):
                ct = pd.crosstab(df["Course"], df["Grade"], normalize="index").reset_index()
                course_grade = ct.melt(id_vars="Course", var_name="Grade", value_name="ratio")
                fig_course_stack = px.bar(
                    course_grade,
                    x="Course",
                    y="ratio",
                    color="Grade",
                    title="Normalized Distribution of Grades by Course",
                )
                fig_course_stack.update_layout(barmode="stack", yaxis_tickformat=",.0%")
                st.plotly_chart(fig_course_stack, use_container_width=True)

            st.markdown("#### 🔹 Admission Grade Distribution by Outcome (Violin)")
            if all(c in df.columns for c in ["Admission grade", "Grade"]):
                fig_violin = px.violin(
                    df, y="Admission grade", x="Grade", color="Grade",
                    box=True, points="outliers",
                    title="Admission Grade Distribution by Outcome"
                )
                st.plotly_chart(fig_violin, use_container_width=True)

            st.markdown("#### 🔹 Pathways: Gender → Scholarship → Outcome")
            if all(c in df.columns for c in ["Gender", "Scholarship Label", "Grade"]):
                fig_parallel = px.parallel_categories(
                    df[["Gender", "Scholarship Label", "Grade"]],
                    color=df["Grade"].astype("category").cat.codes,
                    color_continuous_scale=px.colors.sequential.Teal,
                    labels={"Gender": "Gender", "Scholarship Label": "Scholarship", "Grade": "Outcome"},
                    title="Parallel Categories: Gender → Scholarship → Outcome"
                )
                st.plotly_chart(fig_parallel, use_container_width=True)

            st.caption("All charts are interactive. Use hover, zoom, pan, and legend toggles for deeper insights.")

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