from flask import request, jsonify, current_app
from functools import wraps
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

def encode_token(mechanic_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(mechanic_id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=7)).timestamp()),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth.split(" ", 1)[1].strip()
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.mechanic_id = int(payload.get("sub"))
        except JWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        return fn(*args, **kwargs)
    return wrapper
