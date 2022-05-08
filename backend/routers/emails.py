from fastapi import APIRouter, Depends, HTTPException
from db.models import ENV, Session, get_db, User, VerificationEmail
from db import schemas, crud
from dependencies import utils

router = APIRouter( prefix="/email" )

@router.get("/test/{email}")
async def send_test_email(email: str, db: Session = Depends(get_db)):
    # Conectar con modelo Email
    content = '<strong>CREAR TEMPLATE PARA EMAIL</strong>'
    await utils.send_email(email=email, subject="Correo de prueba", content=content)
    return {"status": "ok"}

@router.get("/verify/{token}")
async def verify_user_with_email_token(token: str, db: Session = Depends(get_db)):
    # Conectar con modelo Email'
    email = db.query(VerificationEmail).filter(VerificationEmail.token == token).first()
    if email == None:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = db.query(User).filter(User.id == email.user_id).first()
    if user == None:
        raise HTTPException(status_code=400, detail="Invalid user")
    if user.verified == True:
        raise HTTPException(status_code=400, detail="User already verified")
    user.verified = True
    db.commit()
    return {"status": "ok"}
    