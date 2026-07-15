from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileResponse, ResumeImportRequest, ResumeImportResponse
from app.services import get_profile, create_or_update_profile, import_resume, get_profile_versions
from app.utils.deps import get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.get("", response_model=ProfileResponse)
async def get_user_profile(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    profile = await get_profile(db, str(user.id))
    return profile


@router.post("", response_model=ProfileResponse)
async def update_profile(
    data: ProfileCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile = await create_or_update_profile(db, str(user.id), data)
    return profile


@router.post("/import-resume", response_model=ResumeImportResponse)
async def import_resume_text(
    request: ResumeImportRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile_data = await import_resume(db, str(user.id), request.resume_text)
    return {"success": True, "profile_data": profile_data}


@router.post("/upload-resume", response_model=ResumeImportResponse)
async def upload_resume_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 校验文件类型
    import os
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件格式: {ext}，仅支持 {', '.join(ALLOWED_EXTENSIONS)}")

    # 读取文件内容
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过 5MB 限制")

    # 提取文本
    text = await extract_text(content, ext)
    if not text.strip():
        raise HTTPException(status_code=400, detail="无法从文件中提取文本内容")

    profile_data = await import_resume(db, str(user.id), text)
    return {"success": True, "profile_data": profile_data}


async def extract_text(content: bytes, ext: str) -> str:
    if ext == ".txt":
        return content.decode("utf-8", errors="ignore")

    if ext == ".pdf":
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=content, filetype="pdf")
            return "\n".join(page.get_text() for page in doc)
        except ImportError:
            raise HTTPException(status_code=500, detail="PDF 解析依赖未安装，请安装 PyMuPDF: pip install pymupdf")

    if ext in (".docx", ".doc"):
        try:
            from io import BytesIO
            from docx import Document
            doc = Document(BytesIO(content))
            return "\n".join(para.text for para in doc.paragraphs if para.text.strip())
        except ImportError:
            raise HTTPException(status_code=500, detail="Word 解析依赖未安装，请安装 python-docx: pip install python-docx")

    return ""


@router.get("/versions", response_model=list[ProfileResponse])
async def get_profile_version_history(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    versions = await get_profile_versions(db, str(user.id))
    return versions
