"""
report_generator.py - PDF report generation using ReportLab.

Generates a comprehensive PDF report including:
  - Total employees
  - Burnout statistics
  - Attrition statistics
  - Model performance metrics
  - High-risk employee summary
  - Key insights
"""

import os
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from sqlalchemy.orm import Session
from app.models import EmployeeData, Prediction
from app.ml_model import load_training_metrics


def generate_pdf_report(db: Session) -> io.BytesIO:
    """
    Generate a comprehensive PDF report of the employee burnout analysis.

    Args:
        db: SQLAlchemy session

    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=50, leftMargin=50,
        topMargin=50, bottomMargin=50
    )

    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=20,
        textColor=colors.HexColor("#1a237e"),
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor("#283593"),
    )
    body_style = styles["Normal"]

    # ── Title ──────────────────────────────────────────────
    elements.append(Paragraph(
        "AI-Based Employee Burnout & Attrition Detection Report", title_style
    ))
    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", body_style
    ))
    elements.append(Spacer(1, 20))

    # ── Total Employees ────────────────────────────────────
    total_employees = db.query(EmployeeData).count()
    total_predictions = db.query(Prediction).count()

    elements.append(Paragraph("1. Overview", heading_style))
    overview_data = [
        ["Metric", "Value"],
        ["Total Employees in Database", str(total_employees)],
        ["Total Predictions Made", str(total_predictions)],
    ]
    overview_table = Table(overview_data, colWidths=[3 * inch, 2 * inch])
    overview_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a237e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
    ]))
    elements.append(overview_table)
    elements.append(Spacer(1, 15))

    # ── Burnout Statistics ─────────────────────────────────
    elements.append(Paragraph("2. Burnout Statistics", heading_style))
    employees = db.query(EmployeeData).all()
    if employees:
        burnout_counts = {"Low": 0, "Medium": 0, "High": 0}
        for emp in employees:
            if emp.burnout_level in burnout_counts:
                burnout_counts[emp.burnout_level] += 1

        burnout_data = [["Burnout Level", "Count", "Percentage"]]
        for level, count in burnout_counts.items():
            pct = round(count / total_employees * 100, 1) if total_employees > 0 else 0
            burnout_data.append([level, str(count), f"{pct}%"])

        burnout_table = Table(burnout_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
        burnout_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#c62828")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ]))
        elements.append(burnout_table)
    else:
        elements.append(Paragraph("No employee data available.", body_style))
    elements.append(Spacer(1, 15))

    # ── Attrition Statistics ───────────────────────────────
    elements.append(Paragraph("3. Attrition Statistics", heading_style))
    if employees:
        attrition_counts = {"Stay": 0, "Leave": 0}
        for emp in employees:
            if emp.attrition_status in attrition_counts:
                attrition_counts[emp.attrition_status] += 1

        attrition_data = [["Attrition Status", "Count", "Percentage"]]
        for status, count in attrition_counts.items():
            pct = round(count / total_employees * 100, 1) if total_employees > 0 else 0
            attrition_data.append([status, str(count), f"{pct}%"])

        attrition_table = Table(attrition_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
        attrition_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565c0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ]))
        elements.append(attrition_table)
    else:
        elements.append(Paragraph("No employee data available.", body_style))
    elements.append(Spacer(1, 15))

    # ── Model Performance Metrics ──────────────────────────
    elements.append(Paragraph("4. Model Performance Metrics", heading_style))
    metrics = load_training_metrics()
    if metrics:
        for target_name, target_key in [("Burnout", "burnout_model"), ("Attrition", "attrition_model")]:
            if target_key in metrics:
                elements.append(Paragraph(f"{target_name} Model Comparison", ParagraphStyle(
                    "SubHeading", parent=body_style, fontSize=11,
                    spaceAfter=8, spaceBefore=8, fontName="Helvetica-Bold"
                )))
                model_data = [["Model", "Accuracy", "Precision", "Recall", "F1 Score"]]
                for model_name, model_key in [
                    ("Logistic Regression", "logistic_regression"),
                    ("Random Forest", "random_forest"),
                ]:
                    if model_key in metrics[target_key]:
                        m = metrics[target_key][model_key]
                        model_data.append([
                            model_name,
                            f"{m['accuracy']:.4f}",
                            f"{m['precision']:.4f}",
                            f"{m['recall']:.4f}",
                            f"{m['f1_score']:.4f}",
                        ])

                best = metrics[target_key].get("best_model", "N/A")
                model_data.append(["Best Model", best, "", "", ""])

                performance_table = Table(model_data, colWidths=[1.5 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch])
                performance_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e7d32")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e8f5e9")),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ]))
                elements.append(performance_table)
                elements.append(Spacer(1, 10))
    else:
        elements.append(Paragraph("Models have not been trained yet.", body_style))
    elements.append(Spacer(1, 15))

    # ── High-Risk Employee Summary ─────────────────────────
    elements.append(Paragraph("5. High-Risk Employee Summary", heading_style))
    predictions = db.query(Prediction).all()
    high_risk = [p for p in predictions if p.risk_level == "High Risk"]
    medium_risk = [p for p in predictions if p.risk_level == "Medium Risk"]
    low_risk = [p for p in predictions if p.risk_level == "Low Risk"]

    risk_data = [
        ["Risk Level", "Count"],
        ["High Risk", str(len(high_risk))],
        ["Medium Risk", str(len(medium_risk))],
        ["Low Risk", str(len(low_risk))],
        ["Total Predictions", str(len(predictions))],
    ]
    risk_table = Table(risk_data, colWidths=[3 * inch, 2 * inch])
    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e65100")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
    ]))
    elements.append(risk_table)
    elements.append(Spacer(1, 15))

    # ── Key Insights ───────────────────────────────────────
    elements.append(Paragraph("6. Key Insights", heading_style))
    insights = []
    if employees:
        high_burnout_count = sum(1 for e in employees if e.burnout_level == "High")
        high_burnout_pct = round(high_burnout_count / total_employees * 100, 1)
        insights.append(f"• {high_burnout_pct}% of employees show HIGH burnout levels.")

        leave_count = sum(1 for e in employees if e.attrition_status == "Leave")
        leave_pct = round(leave_count / total_employees * 100, 1)
        insights.append(f"• {leave_pct}% of employees are at risk of leaving (attrition).")

        avg_salary = sum(e.salary for e in employees) / total_employees
        insights.append(f"• Average employee salary: ${avg_salary:,.2f}")

        avg_hours = sum(e.working_hours for e in employees) / total_employees
        insights.append(f"• Average working hours: {avg_hours:.1f} hours/week")

        overtime_count = sum(1 for e in employees if e.overtime == "Yes")
        overtime_pct = round(overtime_count / total_employees * 100, 1)
        insights.append(f"• {overtime_pct}% of employees work overtime.")

    if high_risk:
        insights.append(f"• {len(high_risk)} prediction(s) flagged as HIGH RISK requiring immediate attention.")

    if metrics:
        for target_key, target_label in [("burnout_model", "Burnout"), ("attrition_model", "Attrition")]:
            if target_key in metrics and "best_model" in metrics[target_key]:
                best = metrics[target_key]["best_model"]
                insights.append(f"• Best {target_label} model: {best}")

    if not insights:
        insights.append("• No data available yet. Generate dataset and train models to see insights.")

    for insight in insights:
        elements.append(Paragraph(insight, body_style))
        elements.append(Spacer(1, 4))

    # ── Footer ─────────────────────────────────────────────
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        "Footer", parent=body_style, fontSize=8,
        textColor=colors.grey, alignment=1
    )
    elements.append(Paragraph(
        "AI-Based Employee Burnout & Attrition Detection System — Confidential Report",
        footer_style
    ))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
