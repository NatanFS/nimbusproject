from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
import logging
from io import BytesIO

from app.utils import format_date

def header(canvas, doc, client_name, report_date):
    canvas.saveState()
    canvas.setFillColorRGB(7/255.0, 55/255.0, 99/255.0)
    canvas.rect(0, 800, 600, 50, stroke=0, fill=1)
    
    canvas.setFillColorRGB(1, 1, 1)
    canvas.setFont('Helvetica-Bold', 16)
    canvas.drawCentredString(300, 820, "Relatório Meteorológico")

    canvas.setFillColorRGB(1.0, 171/255.0, 64/255.0)
    canvas.rect(0, 800, 600, 5, stroke=0, fill=1)
    
    content_left_margin = 77
    content_width = 436
    date_confection_width = canvas.stringWidth("Data de confecção:", 'Helvetica-Bold', 10)
    right_text_width = date_confection_width + canvas.stringWidth(report_date, 'Helvetica', 10)
    right_margin_position = content_left_margin + content_width - right_text_width

    canvas.setFillColorRGB(0, 0, 0)
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(content_left_margin, 780, "Cliente:")
    canvas.setFont('Helvetica', 10)
    canvas.drawString(content_left_margin + 40, 780, client_name)
    
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(right_margin_position, 780, "Data de confecção:")
    canvas.setFont('Helvetica', 10)
    canvas.drawString(right_margin_position + date_confection_width + 4, 780, report_date)
    canvas.restoreState()

def generate_report_pdf(data, client_name, report_date):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Centered', alignment=TA_CENTER, fontSize=12, spaceAfter=20))
    styles.add(ParagraphStyle(name='Justify', alignment=TA_LEFT, fontSize=10, leading=12, spaceAfter=12))
    styles.add(ParagraphStyle(name='HeadingGray', fontSize=12, leading=14, backColor=colors.grey, textColor=colors.white, spaceAfter=12, spaceBefore=12, leftIndent=-4, rightIndent=330))
    styles.add(ParagraphStyle(name='HeadingRed', fontSize=12, leading=14, backColor=colors.red, textColor=colors.white, spaceAfter=12, spaceBefore=12, leftIndent=-4, rightIndent=330))
    styles.add(ParagraphStyle(name='LeftTitleBold', alignment=TA_LEFT, fontSize=12, spaceAfter=20, fontName='Helvetica-Bold'))

    content = []

    content.append(Paragraph("Análise", styles['LeftTitleBold']))

    for analysis in data['análise']:
        style = styles['HeadingGray'] if 'forte' not in analysis.get('mensagem', '') else styles['HeadingRed']
        if 'fenomeno' in analysis:
            content.append(Paragraph(f"&nbsp;{analysis['fenomeno'].capitalize()}", style))
        if 'data' in analysis and 'mensagem' in analysis:
            analysis_date = format_date(analysis['data'])
            content.append(Paragraph(f"<b>{analysis_date}:</b> {analysis['mensagem']}", styles['Justify']))
    
    content.append(PageBreak())
    content.append(Paragraph("Previsão", styles['LeftTitleBold']))

    grouped_forecasts = {}
    for forecast in data['previsao']:
        fenomeno = forecast['fenomeno']
        if fenomeno not in grouped_forecasts:
            grouped_forecasts[fenomeno] = []
        forecast_date = format_date(forecast['data'])
        grouped_forecasts[fenomeno].append(f"<b>{forecast_date}:</b> {forecast['mensagem']}")

    for fenomeno, forecasts in grouped_forecasts.items():
        style = styles['HeadingGray'] if 'forte' not in fenomeno else styles['HeadingRed']
        content.append(Paragraph(f"&nbsp;{fenomeno.capitalize()}", style))
        for forecast in forecasts:
            content.append(Paragraph(forecast, styles['Justify']))

    doc.build(content, onFirstPage=lambda canvas, doc: header(canvas, doc, client_name, report_date), onLaterPages=lambda canvas, doc: header(canvas, doc, client_name, report_date))
    buffer.seek(0)
    logging.info("PDF generated in memory")
    return buffer
