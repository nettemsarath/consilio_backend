from fastapi import HTTPException, Header, status
from supabase_client import supabase_client

async def verify_token(token: str = Header(...)):
    print("hiiiii", token)
    try:
        user = supabase_client.auth.get_user( token )
        if user:
            return user
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

def verify_jwt(jwtoken: str) -> bool:
    try:
        jwt.decode(jwtoken, JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        return True
    except JWTError:
        return False