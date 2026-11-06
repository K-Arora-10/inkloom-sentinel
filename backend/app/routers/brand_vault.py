from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.models import (
    Document, DocumentVersion, BrandRule, GlossaryTerm, ApprovedFact, ClaimPassport, Asset, AuditLog
)
from backend.app.schemas.schemas import (
    DocumentRead, BrandRuleRead, GlossaryTermRead, ApprovedFactRead, ClaimPassportRead
)
from backend.app.services.extraction_service import extract_content
from backend.app.config import settings
import shutil
from pathlib import Path

router = APIRouter(prefix="/brand-vault", tags=["Brand Vault"])

@router.get("/documents", response_model=List[DocumentRead])
def get_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.created_at.asc()).all()

@router.get("/documents/{doc_id}", response_model=DocumentRead)
def get_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.post("/documents/upload", response_model=DocumentRead)
def upload_guideline_document(
    title: str = Form(...),
    doc_type: str = Form("GUIDELINE"),
    category: str = Form("BRAND_GOVERNANCE"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save file
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in [".pdf", ".docx", ".txt", ".md"]:
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, TXT, or MD files are supported.")

    save_path = Path(settings.UPLOADS_DIR) / f"{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    extracted_text, detected_format = extract_content(str(save_path), file.filename)

    doc = Document(
        title=title,
        doc_type=doc_type,
        category=category,
        current_version="1.0",
        summary=f"Uploaded policy document {file.filename} ({detected_format})"
    )
    db.add(doc)
    db.flush()

    doc_ver = DocumentVersion(
        document_id=doc.id,
        version_number="1.0",
        content=extracted_text,
        extracted_text=extracted_text[:500],
        file_path=str(save_path),
        file_format=detected_format,
        created_by="Uploaded by Reviewer"
    )
    db.add(doc_ver)

    db.add(AuditLog(
        action="BRAND_DOCUMENT_UPLOADED",
        actor_name="Brand Manager",
        actor_role="REVIEWER",
        target_type="DOCUMENT",
        target_id=doc.id,
        details=f"Uploaded {file.filename} into Brand Vault."
    ))

    db.commit()
    db.refresh(doc)
    return doc

@router.get("/rules", response_model=List[BrandRuleRead])
def get_rules(db: Session = Depends(get_db)):
    return db.query(BrandRule).filter(BrandRule.is_active == True).all()

@router.get("/glossary", response_model=List[GlossaryTermRead])
def get_glossary(db: Session = Depends(get_db)):
    return db.query(GlossaryTerm).filter(GlossaryTerm.is_active == True).order_by(GlossaryTerm.term.asc()).all()

@router.get("/facts", response_model=List[ApprovedFactRead])
def get_facts(db: Session = Depends(get_db)):
    return db.query(ApprovedFact).order_by(ApprovedFact.fact_code.asc(), ApprovedFact.is_historical.asc()).all()

@router.get("/claims", response_model=List[ClaimPassportRead])
def get_claims(db: Session = Depends(get_db)):
    return db.query(ClaimPassport).order_by(ClaimPassport.claim_code.asc()).all()

@router.get("/assets")
def get_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    return [{"id": a.id, "name": a.name, "asset_type": a.asset_type, "specs": a.specs, "svg_content": a.svg_content} for a in assets]
