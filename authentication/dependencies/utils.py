import os
import re
from uuid import uuid4 as uuid

import bcrypt
from fastapi import Header, HTTPException, Request, Depends
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from db.models import ENV, Session, User, get_db
from db import schemas, crud
from template.verificaition_email import TEMPLATE_EMAIL


def verify_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False


async def send_email(email: str, subject: str, content: str):
    message = Mail(
        from_email='edespigo@gmail.com',
        to_emails=email,
        subject=subject,
        html_content=content)
    # try:
    #     sg = SendGridAPIClient(ENV['SENDGRID_API_KEY'])
    #     response = sg.send(message)
    #     print(response.status_code)
    #     print(response.body)
    #     print(response.headers)
    # except Exception as e:
    #     print(e.message)

async def send_verification_email(db: Session, user_id: int, email: str, token: str):
    user = crud.get_user(db, user_id)
    subject="Bienvenido a GeoMeetr"
    email_template = TEMPLATE_EMAIL
    email_template = email_template.replace("USER_NAME", user.name)
    email_template = email_template.replace("USER_EMAIL", user.email)
    email_template = email_template.replace("USER_LINK", f"{ENV['URL_API']}/users/{user_id}/verify/{token}")
    content = email_template
    await send_email(email=email, subject=subject , content=content)