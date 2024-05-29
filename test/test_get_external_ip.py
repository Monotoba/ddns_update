import requests
import re

from src.ddns_update import get_external_ip

# Dependencies:
# pip install pytest-mock
import pytest


class TestGetExternalIp:

    #  Successfully retrieves external IP address from ipecho.net
    def test_successfully_retrieves_external_ip(self, mocker):
        mock_response = mocker.Mock()
        mock_response.text = '123.123.123.123'
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch('requests.get', return_value=mock_response)

        from src.ddns_update import get_external_ip
        assert get_external_ip() == '123.123.123.123'

    #  Handles network timeout when trying to reach ipecho.net
    def test_handles_network_timeout(self, mocker):
        mocker.patch('requests.get', side_effect=requests.Timeout)
        mock_log_message = mocker.patch('src.ddns_update.log_message')

        from src.ddns_update import get_external_ip
        assert get_external_ip() is None
        mock_log_message.assert_called_once_with("Failed to get external IP address: ")

    def test_live_response_real(self):
        from ddns_update import get_external_ip

        # Define a regex pattern for a valid IPv4 address
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

        # Get the external IP address
        ip = get_external_ip()

        # Check if the IP address matches the pattern
        assert ip and ip_pattern.match(ip)
