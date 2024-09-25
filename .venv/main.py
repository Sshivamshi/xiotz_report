import json
import os
import math
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.pyplot import pie
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, Image
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Polygon, String, Circle, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.widgets.grids import ShadedRect

# Blue color scheme
color_scheme = [
    colors.HexColor("#ADD8E6"),  # Light Blue
    colors.HexColor("#87CEEB"),  # Sky Blue
    colors.HexColor("#6495ED"),  # Cornflower Blue
    colors.HexColor("#1E90FF"),  # Dodger Blue
    colors.HexColor("#4169E1"),  # Royal Blue
    colors.HexColor("#0000CD"),  # Medium Blue
    colors.HexColor("#00008B"),  # Dark Blue
    colors.HexColor("#000080"),  # Navy Blue
    colors.HexColor("#6A5ACD"),  # Slate Blue
    colors.HexColor("#4682B4")   # Steel Blue
]

def reportlab_color_to_rgba(color):
    """Convert ReportLab color to RGBA tuple for matplotlib."""
    return (color.red, color.green, color.blue, color.alpha) if color.alpha else (color.red, color.green, color.blue, 1)

def load_data_from_json(file_name):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

def create_normal_pie_chart(labels, values):
    drawing = Drawing(400, 200)
    pie_chart = Pie()
    pie_chart.x = 150
    pie_chart.y = 50
    pie_chart.width = 125
    pie_chart.height = 125
    pie_chart.data = values
    pie_chart.labels = labels

    for i, value in enumerate(values):
        pie_chart.slices[i].fillColor = color_scheme[i % len(color_scheme)]

    drawing.add(pie_chart)
    return drawing

def create_pie_chart_with_legend(labels, values):
    drawing = Drawing(400, 200)
    pie_chart = Pie()
    pie_chart.x = 100
    pie_chart.y = 50
    pie_chart.width = 125
    pie_chart.height = 125
    pie_chart.data = values
    pie_chart.labels = ["" for _ in labels]  # No labels directly on the pie chart

    for i, value in enumerate(values):
        pie_chart.slices[i].fillColor = color_scheme[i % len(color_scheme)]

    drawing.add(pie_chart)

    legend_x = 250  # X position of the legend
    legend_y = 150  # Y position of the legend
    for i, label in enumerate(labels):
        color = color_scheme[i % len(color_scheme)]
        drawing.add(Rect(legend_x, legend_y, 10, 10, fillColor=color, strokeWidth=1))
        drawing.add(String(legend_x + 15, legend_y, label, fontSize=10))
        legend_y -= 15

    return drawing

def create_vertical_bar_chart(labels, values):
    drawing = Drawing(400, 200)
    bar_chart = VerticalBarChart()
    bar_chart.x = 50
    bar_chart.y = 50
    bar_chart.height = 125
    bar_chart.width = 300
    bar_chart.data = [values]
    bar_chart.categoryAxis.categoryNames = labels
    
    bar_chart.barWidth = 0.3 * inch
    bar_chart.barSpacing = 0.2 * inch
    bar_chart.valueAxis.valueMin = 0
    bar_chart.valueAxis.valueMax = max(values) * 1.2
    bar_chart.valueAxis.valueStep = max(values) // 5 or 1
    
    bar_chart.bars[0].fillColor = color_scheme[0]  # Default color scheme
    bar_chart.categoryAxis.labels.angle = 90
    
    drawing.add(bar_chart)
    return drawing

def create_horizontal_bar_chart(labels, values, color_scheme=[colors.blue]):
    drawing = Drawing(400, 300)
    bar_chart = HorizontalBarChart()
    bar_chart.x = 50
    bar_chart.y = 50
    bar_chart.height = 200
    bar_chart.width = 300
    bar_chart.data = [values]
    bar_chart.categoryAxis.categoryNames = labels
    
    bar_chart.barWidth = 0.4 * inch
    bar_chart.barSpacing = 0.2 * inch
    bar_chart.valueAxis.valueMin = 0
    bar_chart.valueAxis.valueMax = max(values) * 1.2
    bar_chart.valueAxis.valueStep = max(values) // 5 or 1

    bar_chart.bars[0].fillColor = color_scheme[0]  # Applying color scheme

    drawing.add(bar_chart)
    return drawing

def create_spider_chart(labels, values):
    num_vars = len(labels)
    max_value = max(values)
    angle = 2 * math.pi / num_vars

    drawing = Drawing(400, 400)

    center_x = 200
    center_y = 200
    radius = 150

    for i in range(1, 6):  # 5 layers of grids (20%, 40%, 60%, 80%, 100%)
        points = []
        for j in range(num_vars):
            x = center_x + (i * radius / 5) * math.cos(j * angle)
            y = center_y + (i * radius / 5) * math.sin(j * angle)
            points.append((x, y))
        flat_points = [coord for point in points for coord in point]  # Flatten the list of tuples
        drawing.add(Polygon(flat_points, strokeColor=colors.black, strokeWidth=0.5))

    value_points = []
    for i in range(num_vars):
        x = center_x + (values[i] / max_value * radius) * math.cos(i * angle)
        y = center_y + (values[i] / max_value * radius) * math.sin(i * angle)
        value_points.append((x, y))
        drawing.add(Circle(x, y, 5, fillColor=color_scheme[i % len(color_scheme)]))

    value_flat_points = [coord for point in value_points for coord in point]  # Flatten the value points
    drawing.add(Polygon(value_flat_points, strokeColor=color_scheme[0], fillColor=color_scheme[0], fillOpacity=0.3))

    for i, label in enumerate(labels):
        x = center_x + (radius + 20) * math.cos(i * angle)
        y = center_y + (radius + 20) * math.sin(i * angle)
        drawing.add(String(x, y, label, fontSize=10, fillColor=colors.black))

    return drawing

