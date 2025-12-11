from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import pymysql

# Importamos nuestras propias herramientas
from app.database import get_db_connection
from app.schemas import UserCreate, Token
from app.security import verify_password, get_password_hash, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Autenticación"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            hashed_pw = get_password_hash(user.password)
            sql = "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user.username, user.email, hashed_pw))
        conn.commit()
        return {"message": "Usuario creado exitosamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    finally:
        conn.close()

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    user_db = None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (form_data.username,))
            user_db = cursor.fetchone()
    finally:
        conn.close()

    if not user_db or not verify_password(form_data.password, user_db['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_db['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user, "role": "authenticated_user"}