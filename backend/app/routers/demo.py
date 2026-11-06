from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.models import User
from backend.app.schemas.schemas import RoleSwitchRequest, UserRead

router = APIRouter(prefix="/demo", tags=["Demo Controls"])

@router.get("/users")
def list_demo_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]

@router.post("/switch-role")
def switch_demo_role(payload: RoleSwitchRequest, db: Session = Depends(get_db)):
    role = payload.role.upper()
    if role not in ["CREATOR", "REVIEWER"]:
        role = "CREATOR"

    user = db.query(User).filter(User.role == role).first()
    if not user:
        name = "Krish Arora" if role == "CREATOR" else "Sanchita Sharma"
        email = f"{role.lower()}@nexapay.internal"
        user = User(name=name, email=email, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)

    return {
        "active_role": user.role,
        "user_name": user.name,
        "email": user.email,
        "permissions": {
            "can_submit": True,
            "can_apply_fixes": True,
            "can_approve": (user.role == "REVIEWER"),
            "can_request_changes": (user.role == "REVIEWER"),
            "can_sign": (user.role == "REVIEWER")
        }
    }
