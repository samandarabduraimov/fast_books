from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime

from database import SessionLocal
from models import User
from schemas import SignUp, Login

class Settings(BaseModel):
    authjwt_secret_key: str = '76ce38ef876902afa65ba6b260015efd40abe3ff251ccc5381ab876baba93364'

@AuthJWT.load_config
def get_config():
    return Settings()

auth_router = APIRouter(
    prefix="/auth"
)

@auth_router.get('/')
async def get_auth(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {"message": "This is the auth signup page."}

@auth_router.post('/signup', status_code=201)
async def signup(user: SignUp):
    session = SessionLocal()

    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return {'message': 'Email already exists', 'status_code': status.HTTP_400_BAD_REQUEST}
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return {'message': 'Username already exists', 'status_code': status.HTTP_400_BAD_REQUEST}
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )
    session.add(new_user)
    session.commit()
    user_data = {
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
    }
    return {'message': 'User created successfully', 'new_user': user_data, 'status': status.HTTP_201_CREATED}

@auth_router.post('/login', status_code=200)
async def login(user: Login, Authorize: AuthJWT = Depends()):
    session = SessionLocal()
    db_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )
    ).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_lifetime = timedelta(minutes=60)
        refresh_lifetime = timedelta(days=3)
        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_lifetime)
        token = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        response_data = {
            'status': status.HTTP_200_OK,
            'message': "Successfully logged in",
            'token': token
        }
        return response_data
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid username, email or password')

@auth_router.get('/login/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    session = SessionLocal()
    try:
        access_lifetime = timedelta(minutes=60)
        refresh_lifetime = timedelta(days=3)
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        db_user = session.query(User).filter(User.username == current_user).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        new_access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        response_model = {
            'success': True,
            'code': 200,
            'message': "New access token is created.",
            'data': {
                "access_token": new_access_token
            }
        }
        return response_model

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

@auth_router.get('/logout')
async def logout(Authorize: AuthJWT = Depends()):
    try:
        jti = Authorize.get_raw_jwt()['jti']
        response = {'success': True, 'code': 200, 'message': 'Successfully logged out.'}
        return jsonable_encoder(response)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")