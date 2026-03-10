from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
import jwt

def get_user_identifier(request: Request) -> str:
    """
    Extracts the user's email from the JWT token to use as the rate limit key.
    Falls back to the IP address if no valid token is provided.
    """
    auth_header = request.headers.get("Authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            # We skip signature verification here for maximum performance.
            # Real security verification still happens safely in Depends(get_current_user).
            payload = jwt.decode(token, options={"verify_signature": False})
            user_email = payload.get("sub")
            print(f"{user_email} is making a request to {request.url.path}") # Debug log to see which user is making requests TODO: delete this debug
            if user_email:
                return user_email
        except Exception:
            # If token is malformed, just pass and let the fallback handle it
            pass
            
    # Fallback: Use IP address if the user is not authenticated yet
    return get_remote_address(request)

# Initialize the rate limiter using custom user-based key function
limiter = Limiter(key_func=get_user_identifier)