import io
import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pathlib import Path

def create_text_watermark(text: str):
    """Generates a PDF layer in memory containing the watermark text."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Logic: Set font, transparency (alpha), and rotation
    can.setFont("Helvetica-Bold", 40)
    can.setFillGray(0.5, 0.4)  # 0.5 is gray level, 0.3 is opacity
    
    # Move the origin to the center for rotation
    can.saveState()
    can.translate(300, 400)
    can.rotate(45)
    can.drawCentredString(0, 0, text)
    can.restoreState()
    
    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def apply_watermark(input_path, output_path, watermark_text):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    watermark_page = create_text_watermark(watermark_text)

    for page in reader.pages:
        # Merge the generated text layer onto the existing page
        page.merge_page(watermark_page)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

# Execution
if __name__ == "__main__":
    # Logic: Dynamically locate the Downloads folder on Windows 11
    downloads_dir = Path(os.environ["USERPROFILE"]) / "Downloads"
    
    # DEFINE YOUR FILENAMES HERE
    filename = "sample_input_file.pdf" 
    target_text = "for screening purposes only"
    
    input_pdf = downloads_dir / filename
    output_pdf = downloads_dir / f"sample_output_file_with_watermark.pdf"

    if input_pdf.exists():
        apply_watermark(str(input_pdf), str(output_pdf), target_text)
        print(f"Success! Saved to: {output_pdf}")
    else:
        print(f"Error: Could not find {input_pdf}")