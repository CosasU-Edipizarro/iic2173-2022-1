import os
import re
from uuid import uuid4 as uuid

import bcrypt
from fastapi import Header, HTTPException
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from db.models import ENV, Session, User, JWT, Location, Ping
from db import schemas

def generate_unique(req_type='hex') -> str:
    if req_type == 'str':
        data = str(uuid())
    elif req_type == 'int':
        data = uuid().int
    elif req_type == 'hex':
        data = uuid().hex
    else:
        data = uuid()
    return data


def verify_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False


def verify_password_hash(password: str, password_hash: str) -> bool:
    password = password.encode()
    return bcrypt.check_password_hash(password_hash, password)


def generate_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


async def get_query_token(db: Session, token: str):
    token = db.query(JWT).filter(JWT.token == token).first()
    if not token:
        raise HTTPException(status_code=400, detail="Invalid token")


async def get_token_header(db: Session, x_token: str = Header(...)):
    x_token = db.query(JWT).filter(JWT.token == x_token).first()
    if not x_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def send_email(email: str, subject: str, content: str):
    message = Mail(
        from_email='edespigo@gmail.com',
        to_emails=email,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(ENV['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

async def send_verification_email(email: str, token: str):
    subject="Verifica tu correo"
    content = f"""
        <p>Verifica tu correo</p>
        <a href="https://api.iic2173-g19.xyz" target="_blank">
        <button>¡Verificar correo!</button>
    """
    await send_email(email=email, subject=subject , content=content)