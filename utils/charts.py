import plotly.graph_objects as go


# ---------------------------
# ATS SCORE GAUGE
# ---------------------------

def ats_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "ATS Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#38bdf8"},
                "steps": [
                    {"range": [0, 50], "color": "#7f1d1d"},
                    {"range": [50, 75], "color": "#854d0e"},
                    {"range": [75, 100], "color": "#14532d"},
                ],
            },
        )
    )

    fig.update_layout(
        height=350,
        template="plotly_dark"
    )

    return fig


# ---------------------------
# SKILL RADAR
# ---------------------------

def skill_radar(skills_found, missing_skills=None):

    labels = [
        "Technical",
        "Projects",
        "Tools",
        "Communication",
        "Problem Solving"
    ]

    score = min(len(skills_found) * 5, 100)

    values = [
        score,
        max(score - 5, 0),
        max(score - 10, 0),
        max(score - 15, 0),
        max(score - 8, 0)
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=labels,
            fill="toself",
            name="Skills"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=450,
        template="plotly_dark"
    )

    return fig


# ---------------------------
# SKILL GAP CHART
# ---------------------------

def skill_gap_chart(skills_found, missing_skills):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Found Skills", "Missing Skills"],
            y=[
                len(skills_found),
                len(missing_skills)
            ]
        )
    )

    fig.update_layout(
        title="Skill Gap Analysis",
        height=400,
        template="plotly_dark"
    )

    return fig


# ---------------------------
# CAREER OVERVIEW
# ---------------------------

def career_score_chart(
    ats_score,
    skills_found,
    missing_skills,
    target_score=75
):

    if isinstance(skills_found, list):
        skills_found = len(skills_found)

    if isinstance(missing_skills, list):
        missing_skills = len(missing_skills)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[
                "ATS Score",
                "Skills Found",
                "Missing Skills",
                "Target"
            ],
            y=[
                ats_score,
                skills_found,
                missing_skills,
                target_score
            ]
        )
    )

    fig.update_layout(
        title="Career Overview",
        height=450,
        template="plotly_dark"
    )

    return fig


# ---------------------------
# GITHUB LANGUAGES PIE CHART
# ---------------------------

def github_languages_chart(top_languages):

    if not top_languages:
        return None

    langs = [item[0] for item in top_languages]
    counts = [item[1] for item in top_languages]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=langs,
                values=counts,
                hole=0.4,
                marker=dict(
                    colors=[
                        "#38bdf8",
                        "#818cf8",
                        "#3b82f6",
                        "#06b6d4",
                        "#a78bfa"
                    ]
                ),
                hoverinfo="label+percent+value",
                textinfo="label"
            )
        ]
    )

    fig.update_layout(
        title="Top Languages by Repository Count",
        height=400,
        template="plotly_dark",
        margin=dict(t=50, b=20, l=20, r=20)
    )

    return fig


# ---------------------------
# GITHUB PROFILE SCORE GAUGE
# ---------------------------

def github_score_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "GitHub Profile Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#3b82f6"},
                "steps": [
                    {"range": [0, 50], "color": "#7f1d1d"},
                    {"range": [50, 75], "color": "#854d0e"},
                    {"range": [75, 100], "color": "#14532d"},
                ],
            },
        )
    )

    fig.update_layout(
        height=350,
        template="plotly_dark"
    )

    return fig