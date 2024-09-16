import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime
import matplotlib.pyplot as plt

# Function to load JSON data
def load_data_from_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

# Function to create a pie chart using matplotlib
def create_pie_chart(data, output_image):
    # Extract labels and values
    labels = [record['Agent'] for record in data]
    values = [float(record['Count percentages'].strip('%')) for record in data]

    # Create a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

    # Equal aspect ratio ensures the pie is drawn as a circle.
    plt.axis('equal')

    # Save pie chart as an image file
    plt.savefig(output_image, format='png')
    plt.close()

# Function to generate the PDF report
def generate_pdf_report(json_file, header_image, footer_image, output_pdf, username, rows):
    # Load data from JSON file
    data = load_data_from_json(json_file)
    
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
    pie_chart_image = os.path.join(os.path.dirname(output_pdf), 'pie_chart.png')
    create_pie_chart(data, pie_chart_image)
    
    # Add the pie chart image to the PDF content
    pie_chart_img = Image(pie_chart_image, 7 * inch, 7 * inch)
    content.append(pie_chart_img)

    content.append(Spacer(1, 20))  # Space before the footer

    # Build the PDF
    pdf.build(content, 
              onFirstPage=lambda canvas, doc: draw_header_footer(canvas, header_image, footer_image), 
              onLaterPages=lambda canvas, doc: draw_header_footer(canvas, header_image, footer_image))

# Function to draw header and footer on each page
def draw_header_footer(canvas, header_image, footer_image):
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
    output_pdf = os.path.join(output_folder, 'report_with_piechart.pdf')

    # Generate the PDF report
    generate_pdf_report(json_file, header_image, footer_image, output_pdf, username, rows)
    
    print(f"PDF report generated and saved in: {output_pdf}")
else:
    print("PDF generation cancelled.")
