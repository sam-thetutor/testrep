#!/usr/bin/env python3
"""
Magnus Client Intake Form Generator
- Save drafts in Word format (.docx) for editing
- Generate final reports in PDF format

INSTALLATION REQUIRED:
pip install reportlab python-docx
"""

import os
import sys
import traceback

# Check for required packages
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import inch
except ImportError:
    print("ERROR: ReportLab is not installed. Please run: pip install reportlab")
    sys.exit(1)

try:
    from docx import Document
    from docx.shared import Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    print("ERROR: python-docx is not installed. Please run: pip install python-docx")
    sys.exit(1)

def save_draft_word(form_data, output_path):
    """Save form data as a Word document draft"""
    try:
        # Create document
        doc = Document()
        
        # Add title
        doc.add_heading('Magnus Client Intake Form', 0)
        doc.add_paragraph()
        
        # Personal Information
        doc.add_heading('Personal Information', level=1)
        doc.add_paragraph(f"Full Name: {form_data.get('full_name', '[Not provided]')}")
        doc.add_paragraph(f"Date of Birth: {form_data.get('dob', '[Not provided]')}")
        doc.add_paragraph(f"Social Security Number: {form_data.get('ssn', '[Not provided]')}")
        doc.add_paragraph(f"Citizenship: {form_data.get('citizenship', '[Not provided]')}")
        doc.add_paragraph(f"Marital Status: {form_data.get('marital_status', '[Not provided]')}")
        doc.add_paragraph()
        
        # Contact Information
        doc.add_heading('Contact Information', level=1)
        doc.add_paragraph(f"Residential Address: {form_data.get('residential_address', '[Not provided]')}")
        if form_data.get("mailing_address_different"):
            doc.add_paragraph(f"Mailing Address: {form_data.get('mailing_address', '[Not provided]')}")
        doc.add_paragraph(f"Email: {form_data.get('email', '[Not provided]')}")
        doc.add_paragraph(f"Home Phone: {form_data.get('home_phone', '[Not provided]')}")
        doc.add_paragraph(f"Mobile Phone: {form_data.get('mobile_phone', '[Not provided]')}")
        doc.add_paragraph(f"Work Phone: {form_data.get('work_phone', '[Not provided]')}")
        doc.add_paragraph()
        
        # Employment Information
        doc.add_heading('Employment Information', level=1)
        doc.add_paragraph(f"Employment Status: {form_data.get('employment_status', '[Not provided]')}")
        doc.add_paragraph(f"Employer Name: {form_data.get('employer_name', '[Not provided]')}")
        doc.add_paragraph(f"Occupation/Title: {form_data.get('occupation', '[Not provided]')}")
        doc.add_paragraph(f"Years Employed: {form_data.get('years_employed', '[Not provided]')}")
        doc.add_paragraph(f"Annual Income: {form_data.get('annual_income', '[Not provided]')}")
        doc.add_paragraph(f"Employer Address: {form_data.get('employer_address', '[Not provided]')}")
        
        # Retirement Information (if applicable)
        if form_data.get("employment_status") == "Retired":
            doc.add_paragraph()
            doc.add_heading('Retirement Information', level=1)
            doc.add_paragraph(f"Former Employer: {form_data.get('former_employer', '[Not provided]')}")
            doc.add_paragraph(f"Source of Income: {form_data.get('income_source', '[Not provided]')}")
        
        doc.add_paragraph()
        
        # Financial Information
        doc.add_heading('Financial Information', level=1)
        doc.add_paragraph(f"Education Status: {form_data.get('education_status', '[Not provided]')}")
        doc.add_paragraph(f"Estimated Tax Bracket: {form_data.get('tax_bracket', '[Not provided]')}")
        doc.add_paragraph(f"Investment Risk Tolerance: {form_data.get('risk_tolerance', '[Not provided]')}")
        doc.add_paragraph(f"Investment Objectives: {form_data.get('investment_objectives', '[Not provided]')}")
        doc.add_paragraph(f"Net Worth (excluding primary home): {form_data.get('net_worth', '[Not provided]')}")
        doc.add_paragraph(f"Liquid Net Worth: {form_data.get('liquid_net_worth', '[Not provided]')}")
        doc.add_paragraph(f"Assets Held Away: {form_data.get('assets_held_away', '[Not provided]')}")
        doc.add_paragraph()
        
        # Spouse Information (if applicable)
        if form_data.get("spouse_applicable", False):
            doc.add_heading('Spouse/Partner Information', level=1)
            doc.add_paragraph(f"Spouse Full Name: {form_data.get('spouse_full_name', '[Not provided]')}")
            doc.add_paragraph(f"Spouse Date of Birth: {form_data.get('spouse_dob', '[Not provided]')}")
            doc.add_paragraph(f"Spouse SSN: {form_data.get('spouse_ssn', '[Not provided]')}")
            doc.add_paragraph(f"Spouse Employment Status: {form_data.get('spouse_employment_status', '[Not provided]')}")
            doc.add_paragraph(f"Spouse Employer Name: {form_data.get('spouse_employer_name', '[Not provided]')}")
            doc.add_paragraph(f"Spouse Occupation/Title: {form_data.get('spouse_occupation', '[Not provided]')}")
            doc.add_paragraph()
        
        # Dependents Information
        doc.add_heading('Dependents Information', level=1)
        dependents = form_data.get("dependents", [])
        if dependents:
            for i, dep in enumerate(dependents):
                doc.add_paragraph(f"Dependent {i+1}:")
                doc.add_paragraph(f"  Name: {dep.get('name', '[Not provided]')}")
                doc.add_paragraph(f"  Date of Birth: {dep.get('dob', '[Not provided]')}")
                doc.add_paragraph(f"  Relationship: {dep.get('relationship', '[Not provided]')}")
        else:
            doc.add_paragraph("No dependents specified")
        doc.add_paragraph()
        
        # Beneficiaries Information
        doc.add_heading('Beneficiaries Information', level=1)
        beneficiaries = form_data.get("beneficiaries", [])
        if beneficiaries:
            for i, ben in enumerate(beneficiaries):
                doc.add_paragraph(f"Beneficiary {i+1}:")
                doc.add_paragraph(f"  Name: {ben.get('name', '[Not provided]')}")
                doc.add_paragraph(f"  Date of Birth: {ben.get('dob', '[Not provided]')}")
                doc.add_paragraph(f"  Relationship: {ben.get('relationship', '[Not provided]')}")
                percentage = ben.get('percentage', '')
                doc.add_paragraph(f"  Percentage: {percentage}%" if percentage else "  Percentage: [Not provided]")
        else:
            doc.add_paragraph("No beneficiaries specified")
        doc.add_paragraph()
        
        # Asset Breakdown
        doc.add_heading('Asset Breakdown', level=1)
        asset_types = ["Stocks", "Bonds", "Mutual Funds", "ETFs", "Options", "Futures", "Short-Term", "Other"]
        for asset_type in asset_types:
            field_name = f"asset_breakdown_{asset_type.lower().replace(' ', '_')}"
            value = form_data.get(field_name)
            doc.add_paragraph(f"{asset_type}: {value}%" if value else f"{asset_type}: [Not provided]")
        doc.add_paragraph()
        
        # Investment Experience
        doc.add_heading('Investment Experience', level=1)
        experience_types = ["Stocks", "Bonds", "Mutual Funds", "ETFs", "Options", "Futures"]
        for exp_type in experience_types:
            year_field = f"asset_experience_{exp_type.lower().replace(' ', '_')}_year"
            level_field = f"asset_experience_{exp_type.lower().replace(' ', '_')}_level"
            
            year = form_data.get(year_field)
            level = form_data.get(level_field)
            
            doc.add_paragraph(f"{exp_type}:")
            doc.add_paragraph(f"  Year Started: {year if year else '[Not provided]'}")
            doc.add_paragraph(f"  Experience Level: {level if level else '[Not provided]'}")
            doc.add_paragraph()
        
        # Outside Broker Information
        if form_data.get("has_outside_broker", False):
            doc.add_heading('Outside Broker Information', level=1)
            doc.add_paragraph(f"Broker Firm Name: {form_data.get('outside_broker_name', '[Not provided]')}")
            doc.add_paragraph(f"Account Number: {form_data.get('outside_broker_account', '[Not provided]')}")
            doc.add_paragraph(f"Account Type: {form_data.get('outside_broker_account_type', '[Not provided]')}")
            doc.add_paragraph()
        
        # Trusted Contact Information
        doc.add_heading('Trusted Contact Information', level=1)
        doc.add_paragraph(f"Full Name: {form_data.get('trusted_full_name', '[Not provided]')}")
        doc.add_paragraph(f"Relationship: {form_data.get('trusted_relationship', '[Not provided]')}")
        doc.add_paragraph(f"Phone Number: {form_data.get('trusted_phone', '[Not provided]')}")
        doc.add_paragraph(f"Email Address: {form_data.get('trusted_email', '[Not provided]')}")
        doc.add_paragraph()
        
        # Regulatory Consent
        doc.add_heading('Regulatory Consent', level=1)
        electronic_consent = "Yes" if form_data.get("electronic_regulatory_yes", False) else "No"
        doc.add_paragraph(f"Electronic Delivery Consent: {electronic_consent}")
        
        # Save document
        doc.save(output_path)
        return True
        
    except Exception as e:
        print(f"Error saving Word document: {str(e)}")
        traceback.print_exc()
        return False

