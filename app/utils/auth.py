from flask import request, jsonify, current_app
from functools import wraps
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

# === Encode token with user_id + role ===
def encode_token(user_id: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=365)).timestamp()),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

# === Decorator to enforce token auth ===
def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth:
            return jsonify({"error": "Missing Authorization header"}), 401

        # Handle both "Bearer <token>" and "<token>"
        token = auth.split(" ")[-1].strip()

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.mechanic_id = int(payload.get("sub"))
            request.mechanic_role = payload.get("role")
        except JWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        return fn(*args, **kwargs)
    return wrapper
