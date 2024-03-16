# FastAPI auto generates documentation and Postman-like interface for testing API.

# FastAPI has some patterns for user login and API keys 
# Although we can handle auth later.

# During creation of the database, run this to create the password table
# INSERT INTO users VALUES (1, 'johndoe', 'johndoe@example.com', 'John Doe', false, '$2b$12$dQD2AD2Y.Aa8F3IliHPfk.yNESW7FZe3RmeT38K661sg/vds404ga');

# from datetime import datetime, timedelta
# from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from pydantic import BaseModel
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select

from pycognito import Cognito

app = FastAPI()


# Redirects root to docs
# @app.get("/", include_in_schema=False)
# def root() -> RedirectResponse:
#     """Redirects the root ("/") to the /docs url."""
#     return RedirectResponse(url='/docs')


# @app.on_event("startup")
# async def start_db():
#     """Generates DB is there is none, starts database from file if exists."""
#     async with database.engine.begin() as conn:
#         await conn.run_sync(database.Base.metadata.create_all)


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# async def get_user(db: AsyncSession, username: str) -> database.User:
#     result = await db.execute(select(database.User).filter_by(username=username))
#     return result.scalars().first()


# async def authenticate_user(db: AsyncSession, username: str, password: str) -> database.User:
#     user = await get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)) -> database.User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except:
#         raise credentials_exception
#     user = await get_user(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)) -> database.User:
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token", response_model=Token)
# async def login_for_access_token(db: AsyncSession = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
#     """GETs user api token"""
#     user = await authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     """GETs user data, which includes username, password hash, and email"""
#     return current_user

# DATA ========================
@app.get("/api/{reactor}/{sensor}")
def get_sensor_data_range(reactor: str, sensor: str, requestJSON):
    """
    GET request for requesting sensor data from Cloud database (AWS Timestream).
    - param command: TODO: Request JSON Schema TBD
    - return: TODO: Historical Data JSON Schema TBD
    """
    # TODO: requestJSON: {reactor:, sensor:, datetimestart, datetimeend}
    print(f"sensor: {sensor}")
    # TODO: SQL REQUEST FROM TIMESTREAM (previous API)
    return ""

# REACTOR COMMANDS ===========
@app.post("/api/{reactor}/{command}")
def post_command(reactor:str, command: str):
    """
    POST request for sending commands to the Pi over MQTT. Converts frontend http api call to an MQTT publish. 
    - param command: TODO: syntax of command TBD 
    - return: TODO: TBD
    """
    # request payload JSON: {reactor:, command:}
    print(f"command: {command}")
    # TODO: MQTT SEND
    # TODO: MQTT READ
    return ""