def create_3d_pie_chart(labels, values):
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(aspect="equal"))



    # Convert ReportLab colors to RGBA tuples for matplotlib
    colors_for_matplotlib = [reportlab_color_to_rgba(color_scheme[i % len(color_scheme)]) for i in range(len(values))]

    wedges, texts, autotexts = pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors_for_matplotlib,
        startangle=140,
        wedgeprops=dict(width=0.4, edgecolor='w')
    )
    
    for wedge in wedges:
        wedge.set_edgecolor('grey')

    ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.2, 1))

    plt.setp(autotexts, size=10, weight="bold")
    plt.title("3D Pie Chart")

    pie_chart_file = "3d_pie_chart.png"
    plt.savefig(pie_chart_file, bbox_inches='tight', dpi=300)
    plt.close(fig)

    return pie_chart_file

def draw_header_footer(canvas, doc, header_image, footer_image):
    width, height = letter
    if header_image:
        canvas.drawImage(header_image, 1 * inch, height - 1 * inch, width=6 * inch, height=1 * inch)
    if footer_image:
        canvas.drawImage(footer_image, 1 * inch, 0.5 * inch, width=6 * inch, height=1 * inch)

def generate_pdf_report(json_file, header_image, footer_image, output_pdf, username, rows):
    data = load_data_from_json(json_file)
    
    if data is None:
        return
    
    agent_data = [record for record in data if 'Agent' in record]
    technique_data = [record for record in data if 'Technique' in record]
    
    agent_data = agent_data[:rows]
    technique_data = technique_data[:rows]
    
    pdf = SimpleDocTemplate(output_pdf, pagesize=letter)
    content = []
    
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    # Metadata
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

    # Agent Data Table
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

    # Agent Charts
    agent_labels = [record['Agent'] for record in agent_data]
    agent_counts = [int(record['Count'].replace(',', '')) for record in agent_data]
    agent_percentages = [float(record['Count percentages'].replace('%', '')) for record in agent_data]

    content.append(Paragraph("Agent Data - Vertical Bar Chart", styles['Heading3']))
    content.append(create_vertical_bar_chart(agent_labels, agent_counts))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Agent Data - Horizontal Bar Chart (Blue)", styles['Heading3']))
    content.append(create_horizontal_bar_chart(agent_labels, agent_counts, color_scheme=[colors.blue]))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Agent Data - Normal Pie Chart", styles['Heading3']))
    content.append(create_normal_pie_chart(agent_labels, agent_percentages))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Agent Data - Pie Chart with Multi-Column Legend", styles['Heading3']))
    content.append(create_pie_chart_with_legend(agent_labels, agent_percentages))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Agent Data - Spider Chart", styles['Heading3']))
    content.append(create_spider_chart(agent_labels, agent_percentages))
    content.append(Spacer(1, 20))

    # Add 3D Pie Chart
    pie_chart_file = create_3d_pie_chart(agent_labels, agent_percentages)
    content.append(Paragraph("Agent Data - 3D Pie Chart", styles['Heading3']))
    content.append(Image(pie_chart_file, width=6*inch, height=4*inch))
    content.append(Spacer(1, 20))

    # Technique Data Table
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

    # Technique Charts
    technique_labels = [record['Technique'] for record in technique_data]
    technique_counts = [int(record['Count'].replace(',', '')) for record in technique_data]
    technique_percentages = [float(record['Count percentages'].replace('%', '')) for record in technique_data]

    content.append(Paragraph("Technique Data - Vertical Bar Chart", styles['Heading3']))
    content.append(create_vertical_bar_chart(technique_labels, technique_counts))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Technique Data - Horizontal Bar Chart (Blue)", styles['Heading3']))
    content.append(create_horizontal_bar_chart(technique_labels, technique_counts, color_scheme=[colors.blue]))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Technique Data - Normal Pie Chart", styles['Heading3']))
    content.append(create_normal_pie_chart(technique_labels, technique_percentages))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Technique Data - Pie Chart with Multi-Column Legend", styles['Heading3']))
    content.append(create_pie_chart_with_legend(technique_labels, technique_percentages))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Technique Data - Spider Chart", styles['Heading3']))
    content.append(create_spider_chart(technique_labels, technique_percentages))
    content.append(Spacer(1, 20))

    pie_chart_file = create_3d_pie_chart(agent_labels, agent_percentages)
    content.append(Paragraph("Agent Data - 3D Pie Chart", styles['Heading3']))
    content.append(Image(pie_chart_file, width=6*inch, height=4*inch))
    content.append(Spacer(1, 20))

    # Adding header and footer images
    if header_image:
        content.insert(0, Image(header_image, width=6*inch, height=1*inch))
    if footer_image:
        content.append(Spacer(1, 20))
        content.append(Image(footer_image, width=6*inch, height=1*inch))

    pdf.build(content, 
              onFirstPage=lambda canvas, doc: draw_header_footer(canvas, doc, header_image, footer_image), 
              onLaterPages=lambda canvas, doc: draw_header_footer(canvas, doc, header_image, footer_image))

    print(f"PDF report generated: {output_pdf}")

# Directory paths and files
base_dir = r"c:\Users\S Shivamshi\Desktop\WebDevRepos\xiotz_report\.venv"

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