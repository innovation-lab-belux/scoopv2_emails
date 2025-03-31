import unittest
from unittest.mock import patch, MagicMock
from app import getToken, PostAgentsAPI, send_email, weekly_task, createChat, askAgentInChat


class TestMain(unittest.TestCase):

    @patch("app.requests.post")  # Fixed module name
    def test_getToken_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "mocked_token"}
        mock_post.return_value = mock_response

        token = getToken()
        self.assertEqual(token, "mocked_token")
        mock_post.assert_called_once()

    @patch("app.requests.post")  # Fixed module name
    def test_getToken_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        token = getToken()
        self.assertIsNone(token)
        mock_post.assert_called_once()

    @patch("app.requests.post")  # Fixed module name
    def test_PostAgentsAPI_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        result = PostAgentsAPI("/test_endpoint", {"key": "value"})
        self.assertEqual(result, {"result": "success"})
        mock_post.assert_called_once()

    @patch("app.requests.post")  # Fixed module name
    def test_PostAgentsAPI_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        result = PostAgentsAPI("/test_endpoint", {"key": "value"})
        self.assertEqual(result, 500)
        mock_post.assert_called_once()

    @patch("app.smtplib.SMTP")  # Fixed module name
    def test_send_email_success(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_email("Test Subject", "Test Body", "test@example.com")
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("mock_email@example.com", "mock_password")
        mock_server.sendmail.assert_called_once()

    @patch("app.smtplib.SMTP")  # Fixed module name
    def test_send_email_failure(self, mock_smtp):
        mock_server = MagicMock()
        mock_server.sendmail.side_effect = Exception("SMTP Error")
        mock_smtp.return_value.__enter__.return_value = mock_server

        with self.assertRaises(Exception):  # Expecting an exception
            send_email("Test Subject", "Test Body", "test@example.com")
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)

    @patch("app.createChat")  # Fixed module name
    @patch("app.askAgentInChat")  # Fixed module name
    @patch("app.send_email")  # Fixed module name
    def test_weekly_task(self, mock_send_email, mock_askAgentInChat, mock_createChat):
        mock_createChat.return_value = "mock_chat_id"
        mock_askAgentInChat.return_value = {"response": "mock_response"}
        mock_send_email.return_value = None

        weekly_task()

        mock_createChat.assert_called_once()
        self.assertEqual(mock_askAgentInChat.call_count, 2)  # Called for each customer
        mock_send_email.assert_called_once_with("test subject", "testing body.", "liano.caekebeke@sap.com")


if __name__ == "__main__":
    unittest.main()