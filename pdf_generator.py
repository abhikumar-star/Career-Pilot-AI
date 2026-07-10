from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

def create_pdf(report_text, filename="Career_Report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    # Title
    story.append(Paragraph("CareerPilot AI", title_style))
    story.append(Paragraph("AI Career Analysis Report", heading_style))
    story.append(Spacer(1, 20))

    # Process AI report line by line
    for line in report_text.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        # Markdown headings
        if line.startswith("###"):
            story.append(
                Paragraph(
                    "<b>" + line.replace("###", "").strip() + "</b>",
                    heading_style
                )
            )

        elif line.startswith("##"):
            story.append(
                Paragraph(
                    "<b>" + line.replace("##", "").strip() + "</b>",
                    heading_style
                )
            )

        elif line.startswith("#"):
            story.append(
                Paragraph(
                    "<b>" + line.replace("#", "").strip() + "</b>",
                    heading_style
                )
            )

        else:
            # Remove markdown bullets
            line = line.replace("**", "")
            line = line.replace("* ", "• ")

            story.append(Paragraph(line, body_style))

    doc.build(story)

    return filename
