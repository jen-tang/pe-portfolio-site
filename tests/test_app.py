import unittest
import os

os.environ['TESTING'] = 'true'
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<!DOCTYPE html>' in html
        assert "<h2>Welcome to My Portfolio!</h2>" in html

    def test_timeline(self):
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert 'timeline_posts' in json
        assert len(json['timeline_posts']) == 0

        send = self.client.post('/api/timeline_post', data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'content': 'Hello World'
        })
        assert send.status_code == 200
        res = self.client.get('/api/timeline_post')
        assert res.status_code == 200
        json = res.get_json()
        assert 'timeline_posts' in json
        assert len(json['timeline_posts']) == 1
        assert json['timeline_posts'][0]['name'] == 'John Doe'
        assert json['timeline_posts'][0]['content'] == 'Hello World'
        assert json['timeline_posts'][0]['email'] == 'john@example.com'

    def test_malformed_timeline_post(self):
        # missing name
        response = self.client.post('/api/timeline_post', data={
            'email': 'john@example.com',
            'content': 'Hello World'
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert 'Invalid name' in html

        # empty content
        response = self.client.post('/api/timeline_post', data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'content': ''
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert 'Invalid content' in html

        # malformed email
        response = self.client.post('/api/timeline_post', data={
            'name': 'John Doe',
            'email': 'not an email',
            'content': 'Hello World'
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert 'Invalid email' in html
