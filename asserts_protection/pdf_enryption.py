import os
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def add_password(input_path, output_path, password):
    """Clones a PDF and applies AES-256 encryption."""
    reader = PdfReader(input_path)
    # Using clone_from is the most efficient way to copy all pages/metadata
    writer = PdfWriter(clone_from=reader)
    
    # AES-256-R5 is the most secure modern standard supported by pypdf
    writer.encrypt(user_password=password, algorithm="AES-256-R5")

    with open(output_path, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    # Logic: Dynamically locate the Downloads folder on Windows 11
    downloads_dir = Path(os.environ["USERPROFILE"]) / "Downloads"
    
    # CONFIGURATION
    filename = "sample_input_file.pdf" 
    pdf_password = "your_password" 
    
    input_pdf = downloads_dir / filename
    output_pdf = downloads_dir / "sample_output_file_with_password.pdf"

    if input_pdf.exists():
        try:
            add_password(str(input_pdf), str(output_pdf), pdf_password)
            print(f"Success! Password protection applied.")
            print(f"Saved to: {output_pdf}")
        except Exception as e:
            print(f"Error during encryption: {e}")
    else:
        print(f"Error: Could not find {input_pdf}")