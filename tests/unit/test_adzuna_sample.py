import os
import unittest
from unittest.mock import Mock, patch

from src.techstack_compass.core import config
from src.techstack_compass.data import adzuna_sample


class TestAdzunaSample(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    @patch("src.techstack_compass.core.config.dotenv.find_dotenv", return_value="/tmp/test.env")
    @patch("src.techstack_compass.core.config.dotenv.load_dotenv")
    def test_get_adzuna_credentials_uses_dotenv_finder(
        self,
        load_dotenv_mock: Mock,
        find_dotenv_mock: Mock,
    ) -> None:
        os.environ["APP_ID"] = "test-app-id"
        os.environ["APP_KEY"] = "test-app-key"

        app_id, app_key = config.get_adzuna_credentials()

        self.assertEqual(app_id, "test-app-id")
        self.assertEqual(app_key, "test-app-key")
        find_dotenv_mock.assert_called_once_with(usecwd=True)
        load_dotenv_mock.assert_called_once_with("/tmp/test.env")

    @patch("src.techstack_compass.data.adzuna_sample.get_adzuna_credentials", return_value=("app-id", "app-key"))
    @patch("src.techstack_compass.data.adzuna_sample.httpx.get")
    def test_fetch_adzuna_sample_builds_request(self, httpx_get_mock: Mock, _get_adzuna_credentials_mock: Mock) -> None:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"results": []}
        httpx_get_mock.return_value = mock_response

        payload = adzuna_sample.fetch_adzuna_sample("gb", "data engineer", 3)

        self.assertEqual(payload, {"results": []})
        httpx_get_mock.assert_called_once()
        kwargs = httpx_get_mock.call_args.kwargs
        self.assertEqual(kwargs["timeout"], 20.0)
        self.assertEqual(kwargs["params"]["app_id"], "app-id")
        self.assertEqual(kwargs["params"]["app_key"], "app-key")
        self.assertEqual(kwargs["params"]["what"], "data engineer")
        self.assertEqual(kwargs["params"]["results_per_page"], 3)


if __name__ == "__main__":
    unittest.main()
