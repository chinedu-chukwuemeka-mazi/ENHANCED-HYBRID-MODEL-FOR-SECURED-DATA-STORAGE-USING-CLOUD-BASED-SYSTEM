from app import app, db


class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    adminid = db.Column(db.String(255))
    
    def __repr__(self):
        return '%r %r'.format(self.id, self.adminid)
        
        
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    job = db.Column(db.String(255))
    userid = db.Column(db.String(255))
    
    def __repr__(self):
        return '%r %r'.format(self.id, self.userid)