import os
from pathlib import Path
from pypdf import PdfWriter

def merge_pdfs(input_paths, output_path):
    """
    Merges multiple PDF files into a single output file.
    
    Args:
        input_paths (list): List of Path objects to source PDFs.
        output_path (Path): Path object for the destination file.
    """
    writer = PdfWriter()

    for path in input_paths:
        if path.exists():
            print(f"Processing: {path.name}")
            writer.append(path)
        else:
            print(f"Error: File not found at {path}")

    # Write the entire buffer to the destination
    with open(output_path, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    # Logic: Dynamically locate the Downloads folder on Windows 11
    downloads_dir = Path(os.environ["USERPROFILE"]) / "Downloads"
    
    # CONFIGURATION: Define your source files in order
    files_to_merge = [
        "document_part_1.pdf",
        "document_part_2.pdf",
        "document_part_3.pdf"
    ]
    
    # Resolve full paths
    input_pdf_paths = [downloads_dir / f for f in files_to_merge]
    output_pdf_path = downloads_dir / "merged_output_final.pdf"

    try:
        if not files_to_merge:
            raise ValueError("The 'files_to_merge' list is empty.")
            
        merge_pdfs(input_pdf_paths, output_pdf_path)
        
        print("-" * 30)
        print(f"Success! Merged {len(files_to_merge)} files.")
        print(f"Final File: {output_pdf_path}")
        
    except Exception as e:
        print(f"Pipeline Failure: {e}")