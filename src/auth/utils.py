from passlib.context import CryptContext

password_context = CryptContext(
    schemes=["bcrypt"]
)

def generate_hash_password(password: str) -> str:
    hash_password = password_context.hash(password)

    return hash_password

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

