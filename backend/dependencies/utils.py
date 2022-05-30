# import os
# import re
# from uuid import uuid4 as uuid

# import bcrypt
# from fastapi import Header, HTTPException, Request, Depends
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# from db.models import ENV, Session, User, Location, Ping, get_db
# from db import schemas, crud
# from template.verificaition_email import TEMPLATE_EMAIL

# def generate_unique(req_type='hex') -> str:
#     if req_type == 'str':
#         data = str(uuid())
#     elif req_type == 'int':
#         data = uuid().int
#     elif req_type == 'hex':
#         data = uuid().hex
#     else:
#         data = uuid()
#     return data


# def verify_email(email: str) -> bool:
#     email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#     if re.match(email_regex, email):
#         return True
#     else:
#         return False


# def verify_password_hash(password: str, password_hash: str) -> bool:
#     password = password.encode()
#     password_hash = password_hash.encode()
#     return bcrypt.checkpw(password, password_hash)


# def generate_password_hash(password: str) -> str:
#     return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# async def get_query_token(db: Session, token: str):
#     token = db.query(JWT).filter(JWT.token == token).first()
#     if not token:
#         raise HTTPException(status_code=400, detail="Invalid token")


# async def get_token_header(db: Session, x_token: str = Header(...)):
#     x_token = db.query(JWT).filter(JWT.token == x_token).first()
#     if not x_token:
#         raise HTTPException(status_code=400, detail="X-Token header invalid")


# async def send_email(email: str, subject: str, content: str):
#     message = Mail(
#         from_email='edespigo@gmail.com',
#         to_emails=email,
#         subject=subject,
#         html_content=content)
    # try:
    #     sg = SendGridAPIClient(ENV['SENDGRID_API_KEY'])
    #     response = sg.send(message)
    #     print(response.status_code)
    #     print(response.body)
    #     print(response.headers)
    # except Exception as e:
    #     print(e.message)

# async def send_verification_email(db: Session, user_id:int, email: str, token: str):
#     user = crud.get_user(db, user_id)
#     subject="Bienvenido a GeoMeetr"
#     email_template = TEMPLATE_EMAIL
#     email_template = email_template.replace("USER_NAME", user.name)
#     email_template = email_template.replace("USER_EMAIL", user.email)
#     email_template = email_template.replace("USER_LINK", f"{ENV['URL_API']}/users/{user_id}/verify/{token}")
#     content = email_template
#     await send_email(email=email, subject=subject , content=content)

# def get_user_by_token(request: Request, db: Session = Depends(get_db)):
#     token = request.headers.get("Authorization")
#     print(f'Token: {token}')
#     if not token:
#         raise HTTPException(status_code=401, detail="Token is missing")
#     query_token = db.query(JWT).filter(JWT.token == token).first()
#     if not query_token:
#         raise HTTPException(status_code=401, detail="Token is invalid")
#     user = query_token.user
#     return user