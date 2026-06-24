import streamlit as st
import tempfile

from agents.resume_agent import analyze_resume
from agents.pdf_report import generate_pdf_report
from agents.pdf_parser import extract_text_from_pdf
from agents.resume_builder_agent import build_resume
from agents.resume_docx import create_resume_docx
from agents.jd_matcher import match_jd
from agents.job_search import search_jobs
from roles import ROLES
from streamlit_searchbox import st_searchbox
from utils.charts import (
    ats_gauge,
    skill_radar,
    skill_gap_chart,
    career_score_chart,
    github_languages_chart,
    github_score_gauge
)

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

# ------------------------
# THEME
# ------------------------

st.markdown("""
<style>

/* Hide hamburger menu and footer */
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
header { visibility: hidden !important; }

/* App background */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b) !important;
    color: #f1f5f9 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0a0f1e !important;
    border-right: 1px solid #1e293b !important;
}

[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
}

/* Metric cards — force box style */
[data-testid="metric-container"] {
    background: #111827 !important;
    border: 1px solid #334155 !important;
    border-radius: 15px !important;
    padding: 20px !important;
    box-shadow: 0 0 20px rgba(56,189,248,0.2) !important;
}

[data-testid="metric-container"] label,
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="metric-container"] div {
    color: white !important;
}

/* Headings */
h1 { color: white !important; }
h2, h3 { color: #38bdf8 !important; }

/* Expanders */
[data-testid="stExpander"] {
    background: #111827 !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;
}

/* Text area */
.stTextArea textarea {
    background: #111827 !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

/* Dividers */
hr {
    border-color: #334155 !important;
    margin: 24px 0 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #3b82f6) !important;
    color: white !important;
    border-radius: 12px !important;
    height: 50px !important;
    width: 100% !important;
    font-weight: bold !important;
    border: none !important;
}

.stButton>button:hover {
    transform: scale(1.03) !important;
    box-shadow: 0 0 20px rgba(56,189,248,0.4) !important;
}

/* Success / info / error alerts */
[data-testid="stAlert"] {
    background: #111827 !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

/* Progress bar track */
[data-testid="stProgressBar"] {
    background: #1e293b !important;
    border-radius: 10px !important;
}

/* Selectbox / searchbox */
[data-testid="stSelectbox"] > div,
input {
    background: #111827 !important;
    color: white !important;
    border: 1px solid #334155 !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
# SESSION STATE
# ------------------------

if "page" not in st.session_state:
    st.session_state.page = "upload"

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "improved_resume" not in st.session_state:
    st.session_state.improved_resume = ""

if "jd_result" not in st.session_state:
    st.session_state.jd_result = None

if "target_role" not in st.session_state:
    st.session_state.target_role = ""

if "github_result" not in st.session_state:
    st.session_state.github_result = None

if "github_feedback" not in st.session_state:
    st.session_state.github_feedback = None

# ------------------------
# UPLOAD PAGE
# ------------------------

if st.session_state.page == "upload":

    # Hide sidebar on upload page
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    # ------------------------
    # HEADER
    # ------------------------

    col_logo, col_title = st.columns([1, 8])

    with col_logo:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
            width=120
        )

    with col_title:
        st.markdown("""
# 🚀 CareerPilot AI

### AI-Powered Career Intelligence Platform

Analyze resumes, improve ATS score,
generate interview questions,
career roadmaps, jobs and ATS resumes.
""")

    # ------------------------
    # BANNER — split into two columns to avoid Streamlit HTML truncation
    # ------------------------

    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.markdown("""
<style>
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes scanline {
    0%   { top: 0%; }
    100% { top: 100%; }
}
</style>
<div style="background:linear-gradient(135deg,#0a0f1e,#0f172a,#1a1040);background-size:200% 200%;animation:gradientShift 6s ease infinite;border-radius:24px;border:1px solid #1e3a5f;padding:40px 36px;min-height:300px;box-shadow:0 0 80px rgba(56,189,248,0.12),inset 0 1px 0 rgba(255,255,255,0.05);position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;width:100%;height:100%;background-image:radial-gradient(circle,#1e3a5f 1px,transparent 1px);background-size:28px 28px;opacity:0.4;z-index:0;pointer-events:none;"></div>
  <div style="position:absolute;left:0;width:100%;height:2px;background:linear-gradient(90deg,transparent,rgba(56,189,248,0.4),transparent);animation:scanline 4s linear infinite;z-index:1;pointer-events:none;"></div>
  <div style="position:relative;z-index:2;">
    <div style="display:inline-block;background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.3);border-radius:20px;padding:4px 14px;font-size:12px;color:#38bdf8;margin-bottom:14px;letter-spacing:1px;">✦ AI-POWERED CAREER PLATFORM</div>
    <div style="font-size:42px;font-weight:900;color:white;line-height:1.15;letter-spacing:-1px;">
      Land Your<br>
      <span style="background:linear-gradient(90deg,#38bdf8,#818cf8,#3b82f6);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:gradientShift 3s ease infinite;">Dream Role</span>
      <span style="color:white;"> with AI</span>
    </div>
    <div style="color:#64748b;font-size:15px;margin-top:12px;line-height:1.6;">
      Upload your resume → get instant ATS analysis,<br>skill gaps, roadmap and matching jobs.
    </div>
    <div style="margin-top:20px;display:flex;gap:10px;flex-wrap:wrap;">
      <span style="background:rgba(56,189,248,0.12);border:1px solid rgba(56,189,248,0.4);color:#38bdf8;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;">✅ ATS Score</span>
      <span style="background:rgba(139,92,246,0.12);border:1px solid rgba(139,92,246,0.4);color:#a78bfa;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;">🗺️ Roadmap</span>
      <span style="background:rgba(59,130,246,0.12);border:1px solid rgba(59,130,246,0.4);color:#60a5fa;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;">💼 Jobs</span>
      <span style="background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.4);color:#34d399;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;">🎤 Interview</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    with right_col:
        st.markdown("""
<style>
@keyframes float1 { 0%,100%{transform:translateY(0px)} 50%{transform:translateY(-10px)} }
@keyframes float2 { 0%,100%{transform:translateY(0px)} 50%{transform:translateY(-14px)} }
@keyframes float3 { 0%,100%{transform:translateY(0px)} 50%{transform:translateY(-8px)} }
@keyframes float4 { 0%,100%{transform:translateY(0px)} 50%{transform:translateY(-12px)} }
@keyframes blink  { 0%,100%{opacity:1} 50%{opacity:0} }
</style>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px;">

  <div style="background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid rgba(56,189,248,0.5);border-radius:16px;padding:16px;box-shadow:0 0 30px rgba(56,189,248,0.2);animation:float1 3s ease-in-out infinite;">
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
      <div style="width:8px;height:8px;background:#38bdf8;border-radius:50%;box-shadow:0 0 6px #38bdf8;animation:blink 1.5s infinite;"></div>
      <div style="color:#38bdf8;font-size:10px;font-weight:700;letter-spacing:1px;">ATS SCORE</div>
    </div>
    <div style="color:white;font-size:34px;font-weight:900;">87%</div>
    <div style="background:#1e3a5f;border-radius:10px;height:5px;margin-top:10px;">
      <div style="background:linear-gradient(90deg,#38bdf8,#3b82f6);width:87%;height:5px;border-radius:10px;"></div>
    </div>
    <div style="color:#64748b;font-size:10px;margin-top:6px;">Above average ↑</div>
  </div>

  <div style="background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid rgba(139,92,246,0.5);border-radius:16px;padding:16px;box-shadow:0 0 30px rgba(139,92,246,0.2);animation:float2 3.5s ease-in-out infinite;">
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
      <div style="width:8px;height:8px;background:#8b5cf6;border-radius:50%;box-shadow:0 0 6px #8b5cf6;"></div>
      <div style="color:#a78bfa;font-size:10px;font-weight:700;letter-spacing:1px;">SKILLS FOUND</div>
    </div>
    <div style="color:white;font-size:30px;font-weight:900;">15</div>
    <div style="margin-top:8px;">
      <span style="background:rgba(139,92,246,0.2);color:#a78bfa;font-size:9px;padding:2px 7px;border-radius:10px;margin:2px;display:inline-block;">Python</span>
      <span style="background:rgba(139,92,246,0.2);color:#a78bfa;font-size:9px;padding:2px 7px;border-radius:10px;margin:2px;display:inline-block;">ML</span>
      <span style="background:rgba(139,92,246,0.2);color:#a78bfa;font-size:9px;padding:2px 7px;border-radius:10px;margin:2px;display:inline-block;">NLP</span>
    </div>
  </div>

  <div style="background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid rgba(59,130,246,0.5);border-radius:16px;padding:16px;box-shadow:0 0 30px rgba(59,130,246,0.2);animation:float3 4s ease-in-out infinite;">
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;">
      <div style="width:8px;height:8px;background:#3b82f6;border-radius:50%;box-shadow:0 0 6px #3b82f6;"></div>
      <div style="color:#60a5fa;font-size:10px;font-weight:700;letter-spacing:1px;">MATCHING JOBS</div>
    </div>
    <div style="color:white;font-size:11px;margin-bottom:4px;">💼 AI Engineer</div>
    <div style="color:white;font-size:11px;margin-bottom:4px;">💼 ML Engineer</div>
    <div style="color:#64748b;font-size:11px;">💼 Data Scientist</div>
  </div>

  <div style="background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid rgba(6,182,212,0.5);border-radius:16px;padding:16px;box-shadow:0 0 30px rgba(6,182,212,0.2);animation:float4 3.8s ease-in-out infinite;">
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;">
      <div style="width:8px;height:8px;background:#06b6d4;border-radius:50%;box-shadow:0 0 6px #06b6d4;animation:blink 2s infinite;"></div>
      <div style="color:#06b6d4;font-size:10px;font-weight:700;letter-spacing:1px;">ROADMAP</div>
    </div>
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:5px;">
      <div style="width:10px;height:10px;background:#06b6d4;border-radius:50%;flex-shrink:0;"></div>
      <div style="color:white;font-size:10px;">Week 1 ✅</div>
    </div>
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:5px;">
      <div style="width:10px;height:10px;background:#06b6d4;border-radius:50%;flex-shrink:0;"></div>
      <div style="color:white;font-size:10px;">Week 2 ✅</div>
    </div>
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:5px;">
      <div style="width:10px;height:10px;background:#334155;border-radius:50%;flex-shrink:0;"></div>
      <div style="color:#64748b;font-size:10px;">Week 3 🔄</div>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
      <div style="width:10px;height:10px;background:#334155;border-radius:50%;flex-shrink:0;"></div>
      <div style="color:#64748b;font-size:10px;">Week 4 🔒</div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

    st.divider()

    # ------------------------
    # TARGET ROLE
    # ------------------------

    target_role = st_searchbox(
        lambda x: [r for r in ROLES if x.lower() in r.lower()],
        label="🎯 Search Target Role"
    )

    # ------------------------
    # FILE UPLOAD
    # ------------------------

    uploaded_file = st.file_uploader(
        "📄 Upload Your Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(f"✅ Uploaded: {uploaded_file.name}")

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:

                tmp.write(uploaded_file.getvalue())
                pdf_path = tmp.name

            resume_text = extract_text_from_pdf(pdf_path)

            if not resume_text.strip():

                st.error(
                    "❌ Unable to read this PDF. Please upload another resume."
                )

                st.stop()

            st.session_state.resume_text = resume_text

            with st.expander("📄 Resume Text Preview"):

                st.text(
                    st.session_state.resume_text[:3000]
                )

        except Exception as e:

            st.error(f"❌ PDF Error: {str(e)}")

            st.stop()

        # ------------------------
        # ANALYZE BUTTON
        # ------------------------

        if st.button("🚀 Analyze Resume", key="analyze_btn"):

            with st.status(
                "🚀 AI Resume Analysis Started...",
                expanded=True
            ) as status:

                st.write("📄 Extracting Resume Data...")
                st.write("🧠 Detecting Skills...")
                st.write("🎯 Calculating ATS Score...")
                st.write("💼 Finding Matching Jobs...")
                st.write("🗺️ Generating Career Roadmap...")

                try:

                    st.session_state.analysis = analyze_resume(
                        st.session_state.resume_text,
                        target_role
                    )

                    status.update(
                        label="✅ Analysis Complete",
                        state="complete"
                    )

                    st.session_state.target_role = target_role
                    st.session_state.page = "dashboard"

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Analysis Error: {str(e)}"
                    )

# ------------------------
# DASHBOARD PAGE
# ------------------------

if (
    st.session_state.page == "dashboard"
    and st.session_state.analysis
):

    result = st.session_state.analysis

    # ------------------------
    # SIDEBAR NAVIGATION
    # ------------------------

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Skills",
            "Gaps",
            "Roadmap",
            "Jobs",
            "Interview",
            "Resume Builder",
            "JD Matcher"
        ]
    )

    st.sidebar.divider()

    st.sidebar.button(
        "⬅ Back to Upload",
        on_click=lambda:
        st.session_state.update(
            {"page": "upload"}
        )
    )

    # ------------------------
    # DASHBOARD HEADER
    # ------------------------

    col_logo, col_title = st.columns([1, 8])

    with col_logo:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
            width=80
        )

    with col_title:
        st.markdown(f"""
### 🚀 CareerPilot AI — {st.session_state.target_role}
""")

    st.divider()



    # ------------------------
    # DASHBOARD CARDS
    # ------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("ATS Score", f"{result['ats_score']}%")

    with col2:
        st.metric("Skills Found", len(result["skills_found"]))

    with col3:
        st.metric("Missing Skills", len(result["missing_skills"]))

    with col4:
        st.metric("Role Match", st.session_state.target_role)

    st.markdown("""
    <div style="
    height:2px;
    background: linear-gradient(90deg, #38bdf8, #3b82f6, transparent);
    border-radius:2px;
    margin: 24px 0;
    "></div>
    """, unsafe_allow_html=True)

    pdf_file = generate_pdf_report(result)

    with open(pdf_file, "rb") as file:

        st.download_button(
            "📄 Download PDF Report",
            file,
            file_name="CareerPilot_Report.pdf",
            mime="application/pdf"
        )

    # ------------------------
    # DASHBOARD
    # ------------------------

    if page == "Dashboard":

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                ats_gauge(
                    result["ats_score"]
                ),
                width="stretch",
                key="ats_gauge_dashboard"
            )

        with col2:
            st.plotly_chart(
                career_score_chart(
                    result["ats_score"],
                    len(result["skills_found"]),
                    len(result["missing_skills"]),
                    75
                ),
                width="stretch",
                key="career_chart"
            )

        st.subheader("🎯 Recommendations")

        for rec in result["recommendations"]:
            st.info(rec)

    # ------------------------
    # SKILLS
    # ------------------------

    elif page == "Skills":

        st.subheader("🛠 Skills Found")

        st.plotly_chart(
            skill_radar(
                result["skills_found"][:8],
                result["missing_skills"][:8]
            ),
            width="stretch",
            key="radar_chart"
        )

        skills_html = ""

        for skill in result["skills_found"]:
            skills_html += f"""
            <span style="
            background:#0284c7;
            padding:8px 12px;
            border-radius:20px;
            margin:5px;
            display:inline-block;
            color:white;">
            {skill}
            </span>
            """

        st.markdown(skills_html, unsafe_allow_html=True)

        st.subheader("💪 Strengths")

        for strength in result["strengths"]:
            st.write("✅", strength)

    # ------------------------
    # GAPS
    # ------------------------

    elif page == "Gaps":

        st.subheader("⚠️ Missing Skills")

        st.plotly_chart(
            skill_gap_chart(
                result["skills_found"],
                result["missing_skills"]
            ),
            width="stretch",
            key="gap_chart"
        )

        skills_html = ""

        for skill in result["missing_skills"]:
            skills_html += f"""
            <span style="
            background:#be123c;
            padding:8px 12px;
            border-radius:20px;
            margin:5px;
            display:inline-block;
            color:white;">
            {skill}
            </span>
            """

        st.markdown(skills_html, unsafe_allow_html=True)

    # ------------------------
    # ROADMAP
    # ------------------------

    elif page == "Roadmap":

        st.subheader("🗺️ 30-Day Career Roadmap")

        roadmap = result["roadmap"]

        week_configs = [
            ("week1", "📅 Week 1 — Foundations",    "#0284c7"),
            ("week2", "📅 Week 2 — Core Skills",    "#0891b2"),
            ("week3", "📅 Week 3 — Advanced Topics","#0e7490"),
            ("week4", "📅 Week 4 — Final Sprint",   "#155e75"),
        ]

        for key, label, color in week_configs:

            week = roadmap.get(key, {})

            with st.expander(label, expanded=(key == "week1")):

                st.markdown(f"""
                <div style="
                border-left:4px solid {color};
                padding-left:16px;
                margin-bottom:16px;">
                <h4 style="color:{color};">🎯 Goal</h4>
                <p style="color:white;">{week.get("goal", "")}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <h4 style="color:{color}; margin-bottom:8px;">📚 Topics</h4>
                """, unsafe_allow_html=True)

                topics_html = ""

                for topic in week.get("topics", []):
                    topics_html += f"""
                    <span style="
                    background:{color};
                    padding:6px 14px;
                    border-radius:20px;
                    margin:4px;
                    display:inline-block;
                    color:white;
                    font-size:14px;">
                    {topic}
                    </span>
                    """

                st.markdown(topics_html, unsafe_allow_html=True)

                st.markdown(f"""
                <h4 style="color:{color}; margin-top:20px; margin-bottom:8px;">🗓️ Daily Tasks</h4>
                """, unsafe_allow_html=True)

                for task in week.get("daily_tasks", []):
                    st.markdown(f"""
                    <div style="
                    background:#1e293b;
                    border-left:3px solid {color};
                    padding:10px 16px;
                    border-radius:6px;
                    margin-bottom:6px;
                    color:white;
                    font-size:14px;">
                    🔹 {task}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="
                background:#111827;
                border:1px solid {color};
                border-radius:12px;
                padding:16px 20px;
                margin-top:16px;">
                <h4 style="color:{color}; margin-bottom:8px;">🏗️ Mini Project</h4>
                <p style="color:white; margin:0;">{week.get("project", "")}</p>
                </div>
                """, unsafe_allow_html=True)

                if key == "week4":

                    extras = [
                        ("🎤 Interview Prep",          "interview_prep"),
                        ("💼 LinkedIn Tasks",          "linkedin_tasks"),
                        ("🐙 GitHub Tasks",            "github_tasks"),
                        ("📨 Internship Applications", "internship_applications"),
                    ]

                    st.markdown("<br>", unsafe_allow_html=True)

                    for extra_label, field in extras:

                        value = week.get(field, "")

                        if value:

                            st.markdown(f"""
                            <div style="
                            background:#1e293b;
                            border-left:3px solid #38bdf8;
                            padding:12px 16px;
                            border-radius:8px;
                            margin-top:10px;">
                            <strong style="color:#38bdf8;">{extra_label}</strong>
                            <p style="color:white; margin-top:6px; margin-bottom:0;">{value}</p>
                            </div>
                            """, unsafe_allow_html=True)

    # ------------------------
    # JOBS
    # ------------------------

    elif page == "Jobs":

        from agents.job_search import search_jobs

        st.subheader("💼 Live Job Opportunities")

        jobs = search_jobs(
            st.session_state.target_role
        )

        if not jobs:
            st.warning(
                "No jobs found right now."
            )

        else:

            for job in jobs:

                st.markdown(
                    f"""
### {job['title']}

🏢 **{job['company']}**

📍 **{job['location']}**

🌐 **Source:** {job['source']}

[🚀 Apply Here]({job['url']})
"""
                )

                st.divider()

    # ------------------------
    # INTERVIEW
    # ------------------------

    elif page == "Interview":

        st.subheader("🎤 Interview Preparation")

        st.success(
            f"{len(result['interview_questions'])} Questions Generated"
        )

        for i, question in enumerate(
            result["interview_questions"],
            start=1
        ):

            with st.expander(
                f"Question {i}",
                expanded=(i == 1)
            ):
                st.write(question)

    # ------------------------
    # RESUME BUILDER
    # ------------------------

    elif page == "Resume Builder":

        st.subheader("📄 ATS Resume Builder")

        if st.button("Generate ATS Resume", key="resume_builder_btn"):

            with st.spinner("Building ATS-Friendly Resume..."):

                try:

                    st.session_state.improved_resume = build_resume(
                        st.session_state.resume_text,
                        st.session_state.target_role
                    )

                except Exception as e:

                    st.error(f"❌ Resume Builder Error: {str(e)}")

        if st.session_state.improved_resume:

            st.markdown(st.session_state.improved_resume)

            try:

                docx_file = create_resume_docx(
                    st.session_state.improved_resume
                )

                with open(docx_file, "rb") as file:

                    st.download_button(
                        label="📥 Download ATS Resume",
                        data=file,
                        file_name="ATS_Resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            except Exception as e:

                st.error(f"❌ DOCX Error: {str(e)}")

    # ------------------------
    # JD MATCHER
    # ------------------------

    elif page == "JD Matcher":

        st.subheader("🎯 Resume vs Job Description")

        job_description = st.text_area(
            "Paste Job Description Here",
            height=250
        )

        if st.button(
            "Match Resume",
            key="jd_match_btn"
        ):

            with st.spinner(
                "Matching Resume..."
            ):

                try:

                    st.session_state.jd_result = match_jd(
                        st.session_state.resume_text,
                        job_description
                    )

                except Exception as e:

                    st.error(
                        f"❌ JD Match Error: {str(e)}"
                    )

        if "jd_result" in st.session_state and st.session_state.jd_result is not None:

            result = st.session_state.jd_result

            st.divider()

            st.metric(
                "🎯 Match Score",
                f"{result['match_score']}%"
            )

            st.progress(
                result["match_score"] / 100
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "✅ Matching Skills"
                )

                for skill in result[
                    "matching_skills"
                ]:

                    st.success(skill)

            with col2:

                st.subheader(
                    "❌ Missing Keywords"
                )

                for skill in result[
                    "missing_keywords"
                ]:

                    st.error(skill)

            st.divider()

            st.subheader(
                "💡 ATS Suggestions"
            )

            for suggestion in result[
                "suggestions"
            ]:

                st.info(suggestion)