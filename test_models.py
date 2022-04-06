from unittest import TestCase

from app import app
from models import db, User

# Setup test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test for user models"""
    
    """Setup columns for model"""
    default_user_icon = '/static/img/user_icon.png'
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=default_user_icon)


    def setUp(self):
        """Clear database"""
        User.query.delete()

    def tearDown(self):
        """Clean up the session upon completion"""
        db.session.rollback()

    def testTable(self):
        test_user = User(first_name = "First Name - Test", last_name ="Last Name - Test", image_url = "/testurl")
        self.assertEqual(test_user.first_name, "First Name - Test")
        self.assertEqual(test_user.last_name, "Last Name - Test")
        self.assertEqual(test_user.image_url, "/testurl")
        self.assertEqual(test_user.full_name, "First Name - Test Last Name - Test")