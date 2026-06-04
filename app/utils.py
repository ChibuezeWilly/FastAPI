import bcrypt

def hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    truncated_bytes = password_bytes[:72]
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(truncated_bytes, salt)
    return hashed.decode('utf-8')

def verify(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8')[:72], 
        hashed_password.encode('utf-8')
    )