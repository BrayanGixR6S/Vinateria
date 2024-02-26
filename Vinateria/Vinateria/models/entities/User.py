from werkzeug.security import check_password_hash



class User():

     def __init__(self, id, username, password, fullname="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname

     @classmethod
     def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
     
    