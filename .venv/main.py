import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Frame
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from datetime import datetime

# Function to load JSON data with debugging
def load_data_from_json(file_name):
    try:
        print(f"Trying to load JSON from: {file_name}")
        with open(file_name, 'r') as f:
            content = f.read()
            print("JSON file content:\n", content)
            data = json.loads(content)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

# Function to create a pie chart based on JSON data
def create_pie_chart(data):
    # Prepare the data for the pie chart
    labels = [record['Agent'] for record in data]
    values = [float(record['Count percentages'].strip('%')) for record in data]

    # Create a drawing object
    drawing = Drawing(400, 200)

    # Create the Pie chart object
    pie = Pie()
    pie.x = 150  # X position of the pie chart
    pie.y = 50   # Y position of the pie chart
    pie.width = 150
    pie.height = 150

    pie.data = values
    pie.labels = labels

    # Style the pie chart
    pie.slices.strokeWidth = 0.5
    pie.slices.strokeColor = colors.black
    pie.slices[0].fillColor = colors.blue
    pie.slices[1].fillColor = colors.green
    pie.slices[2].fillColor = colors.red
    pie.slices[3].fillColor = colors.purple
    pie.slices[4].fillColor = colors.orange
    pie.slices[5].fillColor = colors.pink
    pie.slices[6].fillColor = colors.yellow

    # Add the pie chart to the drawing
    drawing.add(pie)
    
    return drawing

# Function to generate the PDF report
def generate_pdf_report(json_file, header_image, footer_image, output_pdf, username, rows):
    # Load data from JSON file
    data = load_data_from_json(json_file)
    
    if data is None:
        print("Failed to load JSON data. PDF generation aborted.")
        return
    
    # Limit data to the specified number of rows
    data = data[:rows]
    
    # Create the PDF document
    pdf = SimpleDocTemplate(output_pdf, pagesize=letter)
    content = []

    # Metadata section (Username, Report Generation Time, Date)
    metadata_data = [
        ['Username', 'Report Generation Time', 'Report Generation Date'],
        [username, datetime.now().strftime('%H:%M:%S'), datetime.now().strftime('%Y-%m-%d')]
    ]
    
    metadata_table = Table(metadata_data)
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
    content.append(Spacer(1, 20))  # Space before the main table

    # Prepare table data from JSON
    table_data = [['Agent', 'Count', 'Count percentages']]
    
    for record in data:
        row = [
            record.get('Agent', 'N/A'),
            record.get('Count', 'N/A'),
            record.get('Count percentages', 'N/A')
        ]
        table_data.append(row)

    # Create a table for main data
    main_table = Table(table_data)
    main_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    content.append(main_table)
    content.append(Spacer(1, 20))  # Space before the pie chart

    # Create and add pie chart to the PDF content
    pie_chart = create_pie_chart(data)
    content.append(pie_chart)

    content.append(Spacer(1, 20))  # Space before the footer

    # Create a frame to fix header and footer positions
    frame = Frame(0.75 * inch, 1.75 * inch, 7 * inch, 8.5 * inch, showBoundary=0)
    
    # Build the PDF
    pdf.build(content, 
              onFirstPage=lambda canvas, doc: draw_header_footer(canvas, doc, header_image, footer_image), 
              onLaterPages=lambda canvas, doc: draw_header_footer(canvas, doc, header_image, footer_image))

# Function to draw header and footer on each page
def draw_header_footer(canvas, doc, header_image, footer_image):
    # Draw header at the top of the page
    canvas.drawImage(header_image, 0.1 * inch, 9.5 * inch, width=7.5 * inch, height=1.0 * inch)
    
    # Draw footer at the bottom of the page
    canvas.drawImage(footer_image, 0.5 * inch, 0.5 * inch, width=7.5 * inch, height=1.0 * inch)

# Directory paths and files
base_dir = r"C:\Users\S Shivamshi\Desktop\WebDevRepos\xiotz_report\.venv"

# File paths
json_file = os.path.join(base_dir, 'data.json')
header_image = os.path.join(base_dir, 'header.png')
footer_image = os.path.join(base_dir, 'footer.png')

# Ask the user if they want to generate the PDF
user_input = input("Do you want to generate the PDF report? (yes/YES to confirm): ")

# Check user input
if user_input.lower() == 'yes':
    # Ask for the username
    username = input("Enter your username: ")
    rows = int(input("Enter the number of rows (up to 10): "))
    
    # Create a subdirectory for storing the PDF report
    output_folder = os.path.join(base_dir, 'pdf_reports')
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    
    # Define output PDF path
    output_pdf = os.path.join(output_folder, 'report.pdf')

    # Generate the PDF report
    generate_pdf_report(json_file, header_image, footer_image, output_pdf, username, rows)
    
    print(f"PDF report generated and saved in: {output_pdf}")
else:
    print("PDF generation cancelled.")
