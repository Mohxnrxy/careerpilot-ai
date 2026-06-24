from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(result, filename="career_report.pdf"):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "CareerPilot AI Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"ATS Score: {result['ats_score']}%",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Skills Found",
            styles["Heading2"]
        )
    )

    for skill in result["skills_found"]:
        story.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Missing Skills",
            styles["Heading2"]
        )
    )

    for skill in result["missing_skills"]:
        story.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    story.append(PageBreak())

    story.append(
        Paragraph(
            "Recommendations",
            styles["Heading2"]
        )
    )

    for rec in result["recommendations"]:
        story.append(
            Paragraph(
                f"• {rec}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Interview Questions",
            styles["Heading2"]
        )
    )

    for q in result["interview_questions"]:
        story.append(
            Paragraph(
                f"• {q}",
                styles["BodyText"]
            )
        )

    doc.build(story)

    return filename