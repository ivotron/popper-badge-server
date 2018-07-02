import os

from app import app
from unittest import TestCase


class TestPopperBadgeServer(TestCase):

    @classmethod
    def setUpClass(self):
        """Runs once for the entire test suite.
        """
        self.DB_NAME = 'test-db.json'
        app.config['DB_NAME'] = self.DB_NAME

    @classmethod
    def tearDownClass(self):
        """Runs once for the entire test suite.
        """
        del app.config['DB_NAME']

    def setUp(self):
        """Runs once for each test. Sets up the tests.
        """
        self.app = app.test_client()

    def tearDown(self):
        """Runs once for each test. Cleans up, i.e., deletes the test database.
        """
        if os.path.isfile(self.DB_NAME):
            os.remove(self.DB_NAME)

    def test_get_badge_without_data(self):
        """When no data is present, test whether the app is properly redirected
        with proper status code and proper redirect url."""
        response = self.app.get('/systemslab/popper')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            'https://img.shields.io/badge/Popper-undefined-lightgrey.svg'
        )

    def test_post_correct_data(self):
        response = self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'OK',
            'timestamp': '1530440638'
        })
        self.assertEqual(response.status_code, 201)

    def test_post_incorrect_data(self):
        response = self.app.post('/systemslab/popper', data={
            'status': 'OK',
            'timestamp': '1530440638'
        })
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'timestamp': '1530440638'
        })
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'OK',
        })
        self.assertEqual(response.status_code, 400)

    def test_get_status_ok_badge(self):
        """When no data is present, test whether the app is properly redirected
        with proper status code and proper redirect url."""
        self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'OK',
            'timestamp': '1530440638'
        })
        response = self.app.get('/systemslab/popper')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            'https://img.shields.io/badge/Popper-OK-green.svg'
        )

    def test_get_status_gold_badge(self):
        """When no data is present, test whether the app is properly redirected
        with proper status code and proper redirect url."""
        self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'GOLD',
            'timestamp': '1530440638'
        })
        response = self.app.get('/systemslab/popper')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            'https://img.shields.io/badge/Popper-GOLD-yellow.svg'
        )

    def test_get_status_fail_badge(self):
        """When no data is present, test whether the app is properly redirected
        with proper status code and proper redirect url."""
        self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'FAIL',
            'timestamp': '1530440638'
        })
        response = self.app.get('/systemslab/popper')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            'https://img.shields.io/badge/Popper-FAIL-red.svg'
        )

    def test_get_list_without_data(self):
        """When no data is present, test whether empty data is returned fro the
        org:repo from the list endpoint."""
        response = self.app.get('/systemslab/popper/list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_list_with_data(self):
        """When no data is present, test whether empty data is returned fro the
        org:repo from the list endpoint."""
        self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'OK',
            'timestamp': '1530440638'
        })
        response = self.app.get('/systemslab/popper/list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [{'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
              'status': 'OK'}]
        )
