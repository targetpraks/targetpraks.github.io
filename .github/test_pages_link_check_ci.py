import importlib.util
from pathlib import Path
import unittest
from unittest import mock
import urllib.error


SPEC = importlib.util.spec_from_file_location(
    "pages_link_check_ci", Path(__file__).with_name("pages_link_check_ci.py"))
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)
URL = "https://example.invalid/published.html"


def http_error(code):
    return urllib.error.HTTPError(URL, code, "test response", None, None)


def ok():
    response = mock.MagicMock()
    response.__enter__.return_value.status = 200
    return response


class Clock:
    def __init__(self):
        self.now = 0.0

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class StatusTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.urlopen = self.patch(checker.urllib.request, "urlopen")
        self.sleep = self.patch(checker.time, "sleep", side_effect=self.clock.sleep)
        self.patch(checker.time, "monotonic", side_effect=self.clock.monotonic)

    def patch(self, target, name, **kwargs):
        patcher = mock.patch.object(target, name, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def methods(self):
        return [call.args[0].get_method() for call in self.urlopen.call_args_list]

    def test_transient_503_then_200_succeeds(self):
        self.urlopen.side_effect = [http_error(503), ok()]
        self.assertEqual(checker.status(URL), 200)
        self.assertEqual(self.methods(), ["HEAD", "HEAD"])
        self.sleep.assert_called_once_with(1)

    def test_persistent_503_remains_a_failure_after_three_attempts(self):
        self.urlopen.side_effect = [http_error(503) for _ in range(3)]
        self.assertEqual(checker.status(URL), 503)
        self.assertEqual(self.urlopen.call_count, 3)
        self.assertEqual(self.sleep.call_args_list, [mock.call(1), mock.call(2)])

    def test_403_and_404_fail_immediately(self):
        for code in (403, 404):
            with self.subTest(code=code):
                self.urlopen.reset_mock()
                self.sleep.reset_mock()
                self.urlopen.side_effect = http_error(code)
                self.assertEqual(checker.status(URL), code)
                self.assertEqual(self.urlopen.call_count, 1)
                self.sleep.assert_not_called()

    def test_head_405_still_falls_back_to_get(self):
        self.urlopen.side_effect = [http_error(405), ok()]
        self.assertEqual(checker.status(URL), 200)
        self.assertEqual(self.methods(), ["HEAD", "GET"])
        self.sleep.assert_not_called()

    def test_get_retry_does_not_repeat_unsupported_head(self):
        self.urlopen.side_effect = [http_error(405), http_error(503), ok()]
        self.assertEqual(checker.status(URL), 200)
        self.assertEqual(self.methods(), ["HEAD", "GET", "GET"])
        self.sleep.assert_called_once_with(1)

    def test_timeout_is_not_retried(self):
        self.urlopen.side_effect = TimeoutError("test timeout")
        self.assertIsNone(checker.status(URL))
        self.assertEqual(self.urlopen.call_count, 1)
        self.sleep.assert_not_called()

    def test_retries_use_only_the_remaining_timeout_budget(self):
        def request(_req, **_kwargs):
            self.clock.now += 6
            if self.urlopen.call_count == 1:
                raise http_error(503)
            return ok()

        self.urlopen.side_effect = request
        self.assertEqual(checker.status(URL), 200)
        self.assertEqual([c.kwargs["timeout"] for c in self.urlopen.call_args_list],
                         [20, 13])

    def test_backoff_never_extends_the_shared_timeout_budget(self):
        def request(_req, **_kwargs):
            self.clock.now += checker.TIMEOUT - 0.5
            raise http_error(503)

        self.urlopen.side_effect = request
        self.assertEqual(checker.status(URL), 503)
        self.assertEqual(self.urlopen.call_count, 1)
        self.sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
