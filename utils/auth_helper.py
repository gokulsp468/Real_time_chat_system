from fastapi import Depends, HTTPException, WebSocket, status, Request
from fastapi.security import OAuth2PasswordBearer
from utils.token_helper import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):  # Correct usage of Depends
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = verify_access_token(token)
    if user is None:
        raise credentials_exception
    return user



async def get_current_user_from_websocket(websocket: WebSocket):
    # Get the Authorization header from WebSocket's headers
    token = websocket.headers.get("Authorization")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Remove the 'Bearer ' prefix
    token = token.split(" ")[1] if token.startswith("Bearer ") else token
    user = verify_access_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user