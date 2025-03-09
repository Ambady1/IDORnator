import markdown2
import os

def save_report_as_html(report_content, filename="Vulnerability_Report.html"):

    if not report_content.strip():
        print("❌ Error: Empty report content. Report generation failed.")
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

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(styled_html)
        print(f"✅ Report saved successfully as: {output_path}")
    except Exception as e:
        print(f"❌ Error saving report: {e}")
