from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

def create_study_plan_pdf(
    content,
    filename="study_plan.pdf"
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "AI Generated Study Plan",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    for line in content.split("\n"):

        line = line.strip()

        if not line:
            continue

        elements.append(
            Paragraph(
                line,
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(1, 5)
        )

    doc.build(elements)

    return filename