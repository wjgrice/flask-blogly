from unittest import TestCase

from app import app
from models import db, User

# Setup test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly_test'
app.config['SQLALCHEMY_ECHO'] = False

#Make Flask errors be real errors instead of HTML pages with ERROR's info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Test for views on users"""
    """Setup columns for model"""

    def setUp(self):
        """Clear database then build sample user data"""
        User.query.delete()

        user = User(first_name='TestFirstName', last_name='TestLastName', image_url='/testurl')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up the session upon completion"""
        db.session.rollback()

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('TestLastName', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "2nd First Name", "last_name": "2nd Last Name", "image_url": "2nd testurl"}
            resp = client.post("/users/create", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("2nd First Name", html)

