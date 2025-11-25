import pandas as pd
from datetime import date, datetime
from pydantic import BaseModel
from fastapi import APIRouter, Response
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO

from utils.predict_util import predict_productivity
from utils.score_util import calculate_health_score
from utils.tips_util import generate_tips
from firebase_config import save_user_log

router = APIRouter()

class FormData(BaseModel):
    focus_level: int
    mood_level: int
    overthinking_level: int
    stress_level: int
    procrastination_level: int
    sleep_hours: float
    sleep_quality: int
    nap_taken: int
    tasks_planned: int
    tasks_done: int
    distractions: int
    exercise_level: int
    hydration_liters: float
    junk_food_intake: int
    outside_food: int
    body_energy: int
    screen_time: float
    doom_scrolling_time: float
    productivity_yesterday: float 

class AnalyzeRequest(BaseModel):
    uid: str
    is_guest: bool
    form_data: FormData

@router.post("/submit-form/")
async def analyze(data:AnalyzeRequest):
    uid=data.uid
    is_guest=data.is_guest
    form_data=data.form_data
    
    if is_guest:
        ref_path = f'anonymous/{uid}/logs/{date.today().isoformat()}'
    else:
        ref_path = f'users/{uid}/logs/{date.today().isoformat()}'
    try:
        log_data=form_data.dict()
        form_df = pd.DataFrame([log_data])
        prediction= predict_productivity(form_df)
        health_score, raw_score, rating = calculate_health_score(form_df)
        tips = generate_tips(form_df)

        log_data["health_score"] = health_score
        log_data["productivity_score"] = float(prediction)
        log_data["rating"] = rating
        log_data["category_score"] = raw_score
        save_user_log(ref_path, log_data)

        return {"predicted_productivity": prediction, "health_score": health_score, "rating": rating, "tips":tips, "category_score": {k: float(v) for k, v in raw_score.items()}}
    
    except Exception as e:
        print("Error during prediction:", e)
        return {"error": str(e)}
    


@router.post("/pdf/form-summary")
def generate_form_summary_pdf(payload: dict):
    buffer = BytesIO()

    # ---------- COLOR SCHEME ----------
    BRAND_PRIMARY = colors.HexColor("#351c3e")     # Header bar
    ACCENT_PURPLE = colors.HexColor("#4A2A47")     # Section headers
    TEXT_DARK = colors.HexColor("#2A2A2A")         # Normal text
    CREAM = colors.HexColor("#FACAB3")             # Score cards background

    # ---------- PDF BASE ----------
    doc = SimpleDocTemplate(buffer, Margin= A4)
    elements = []

    # ---------- CUSTOM TEXT STYLES ----------
    title_style = ParagraphStyle(
        "title_style",
        fontSize=20,
        textColor=colors.white,
        leading=26,
        spaceAfter=10,
        alignment=1,
        fontName="Helvetica-Bold"
    )

    header_style = ParagraphStyle(
        "header_style",
        fontSize=12,
        textColor=colors.white,
        leading=14,
        alignment=1
    )

    section_header = ParagraphStyle(
        "section_header",
        fontSize=15,
        textColor=ACCENT_PURPLE,
        leading=20,
        fontName="Helvetica-Bold"
    )

    normal_text = ParagraphStyle(
        "normal_text",
        fontSize=11,
        textColor=TEXT_DARK,
        leading=15
    )

    # ---------- HEADER BLOCK ----------
    header_data = [
        [Paragraph("<b>PRODUXI</b>", title_style)],
        [Paragraph("Your Productivity and Health Summary", header_style)],
        [Paragraph(datetime.now().strftime("%d %B %Y, %I:%M %p"), header_style)]
    ]

    header_table = Table(header_data, colWidths=[450])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_PRIMARY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOX", (0, 0), (-1, -1), 0.1, BRAND_PRIMARY)
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 20))

    print("Category Score Structure:", repr(payload.get("category_score", None)))
    print(type(payload.get("category_score", None)))

    # ---------- INPUTS SECTION ----------
    elements.append(Paragraph("Your Responses", section_header))
    elements.append(Spacer(1, 8))

    form_inputs = payload.get("form_inputs", {})

    for key, value in form_inputs.items():
        formatted_key = key.replace("_", " ").title()
        elements.append(Paragraph(f"<b>{formatted_key}:</b> {value}", normal_text))
        elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 20))

    # ---------- SCORES SECTION ----------
    elements.append(Paragraph("Scores", section_header))

    health_score = payload.get("health_score", 0)
    productivity_score = payload.get("productivity_score", 0)
    rating = payload.get("rating", "")

    def score_card(label, value):
        return Table(
            [[Paragraph(f"<b>{label}:</b> {value}", ParagraphStyle("card", fontSize=13, textColor=CREAM, alignment=1))]],
            colWidths=[460],
            style=[
                ("BACKGROUND", (0, 0), (-1, -1), ACCENT_PURPLE),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )

    # Main Score Cards
    elements.append(score_card("Health Score", f"{health_score} {rating}"))
    elements.append(Spacer(1, 12))
    elements.append(score_card("Predicted Productivity Score", productivity_score))
    elements.append(Spacer(1, 20))  

    # ---------- CATEGORY SCORES ----------
    elements.append(Paragraph("Category-wise Health Score Breakdown (in %)", section_header))
    elements.append(Spacer(1, 10))

    category_scores = payload.get("category_score", {})

    if isinstance(category_scores, dict) and category_scores:

        for cat, val in category_scores.items():

            label = cat.replace("_", " ").title()
            val = round(float(val), 2)

            table = Table(
                [[
                    Paragraph(f"<b>{label}:</b>", ParagraphStyle(
                        "cat_label",
                        fontSize=12,
                        textColor=CREAM
                    )),
                    Paragraph(f"{val}", ParagraphStyle(
                        "cat_value",
                        fontSize=12,
                        textColor=CREAM,
                        alignment=2    # right align value
                    ))
                ]],
                colWidths=[250, 210]
            )

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), ACCENT_PURPLE),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 10))

    else:
        elements.append(Paragraph("Category scores unavailable.", normal_text))

    elements.append(Spacer(1, 20))



    # ---------- POSITIVE/NEGATIVE TIPS ----------
    elements.append(Paragraph("Personalized Tips", section_header))
    elements.append(Spacer(1, 10))

    tips = payload.get("tips", [])
    parsed_tips = []

    if isinstance(tips, list):
        for obj in tips:
            parsed_tips.append(
                (obj.get("text", ""), obj.get("type", "neutral"))
            )

    if parsed_tips:
        for tip_text, tip_type in parsed_tips:
            tip_color = (
                colors.HexColor("#0b5f48") if tip_type == "positive"
                else colors.HexColor("#a50036")
            )

            tip_style = ParagraphStyle(
                "tip_style",
                fontSize=11,
                textColor=tip_color,
                leading=15
            )

            elements.append(Paragraph(f"• {tip_text}", tip_style))
            elements.append(Spacer(1, 4))
    else:
        elements.append(Paragraph("No tips available.", normal_text))

    # ---------- FOOTER ----------
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle("footer_style", fontSize=9, alignment=1, textColor=TEXT_DARK)
    elements.append(Paragraph("Generated by ProduXi", footer_style))

    # ----- BUILD PDF -----
    def draw_light_background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#F5F5F8"))  
        canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
        canvas.restoreState()

    doc.build(
        elements,
        onFirstPage=draw_light_background,
        onLaterPages=draw_light_background
    )

    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=ProduXi_Summary.pdf"}
    )
