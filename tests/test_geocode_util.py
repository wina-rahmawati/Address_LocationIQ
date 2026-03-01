import requests
    
import pytest
from unittest.mock import patch, MagicMock
import os

def get_coordinates(address: str, api_key: str):
    """
    Calls LocationIQ API to get full address, lat, and lon.
    """
    if not address or not isinstance(address, str):
        return None

    url = "https://us1.locationiq.com/v1/search"
    params = {
        "key": api_key,
        "q": address,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        
        # Handle cases like "Unauthorized" (401) or "Rate Limit" (429)
        if response.status_code != 200:
            return None

        data = response.json()
        if not data:
            return None

        top_result = data[0]
        return {
            "full_address": top_result.get("display_name"),
            "latitude": float(top_result.get("lat")),
            "longitude": float(top_result.get("lon"))
        }

    except (requests.exceptions.RequestException, ValueError, KeyError):
        # If the API is down or data is weird, return None so the ETL doesn't crash
        return None


@patch('requests.get')
def test_get_coordinates_success(mock_get):
    """Test when the API works perfectly"""
    # 1. Arrange: Fake a successful API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{
        "display_name": "123 Main St, New York",
        "lat": "40.71",
        "lon": "-74.00"
    }]
    mock_get.return_value = mock_response

    # 2. Act
    result = get_coordinates("123 Main St", "fake_key")

    # 3. Assert
    assert result["latitude"] == 40.71
    assert "New York" in result["full_address"]

@patch('requests.get')
def test_get_coordinates_not_found(mock_get):
    """Test when the API finds nothing (Address doesn't exist)"""
    mock_response = MagicMock()
    mock_response.status_code = 404 # Not Found
    mock_get.return_value = mock_response

    result = get_coordinates("Gibberish Address 999999", "fake_key")
    
    assert result is None

@patch('requests.get')
def test_get_coordinates_api_timeout(mock_get):
    """Test when the internet is down"""
    # Simulate a network timeout error
    import requests
    mock_get.side_effect = requests.exceptions.Timeout

    result = get_coordinates("Sydney", "fake_key")
    
    assert result is None