import os
import unittest
import json
from readrr_api import create_app

app = create_app()

json_path = os.path.join(
    os.path.dirname(__file__),
    'mock_bookshelf.json'
    )
# set up mock bookshelf for POST test
with open(json_path) as data:
    bookshelf = json.load(data)

relevant_details = [
    'googleId', 'title', 'authors', 'publisher',
    'publishedDate', 'description', 'industryIdentifiers',
    'pageCount', 'categories', 'thumbnail', 'smallThumbnail',
    'language', 'webReaderLink', 'textSnippet', 'isEbook',
    'averageRating'
]


class TestRecRoutes(unittest.TestCase):

    def setUp(self):
        """Set up testing connection"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()
        self.assertEqual(app.debug, True)

    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.app.post("/recommendations", json=bookshelf)
        self.assertEqual(response.status_code, 200)

    def test_res_content(self):
        response = self.app.post("/recommendations", json=bookshelf)
        data = response.json
        self.assertEqual(len(data.keys()), 2)
        for detail in relevant_details:
            self.assertIn(detail, data['recommendations'][0].keys())