def generate_pdf_report(form_data, output_path):
    """Generate PDF report from form data"""
    try:
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Create styles
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Build content
        content = []
        
        # Title
        content.append(Paragraph("Magnus Client Intake Form", title_style))
        content.append(Spacer(1, 12))
        
        # Personal Information
        content.append(Paragraph("Personal Information", subtitle_style))
        content.append(Spacer(1, 6))
        
        personal_info = [
            ("Full Name", form_data.get("full_name", "[Not provided]")),
            ("Date of Birth", form_data.get("dob", "[Not provided]")),
            ("Social Security Number", form_data.get("ssn", "[Not provided]")),
            ("Citizenship", form_data.get("citizenship", "[Not provided]")),
            ("Marital Status", form_data.get("marital_status", "[Not provided]"))
        ]
        
        for label, value in personal_info:
            content.append(Paragraph(f"{label}: {value}", normal_style))
        
        content.append(Spacer(1, 12))
        
        # Contact Information
        content.append(Paragraph("Contact Information", subtitle_style))
        content.append(Spacer(1, 6))
        
        contact_info = [
            ("Residential Address", form_data.get("residential_address", "[Not provided]")),
            ("Email", form_data.get("email", "[Not provided]")),
            ("Home Phone", form_data.get("home_phone", "[Not provided]")),
            ("Mobile Phone", form_data.get("mobile_phone", "[Not provided]")),
            ("Work Phone", form_data.get("work_phone", "[Not provided]"))
        ]
        
        for label, value in contact_info:
            content.append(Paragraph(f"{label}: {value}", normal_style))
        
        content.append(Spacer(1, 12))
        
        # Employment Information
        content.append(Paragraph("Employment Information", subtitle_style))
        content.append(Spacer(1, 6))
        
        employment_info = [
            ("Employment Status", form_data.get("employment_status", "[Not provided]")),
            ("Employer Name", form_data.get("employer_name", "[Not provided]")),
            ("Occupation", form_data.get("occupation", "[Not provided]")),
            ("Years Employed", form_data.get("years_employed", "[Not provided]")),
            ("Annual Income", form_data.get("annual_income", "[Not provided]")),
            ("Employer Address", form_data.get("employer_address", "[Not provided]"))
        ]
        
        for label, value in employment_info:
            content.append(Paragraph(f"{label}: {value}", normal_style))
        
        # Retirement Information
        if form_data.get("employment_status") == "Retired":
            content.append(Spacer(1, 12))
            content.append(Paragraph("Retirement Information", subtitle_style))
            content.append(Spacer(1, 6))
            
            retirement_info = [
                ("Former Employer", form_data.get("former_employer", "[Not provided]")),
                ("Source of Income", form_data.get("income_source", "[Not provided]"))
            ]
            
            for label, value in retirement_info:
                content.append(Paragraph(f"{label}: {value}", normal_style))
        
        content.append(Spacer(1, 12))
        
        # Financial Information
        content.append(Paragraph("Financial Information", subtitle_style))
        content.append(Spacer(1, 6))
        
        financial_info = [
            ("Education Status", form_data.get("education_status", "[Not provided]")),
            ("Estimated Tax Bracket", form_data.get("tax_bracket", "[Not provided]")),
            ("Investment Risk Tolerance", form_data.get("risk_tolerance", "[Not provided]")),
            ("Investment Objectives", form_data.get("investment_objectives", "[Not provided]")),
            ("Net Worth (excluding primary home)", form_data.get("net_worth", "[Not provided]")),
            ("Liquid Net Worth", form_data.get("liquid_net_worth", "[Not provided]")),
            ("Assets Held Away", form_data.get("assets_held_away", "[Not provided]"))
        ]
        
        for label, value in financial_info:
            content.append(Paragraph(f"{label}: {value}", normal_style))
        
        content.append(Spacer(1, 12))
        
        # Spouse Information
        if form_data.get("spouse_applicable"):
            content.append(Paragraph("Spouse Information", subtitle_style))
            content.append(Spacer(1, 6))
            
            spouse_info = [
                ("Spouse Full Name", form_data.get("spouse_full_name", "[Not provided]")),
                ("Spouse Date of Birth", form_data.get("spouse_dob", "[Not provided]")),
                ("Spouse SSN", form_data.get("spouse_ssn", "[Not provided]")),
                ("Spouse Employment Status", form_data.get("spouse_employment_status", "[Not provided]")),
                ("Spouse Employer Name", form_data.get("spouse_employer_name", "[Not provided]")),
                ("Spouse Occupation/Title", form_data.get("spouse_occupation", "[Not provided]"))
            ]
            
            for label, value in spouse_info:
                content.append(Paragraph(f"{label}: {value}", normal_style))
            
            content.append(Spacer(1, 12))
        
        # Dependents
        content.append(Paragraph("Dependents", subtitle_style))
        content.append(Spacer(1, 6))
        
        dependents = form_data.get("dependents", [])
        if dependents:
            for i, dep in enumerate(dependents):
                content.append(Paragraph(f"Dependent {i+1}:", normal_style))
                content.append(Paragraph(f"  Name: {dep.get('name', '[Not provided]')}", normal_style))
                content.append(Paragraph(f"  Date of Birth: {dep.get('dob', '[Not provided]')}", normal_style))
                content.append(Paragraph(f"  Relationship: {dep.get('relationship', '[Not provided]')}", normal_style))
        else:
            content.append(Paragraph("[No dependents specified]", normal_style))
        
        content.append(Spacer(1, 12))
        
        # Beneficiaries
        content.append(Paragraph("Beneficiaries", subtitle_style))
        content.append(Spacer(1, 6))
        
        beneficiaries = form_data.get("beneficiaries", [])
        if beneficiaries:
            for i, ben in enumerate(beneficiaries):
                content.append(Paragraph(f"Beneficiary {i+1}:", normal_style))
                content.append(Paragraph(f"  Name: {ben.get('name', '[Not provided]')}", normal_style))
                content.append(Paragraph(f"  Date of Birth: {ben.get('dob', '[Not provided]')}", normal_style))
                content.append(Paragraph(f"  Relationship: {ben.get('relationship', '[Not provided]')}", normal_style))
                percentage = ben.get('percentage', '')
                content.append(Paragraph(f"  Percentage: {percentage}%" if percentage else "  Percentage: [Not provided]", normal_style))
        else:
            content.append(Paragraph("[No beneficiaries specified]", normal_style))
        
        content.append(Spacer(1, 12))
        
        # Asset Breakdown
        content.append(Paragraph("Asset Breakdown", subtitle_style))
        content.append(Spacer(1, 6))
        
        asset_types = ["Stocks", "Bonds", "Mutual Funds", "ETFs", "Options", "Futures", "Short-Term", "Other"]
        for asset_type in asset_types:
            field_name = f"asset_breakdown_{asset_type.lower().replace(' ', '_')}"
            value = form_data.get(field_name)
            content.append(Paragraph(f"{asset_type}: {value}%" if value else f"{asset_type}: [Not provided]", normal_style))
        
        content.append(Spacer(1, 12))
        
        # Investment Experience
        content.append(Paragraph("Investment Experience", subtitle_style))
        content.append(Spacer(1, 6))
        
        experience_types = ["Stocks", "Bonds", "Mutual Funds", "ETFs", "Options", "Futures"]
        for exp_type in experience_types:
            year_field = f"asset_experience_{exp_type.lower().replace(' ', '_')}_year"
            level_field = f"asset_experience_{exp_type.lower().replace(' ', '_')}_level"
            
            year = form_data.get(year_field)
            level = form_data.get(level_field)
            
            content.append(Paragraph(f"{exp_type}:", normal_style))
            content.append(Paragraph(f"  Year Started: {year if year else '[Not provided]'}", normal_style))
            content.append(Paragraph(f"  Experience Level: {level if level else '[Not provided]'}", normal_style))
        
        content.append(Spacer(1, 12))
        
        # Outside Broker Information
        if form_data.get("has_outside_broker"):
            content.append(Paragraph("Outside Broker Information", subtitle_style))
            content.append(Spacer(1, 6))
            
            broker_info = [
                ("Broker Firm Name", form_data.get("outside_broker_name", "[Not provided]")),
                ("Account Number", form_data.get("outside_broker_account", "[Not provided]")),
                ("Account Type", form_data.get("outside_broker_account_type", "[Not provided]"))
            ]
            
            for label, value in broker_info:
                content.append(Paragraph(f"{label}: {value}", normal_style))
            
            content.append(Spacer(1, 12))
        
        # Trusted Contact Information
        content.append(Paragraph("Trusted Contact Information", subtitle_style))
        content.append(Spacer(1, 6))
        
        trusted_info = [
            ("Full Name", form_data.get("trusted_full_name", "[Not provided]")),
            ("Relationship", form_data.get("trusted_relationship", "[Not provided]")),
            ("Phone Number", form_data.get("trusted_phone", "[Not provided]")),
            ("Email Address", form_data.get("trusted_email", "[Not provided]"))
        ]
        
        for label, value in trusted_info:
            content.append(Paragraph(f"{label}: {value}", normal_style))
        
        content.append(Spacer(1, 12))
        
        # Regulatory Consent
        content.append(Paragraph("Regulatory Consent", subtitle_style))
        content.append(Spacer(1, 6))
        
        electronic_consent = "Yes" if form_data.get("electronic_regulatory_yes", False) else "No"
        content.append(Paragraph(f"Electronic Delivery Consent: {electronic_consent}", normal_style))
        
        # Build the PDF
        doc.build(content)
        return True
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        traceback.print_exc()
        return False

# Alias for backward compatibility with main_enhanced.py
generate_pdf_from_data = generate_pdf_report