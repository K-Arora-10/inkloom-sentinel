import fitz
import docx
from pathlib import Path

TEST_DIR = Path(__file__).parent / "fixtures"
TEST_DIR.mkdir(parents=True, exist_ok=True)

def generate_fixtures():
    # 1. Generate Scenario B PDF
    pdf_path = TEST_DIR / "scenario_b_brochure.pdf"
    doc = fitz.open()
    page = doc.new_page()
    content = (
        "NexaPay Enterprise Payment Brochure v2\n\n"
        "Welcome to NexaPay merchant solutions.\n"
        "Historical notice: Standard transaction fee was previously INR 499 (superseded).\n"
        "Under our revised pricing schedule, the active transaction fee is INR 399.\n"
        "NexaPay is India's safest payment platform for high volume checkout.\n"
    )
    page.insert_text((50, 72), content, fontsize=12)
    doc.save(str(pdf_path))
    doc.close()

    # 2. Generate DOCX fixture
    docx_path = TEST_DIR / "sample_policy.docx"
    doc_file = docx.Document()
    doc_file.add_heading("NexaPay Internal Communication Draft", 0)
    doc_file.add_paragraph("Hey folks!!! Our deal is absolutely insane.")
    doc_file.add_paragraph("NexaPay is 100% secure and guarantees the best payment experience in India.")
    doc_file.save(str(docx_path))

    return str(pdf_path), str(docx_path)

if __name__ == "__main__":
    generate_fixtures()
