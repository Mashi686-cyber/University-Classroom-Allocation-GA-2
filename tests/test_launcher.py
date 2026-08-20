import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to sys.path so we can import start.py
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import start

class TestLauncher(unittest.TestCase):
    @patch('start.shutil_which')
    def test_check_command_found(self, mock_which):
        mock_which.side_effect = lambda x: f"/usr/bin/{x}" if x == "python3" else None
        result = start.check_command(["python3", "python", "py"])
        self.assertEqual(result, "python3")

    @patch('start.shutil_which')
    def test_check_command_not_found(self, mock_which):
        mock_which.return_value = None
        result = start.check_command(["python3", "python", "py"])
        self.assertIsNone(result)

    @patch('start.socket.socket')
    def test_check_port_free(self, mock_socket_class):
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        # connect_ex returns 1 (non-zero) when connection fails (port is free)
        mock_socket_instance.connect_ex.return_value = 1
        
        self.assertTrue(start.check_port(8000))

    @patch('start.socket.socket')
    def test_check_port_in_use(self, mock_socket_class):
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        # connect_ex returns 0 when connection succeeds (port is in use)
        mock_socket_instance.connect_ex.return_value = 0
        
        self.assertFalse(start.check_port(8000))

    @patch('start.urllib.request.urlopen')
    def test_wait_for_health_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = start.wait_for_health("http://127.0.0.1:8000/api/health", timeout=1)
        self.assertTrue(result)

    @patch('start.urllib.request.urlopen')
    def test_wait_for_health_timeout(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
        
        # Keep timeout short for test speed
        result = start.wait_for_health("http://127.0.0.1:8000/api/health", timeout=0.1)
        self.assertFalse(result)

    def test_path_construction(self):
        # Verify the script locates the correct paths regardless of OS
        self.assertTrue(
            str(start.PROJECT_ROOT).endswith("UniClass-GA") or 
            str(start.PROJECT_ROOT).endswith("UniClass-GA-FINAL")
        )
        self.assertTrue(str(start.BACKEND_DIR).endswith("backend"))
        self.assertTrue(str(start.FRONTEND_DIR).endswith("frontend"))
        self.assertEqual(start.BACKEND_REQ.name, "requirements.txt")
        self.assertEqual(start.FRONTEND_PKG.name, "package.json")

if __name__ == '__main__':
    unittest.main()
