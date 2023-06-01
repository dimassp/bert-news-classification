import sys
import psycopg2

from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi_login import LoginManager

# manager = LoginManager()


from passlib.context import CryptContext

from jose import JWTError, jwt

sys.path.insert(0,r'D:\PROGRAMMING\python\bert_news_type_and_topic_classification\db')

from fake_user_db import fake_users_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "e6852f2d5a1156d44c0a4e5692662c1af93a249ed20782798e03d2950c9fd8c4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3
COOKIE_NAME = "access_token"  
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"encoded_jwt: {type(encoded_jwt)}")
    print(f"to_encode: {type(to_encode['sub'])}")
    # column_total = "%s," * 3
    # column_total = column_total[:-1]
    # args = ','.join(cursor.mogrify(f"({column_total})", tuple([encoded_jwt, to_encode['sub'], True])).decode('utf-8'))
    # sql_insert_token = f"INSERT INTO token (token_id, username, is_valid) values ('{encoded_jwt}', '{to_encode['sub']}', {True})"
    # connection =psycopg2.connect(
    # dbname='postgis_3', user='postgres', 
    # host='localhost', password='zulfiramdani900')
    # cursor = connection.cursor()
    # cursor.execute(sql_insert_token)
    # connection.commit()
    # cursor.close()
    # connection.close()
    # print("token successfully saved into database")
    return encoded_jwt

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# def fake_hash_password(password: str):
#     return "fakehashed" + password

# def fake_decode_token(token):
#     user = get_user(fake_user_db, token)
#     return user
    # return User(
    #     username = token + "fakedecoded", 
    #     email = "john@example.com",
    #     full_name = "John Doe"
    # )

async def get_current_user_from_cookie(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    
    print(f"token from get_current_user: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(f"username payload.get('sub'): {username}")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        # print(f"username from variable token_data: {token_data.username}")
    except JWTError:
        sql_update_token_is_valid_false = f"UPDATE token SET is_valid = FALSE WHERE token_id = '{token}'"
        connection =psycopg2.connect(
        dbname='postgis_3', user='postgres', 
        host='localhost', password='zulfiramdani900')
        cursor = connection.cursor()
        cursor.execute(sql_update_token_is_valid_false)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("token successfully updated")
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        print("Hello world from if user is None")
        raise credentials_exception
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print(f"token from get_current_user: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(f"username payload.get('sub'): {username}")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        print(f"username from variable token_data: {token_data.username}")
    except JWTError:
        sql_update_token_is_valid_false = f"UPDATE token SET is_valid = FALSE WHERE token_id = '{token}'"
        connection =psycopg2.connect(
        dbname='postgis_3', user='postgres', 
        host='localhost', password='zulfiramdani900')
        cursor = connection.cursor()
        cursor.execute(sql_update_token_is_valid_false)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("token successfully updated")
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        print("Hello world from if user is None")
        raise credentials_exception
    return user


    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate" :  "Bearer"}
        )
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    print("hello world from get_current_active_user")
    return current_user

async def get_current_active_user_from_cookie(
    current_user: Annotated[User, Depends(get_current_user_from_cookie)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    print("hello world from get_current_active_user")
    return current_user