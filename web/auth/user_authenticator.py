from functools import wraps
from typing import Callable, Any
from flask import request, jsonify
from di.container import container

def user_authenticator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401
            
        user_id = container.auth_service.authorize(auth_header)
        
        if user_id is None:
            return jsonify({"error": "Unauthorized"}), 401
            
        return func(user_id, *args, **kwargs)
        
    return wrapper
