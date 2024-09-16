import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, KeepInFrame, Paragraph
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Function to load JSON data
def load_data_from_json(file_name):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

# Function to create a pie chart based on data
def create_pie_chart(labels, values):
    drawing = Drawing(300, 150)  # Adjusted width and height for better visibility

    pie = Pie()
    pie.x = 65   # X position of the pie chart
    pie.y = 15   # Y position of the pie chart
    pie.width = 100
    pie.height = 100

    pie.data = values
    pie.labels = labels

    # Style the pie chart slices
    pie.slices.strokeWidth = 0.5
    pie.slices.strokeColor = colors.black
    pie.slices[0].fillColor = colors.blue
    pie.slices[1].fillColor = colors.green
    pie.slices[2].fillColor = colors.red
    pie.slices[3].fillColor = colors.purple
    pie.slices[4].fillColor = colors.orange

    drawing.add(pie)
    
    # Keep the pie chart within a frame to ensure it flows correctly
    return KeepInFrame(300, 150, [drawing])

# Function to create a bar chart based on data
def create_bar_chart(labels, values):
    drawing = Drawing(300, 200)
    
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 50
    bar.height = 125
    bar.width = 200
    bar.data = [values]
    bar.categoryAxis.categoryNames = labels
    
    bar.barWidth = 0.3 * inch
    bar.barSpacing = 0.2 * inch
    bar.valueAxis.valueMin = 0
    bar.valueAxis.valueMax = max(values) * 1.2
    bar.valueAxis.valueStep = max(values) // 5 or 1
    
    bar.bars[0].fillColor = colors.blue
    
    drawing.add(bar)
    
    return KeepInFrame(300, 200, [drawing])

# Function to generate the PDF report with improved styling
def generate_pdf_report(json_file, header_image, footer_image, output_pdf, username, rows):
    data = load_data_from_json(json_file)
    
    if data is None:
        return
    
    # Split the data into two sets for tables and pie charts
    agent_data = [record for record in data if 'Agent' in record]
    technique_data = [record for record in data if 'Technique' in record]
    
    # Limit data to specified number of rows for both tables
    agent_data = agent_data[:rows]
    technique_data = technique_data[:rows]
    
    # Create the PDF document
    pdf = SimpleDocTemplate(output_pdf, pagesize=letter)
    content = []
    
    # Set up styles for text wrapping in tables
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    # Metadata section
    metadata_data = [
        ['Username', 'Report Generation Time', 'Report Generation Date'],
        [username, datetime.now().strftime('%H:%M:%S'), datetime.now().strftime('%Y-%m-%d')]
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(metadata_table)
    content.append(Spacer(1, 20))

    # Table for Agent Data
    agent_table_data = [['Agent', 'Count', 'Count percentages']]
    for record in agent_data:
        agent_table_data.append([
            Paragraph(record['Agent'], normal_style), 
            Paragraph(str(record['Count']), normal_style), 
            Paragraph(record['Count percentages'], normal_style)
        ])

    agent_table = Table(agent_table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    agent_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(agent_table)
    content.append(Spacer(1, 20))

    # Pie chart for Agent Data
    agent_labels = [record['Agent'] for record in agent_data]
    agent_values = [float(record['Count percentages'].strip('%')) for record in agent_data]
    agent_pie_chart = create_pie_chart(agent_labels, agent_values)
    content.append(agent_pie_chart)
    content.append(Spacer(1, 20))

    # Bar chart for Agent Data
    agent_counts = [int(record['Count']) if isinstance(record['Count'], int) else int(record['Count'].replace(',', '')) for record in agent_data]
    agent_bar_chart = create_bar_chart(agent_labels, agent_counts)
    content.append(agent_bar_chart)
    content.append(Spacer(1, 20))

    # Table for Technique Data
    technique_table_data = [['Technique', 'Count', 'Count percentages']]
    for record in technique_data:
        technique_table_data.append([
            Paragraph(record['Technique'], normal_style), 
            Paragraph(str(record['Count']), normal_style), 
            Paragraph(record['Count percentages'], normal_style)
        ])

    technique_table = Table(technique_table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    technique_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(technique_table)
    content.append(Spacer(1, 20))

    # Pie chart for Technique Data
    technique_labels = [record['Technique'] for record in technique_data]
    technique_values = [float(record['Count percentages'].strip('%')) for record in technique_data]
    technique_pie_chart = create_pie_chart(technique_labels, technique_values)
    content.append(technique_pie_chart)
    content.append(Spacer(1, 20))

    # Bar chart for Technique Data
    technique_counts = [int(record['Count']) if isinstance(record['Count'], int) else int(record['Count'].replace(',', '')) for record in technique_data]
    technique_bar_chart = create_bar_chart(technique_labels, technique_counts)
    content.append(technique_bar_chart)

    # Build the PDF
    pdf.build(content, 
              onFirstPage=lambda canvas, doc: draw_header_footer(canvas, doc, header_image, footer_image), 
              onLaterPages=lambda canvas, doc: draw_header_footer(canvas, doc, header_image, footer_image))

# Function to draw header and footer on each page
def draw_header_footer(canvas, doc, header_image, footer_image):
    canvas.drawImage(header_image, 0.1 * inch, 9.5 * inch, width=7.5 * inch, height=1.0 * inch)
    canvas.drawImage(footer_image, 0.5 * inch, 0.5 * inch, width=7.5 * inch, height=1.0)


# Directory paths and files
base_dir = r"C:\Users\S Shivamshi\Desktop\WebDevRepos\xiotz_report\.venv"

# File paths
json_file = os.path.join(base_dir, 'data.json')
header_image = os.path.join(base_dir, 'header.png')
footer_image = os.path.join(base_dir, 'footer.png')

# Ask the user if they want to generate the PDF
user_input = input("Do you want to generate the PDF report? (yes/YES to confirm): ")


if user_input.lower() == 'yes':
    username = input("Enter your username: ")
    rows = int(input("Enter the number of rows (up to 10): "))
    
    output_folder = os.path.join(base_dir, 'pdf_reports')
    os.makedirs(output_folder, exist_ok=True)
    
    output_pdf = os.path.join(output_folder, 'report.pdf')

    generate_pdf_report(json_file, header_image, footer_image, output_pdf, username, rows)
    
    print(f"PDF report generated and saved in: {output_pdf}")
else:
    print("PDF generation cancelled.")
