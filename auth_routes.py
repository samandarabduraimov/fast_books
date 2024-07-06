from fastapi import APIRouter
from database import SessionLocal,engine
from schemas import SignUp
from models import User
from werkzeug.security import generate_password_hash,check_password_hash
from fastapi import status

auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.get('/')
async def get_auth():
    return {'message': 'Authentication Successful!'}

@auth_router.post('/signup',status_code=status.HTTP_201_CREATED)
async def signup(user : SignUp):
    session = SessionLocal()

    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return {'message': 'Email already registered!'}
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return {'message': 'Username already registered!'}
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff

    )
    session.add(new_user)
    return {'message': 'User created!', 'new_user': new_user}