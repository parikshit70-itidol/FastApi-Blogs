from passlib.context import CryptContext
cntx_pass = CryptContext(schemes=["bcrypt"],deprecated = "auto")


class Hash():
    def bcrypt(password:str):
        return cntx_pass.hash(password) 
    def verify(hashed_password,plain_password):
        return cntx_pass.verify(plain_password,hashed_password)