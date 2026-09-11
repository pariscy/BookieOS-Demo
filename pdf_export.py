from io import BytesIO
from pathlib import Path
import html

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

YELLOW = colors.HexColor('#F1C400')
GREEN = colors.HexColor('#44883E')
DARK = colors.HexColor('#212322')


def _font_paths():
    candidates = [
        ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
        ('/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf', '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf'),
    ]
    for regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            return regular, bold
    raise RuntimeError('Unicode font not found on server')


def _register_fonts():
    if 'BIONRegular' not in pdfmetrics.getRegisteredFontNames():
        regular, bold = _font_paths()
        pdfmetrics.registerFont(TTFont('BIONRegular', regular))
        pdfmetrics.registerFont(TTFont('BIONBold', bold))


def _clean_line(line: str) -> str:
    line = line.strip()
    for prefix in ('### ', '## ', '# ', '- ', '* '):
        if line.startswith(prefix):
            line = line[len(prefix):]
            break
    line = line.replace('**', '').replace('__', '').replace('`', '')
    return html.escape(line)


def generate_report_pdf(title: str, report: str) -> bytes:
    _register_fonts()
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16*mm,
        leftMargin=16*mm,
        topMargin=16*mm,
        bottomMargin=16*mm,
        title=title,
        author='BION — BookieCo Intelligence Operations Network',
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('BIONTitle', parent=styles['Title'], fontName='BIONBold', fontSize=20, leading=24, textColor=DARK, alignment=TA_CENTER, spaceAfter=4*mm)
    brand_style = ParagraphStyle('Brand', parent=styles['Normal'], fontName='BIONBold', fontSize=9, leading=11, textColor=GREEN, alignment=TA_CENTER, spaceAfter=5*mm)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='BIONBold', fontSize=14, leading=18, textColor=DARK, spaceBefore=4*mm, spaceAfter=2*mm)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='BIONBold', fontSize=11.5, leading=15, textColor=GREEN, spaceBefore=3*mm, spaceAfter=1.5*mm)
    body = ParagraphStyle('Body', parent=styles['BodyText'], fontName='BIONRegular', fontSize=9.5, leading=13.5, textColor=DARK, spaceAfter=1.8*mm)
    bullet = ParagraphStyle('Bullet', parent=body, leftIndent=5*mm, firstLineIndent=-3*mm)

    story = [
        Paragraph('BookieCo', title_style),
        Paragraph('BION · BookieCo Intelligence Operations Network', brand_style),
        HRFlowable(width='100%', thickness=2, color=YELLOW, spaceBefore=0, spaceAfter=5*mm),
        Paragraph(html.escape(title), h1),
        Spacer(1, 2*mm),
    ]

    for raw in report.splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 1.5*mm))
            continue
        if line == '---':
            story.append(HRFlowable(width='100%', thickness=.8, color=GREEN, spaceBefore=2*mm, spaceAfter=2*mm))
        elif line.startswith('# '):
            story.append(Paragraph(_clean_line(line), h1))
        elif line.startswith('## ') or line.startswith('### '):
            story.append(Paragraph(_clean_line(line), h2))
        elif line.startswith('- ') or line.startswith('* '):
            story.append(Paragraph('• ' + _clean_line(line), bullet))
        else:
            story.append(Paragraph(_clean_line(line), body))

    doc.build(story)
    return buffer.getvalue()
