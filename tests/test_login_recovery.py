"""Regression checks for automatic login without a saved browser session."""

import unittest
from unittest.mock import Mock

import requests

from checkin import NewAPICheckin


def response(status, payload, cookie=None):
    result = Mock()
    result.status_code = status
    result.json.return_value = payload
    result.cookies = requests.cookies.RequestsCookieJar()
    if cookie is not None:
        result.cookies.set('session', cookie)
    result.headers = {}
    return result


class LoginRecoveryTests(unittest.TestCase):
    def client(self, **kwargs):
        return NewAPICheckin(
            'https://example.invalid', '',
            login_username='test-user', login_password='test-password', **kwargs,
        )

    def test_empty_session_recovers_and_sets_user_header_before_self_retry(self):
        client = self.client(user_id='old-id')
        calls = []

        def get_user(url, **kwargs):
            calls.append(url)
            if len(calls) == 1:
                return response(401, {'success': False})
            self.assertEqual(client.session.headers['new-api-user'], '42')
            return response(200, {'success': True, 'data': {'id': 42}})

        client.session.get = Mock(side_effect=get_user)
        client.session.post = Mock(return_value=response(
            200, {'success': True, 'data': {'id': 42}}, cookie='test-new-session',
        ))

        self.assertEqual(client.get_user_info(), {'id': 42})
        self.assertEqual(client.session_cookie, 'test-new-session')
        self.assertEqual(client.session.post.call_count, 1)

    def test_invalid_password_does_not_report_login_success(self):
        client = self.client()
        client.session.post = Mock(return_value=response(
            200, {'success': False, 'message': 'Invalid credentials'},
        ))
        self.assertFalse(client._try_login())
        self.assertEqual(client.session_cookie, '')

    def test_success_without_cookie_does_not_report_authenticated(self):
        client = self.client()
        client.session.post = Mock(return_value=response(
            200, {'success': True, 'data': {'require_2fa': True}},
        ))
        self.assertFalse(client._try_login())

    def test_rate_limit_does_not_loop_login(self):
        client = self.client()
        client.session.post = Mock(return_value=response(429, {}))
        self.assertFalse(client._try_login())
        self.assertEqual(client.session.post.call_count, 1)


if __name__ == '__main__':
    unittest.main()
