import markdown2
from weasyprint import HTML
import os

def save_report_as_pdf(report_content, filename="Vulnerability_Report.pdf"):
    """
    Converts the given Markdown report to a formatted PDF and saves it in the working directory.
    
    :param report_content: Markdown text (string)
    :param filename: Name of the output PDF file (default: Vulnerability_Report.pdf)
    """
    if not report_content.strip():
        print("❌ Error: Empty report content. PDF not generated.")
        return

    # Convert Markdown to HTML
    html_content = markdown2.markdown(report_content)

    # Add CSS for styling
    styled_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
            }}
            h1, h2, h3 {{
                color: #333;
                font-weight: bold;
            }}
            h1 {{ font-size: 24px; }}
            h2 {{ font-size: 20px; }}
            h3 {{ font-size: 18px; }}
            code {{
                font-family: monospace;
                background: #f4f4f4;
                padding: 2px 4px;
                border-radius: 4px;
            }}
            pre {{
                background: #f4f4f4;
                padding: 10px;
                border-radius: 4px;
                overflow-x: auto;
            }}
            ul, ol {{
                margin-left: 20px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Save PDF in working directory
    output_path = os.path.join(os.getcwd(), filename)
    HTML(string=styled_html).write_pdf(output_path)

    print(f"✅ Report saved successfully as: {output_path}")

