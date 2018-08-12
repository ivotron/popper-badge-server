import os
import time

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
        try:
            data = response.data.decode()
        except AttributeError:
            data = response.data
        self.assertIn('undefined', data)
        self.assertEqual(response.content_type, 'image/svg+xml')
        self.assertEqual(response.status_code, 200)

    def test_post_correct_data(self):
        response = self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'SUCCESS',
            'timestamp': '1530440638',
            'branch': 'master'
        })
        self.assertEqual(response.status_code, 201)

    def test_post_incorrect_data(self):
        response = self.app.post('/systemslab/popper', data={
            'status': 'SUCCESS',
            'timestamp': '1530440638'
        })
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'timestamp': '1530440638',
            'branch': 'master'
        })
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'SUCCESS',
            'branch': 'master'
        })
        self.assertEqual(response.status_code, 400)

    def test_get_status_success_badge(self):
        """When no data is present, test whether the app is properly redirected
        with proper status code and proper redirect url."""
        self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'SUCCESS',
            'timestamp': '1530440638',
            'branch': 'master'
        })
        response = self.app.get('/systemslab/popper')
        try:
            data = response.data.decode()
        except AttributeError:
            data = response.data
        self.assertIn('SUCCESS', data)
        self.assertEqual(response.content_type, 'image/svg+xml')
        self.assertEqual(response.status_code, 200)

    def test_get_status_gold_badge(self):
        """When no data is present, test whether the app is properly redirected
        with proper status code and proper redirect url."""
        self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'GOLD',
            'timestamp': '1530440638',
            'branch': 'master'
        })
        response = self.app.get('/systemslab/popper')
        try:
            data = response.data.decode()
        except AttributeError:
            data = response.data
        self.assertIn('GOLD', data)
        self.assertEqual(response.content_type, 'image/svg+xml')
        self.assertEqual(response.status_code, 200)

    def test_get_status_fail_badge(self):
        """When no data is present, test whether the app is properly redirected
        with proper status code and proper redirect url."""
        self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'FAIL',
            'timestamp': '1530440638',
            'branch': 'master'
        })
        response = self.app.get('/systemslab/popper')
        try:
            data = response.data.decode()
        except AttributeError:
            data = response.data
        self.assertIn('FAIL', data)
        self.assertEqual(response.content_type, 'image/svg+xml')
        self.assertEqual(response.status_code, 200)

    def test_get_incorrect_status_badge(self):
        """When no data is present, test whether the app is properly redirected
        with proper status code and proper redirect url."""
        self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'blahblah',
            'timestamp': '1530440638',
            'branch': 'master'
        })
        response = self.app.get('/systemslab/popper')
        try:
            data = response.data.decode()
        except AttributeError:
            data = response.data
        self.assertIn('undefined', data)
        self.assertEqual(response.content_type, 'image/svg+xml')
        self.assertEqual(response.status_code, 200)

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
            'status': 'SUCCESS',
            'timestamp': '1530440638',
            'branch': 'master'
        })
        response = self.app.get('/systemslab/popper/list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [{'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
              'status': 'SUCCESS',
              'timestamp': time.strftime(
                  '%Y-%m-%d %H:%M:%S', time.localtime(1530440638)
              )}]
        )

    def test_non_master_branch(self):
        """When the code is run from a non-master branch, the server does
        not store the data.
        """
        response = self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'SUCCESS',
            'timestamp': '1530440638',
            'branch': 'test'
        })
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/systemslab/popper')
        try:
            data = response.data.decode()
        except AttributeError:
            data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertIn('undefined', data)

    def test_headers(self):
        """Test the response headers returned from a GET request.
        """
        response = self.app.get('/systemslab/popper')
        self.assertTrue('Cache-Control' in response.headers)
        self.assertEqual(response.headers['Cache-Control'], 'no-cache')
        self.assertTrue('Last-Modified' in response.headers)

    def test_records_with_same_commit_id(self):
        """Test the situation when two records with same commit id is created.
        The one submitted later should be returned with the GET request and
        also a new record shouldn't be created.
        """
        response = self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'SUCCESS',
            'timestamp': '1530440638',
            'branch': 'master'
        })
        self.assertEqual(response.status_code, 201)
        response = self.app.get('/systemslab/popper')
        try:
            data = response.data.decode()
        except AttributeError:
            data = response.data
        self.assertIn('SUCCESS', data)

        response = self.app.post('/systemslab/popper', data={
            'commit_id': '8d90af11efd1d8ff164775b9406928b22d688d79',
            'status': 'FAIL',
            'timestamp': '1530440679',
            'branch': 'master'
        })
        self.assertEqual(response.status_code, 201)
        response = self.app.get('/systemslab/popper')
        try:
            data = response.data.decode()
        except AttributeError:
            data = response.data
        self.assertIn('FAIL', data)

        response = self.app.get('/systemslab/popper/list')
        self.assertEqual(len(response.json), 1)
