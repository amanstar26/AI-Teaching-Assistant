from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_question_paper_pdf(
    content,
    filename="question_paper.pdf"
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Question Paper",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    for line in content.split("\n"):

        elements.append(
            Paragraph(
                line,
                styles["BodyText"]
            )
        )

    doc.build(elements)

    return filename