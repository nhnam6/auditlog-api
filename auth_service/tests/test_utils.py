"""Test utility functions"""

import os
import sys
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import jwt
import pytest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import create_access_token, hash_password, verify_password, verify_token


class TestPasswordFunctions:
    """Test password hashing and verification functions"""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        password = "testpassword123"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password

    def test_hash_password_different_salts(self):
        """Test that same password produces different hashes (due to salt)"""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2

    def test_verify_password_correct_password(self):
        """Test password verification with correct password"""
        password = "testpassword123"
        hashed = hash_password(password)

        result = verify_password(password, hashed)
        assert result is True

    def test_verify_password_incorrect_password(self):
        """Test password verification with incorrect password"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)

        result = verify_password(wrong_password, hashed)
        assert result is False

    def test_verify_password_empty_password(self):
        """Test password verification with empty password"""
        password = "testpassword123"
        hashed = hash_password(password)

        result = verify_password("", hashed)
        assert result is False

    def test_verify_password_bytes_input(self):
        """Test password verification with bytes input"""
        password = "testpassword123"
        hashed = hash_password(password)

        # Test with bytes hash
        result = verify_password(password, hashed.encode("utf-8"))
        assert result is True

    def test_verify_password_special_characters(self):
        """Test password verification with special characters"""
        password = "test@#$%^&*()_+{}|:<>?[]\\;'\",./<>?"
        hashed = hash_password(password)

        result = verify_password(password, hashed)
        assert result is True

    def test_verify_password_unicode(self):
        """Test password verification with unicode characters"""
        password = "test密码123"
        hashed = hash_password(password)

        result = verify_password(password, hashed)
        assert result is True

    def test_hash_password_empty_string(self):
        """Test hashing empty password"""
        password = ""
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_very_long_password(self):
        """Test password verification with very long password"""
        password = "a" * 1000
        hashed = hash_password(password)

        result = verify_password(password, hashed)
        assert result is True


class TestTokenFunctions:
    """Test JWT token functions"""

    def setup_method(self):
        """Setup method for each test"""
        self.test_data = {
            "sub": "test@example.com",
            "tenant_id": "test-tenant",
            "role": "user",
        }

    @patch("utils.settings")
    def test_create_access_token_default_expiry(self, mock_settings):
        """Test create_access_token with default expiry"""
        mock_settings.JWT_SECRET = "test-secret"
        mock_settings.JWT_ALGORITHM = "HS256"
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 60

        token = create_access_token(self.test_data)

        assert isinstance(token, str)
        assert len(token) > 0

        # Decode token to verify content
        decoded = jwt.decode(
            token,
            mock_settings.JWT_SECRET,
            algorithms=[
                mock_settings.JWT_ALGORITHM,
            ],
        )
        assert decoded["sub"] == self.test_data["sub"]
        assert decoded["tenant_id"] == self.test_data["tenant_id"]
        assert decoded["role"] == self.test_data["role"]
        assert "exp" in decoded

    @patch("utils.settings")
    def test_create_access_token_custom_expiry(self, mock_settings):
        """Test create_access_token with custom expiry"""
        mock_settings.JWT_SECRET = "test-secret"
        mock_settings.JWT_ALGORITHM = "HS256"

        custom_expiry = timedelta(minutes=30)
        token = create_access_token(
            self.test_data,
            expires_delta=custom_expiry,
        )

        assert isinstance(token, str)
        assert len(token) > 0

        # Decode token to verify expiry
        decoded = jwt.decode(
            token,
            mock_settings.JWT_SECRET,
            algorithms=[
                mock_settings.JWT_ALGORITHM,
            ],
        )
        exp_timestamp = decoded["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

        # Check that expiry is approximately 30 minutes from now
        now = datetime.now(timezone.utc)
        time_diff = exp_datetime - now

        assert 29 <= time_diff.total_seconds() / 60 <= 31

    @patch("utils.settings")
    def test_create_access_token_empty_data(self, mock_settings):
        """Test create_access_token with empty data"""
        mock_settings.JWT_SECRET = "test-secret"
        mock_settings.JWT_ALGORITHM = "HS256"
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 60

        token = create_access_token({})

        assert isinstance(token, str)
        assert len(token) > 0

    @patch("utils.settings")
    def test_verify_token_valid_token(self, mock_settings):
        """Test verify_token with valid token"""
        mock_settings.JWT_SECRET = "test-secret"
        mock_settings.JWT_ALGORITHM = "HS256"
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 60

        # Create a token
        token = create_access_token(self.test_data)

        # Verify the token
        payload = verify_token(token)

        assert payload["sub"] == self.test_data["sub"]
        assert payload["tenant_id"] == self.test_data["tenant_id"]
        assert payload["role"] == self.test_data["role"]

    @patch("utils.settings")
    def test_verify_token_expired_token(self, mock_settings):
        """Test verify_token with expired token"""
        mock_settings.JWT_SECRET = "test-secret"
        mock_settings.JWT_ALGORITHM = "HS256"

        # Create a token with very short expiry
        token = create_access_token(
            self.test_data,
            expires_delta=timedelta(seconds=-1),
        )

        with pytest.raises(ValueError, match="Invalid token"):
            verify_token(token)

    @patch("utils.settings")
    def test_create_access_token_with_complex_data(self, mock_settings):
        """Test create_access_token with complex data structure"""
        mock_settings.JWT_SECRET = "test-secret"
        mock_settings.JWT_ALGORITHM = "HS256"
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 60

        complex_data = {
            "sub": "test@example.com",
            "tenant_id": "test-tenant",
            "role": "admin",
            "permissions": ["read", "write", "delete"],
            "metadata": {
                "created_at": "2023-01-01T00:00:00Z",
                "version": "1.0",
            },
        }

        token = create_access_token(complex_data)

        assert isinstance(token, str)
        assert len(token) > 0

        # Decode token to verify content
        decoded = jwt.decode(
            token,
            mock_settings.JWT_SECRET,
            algorithms=[mock_settings.JWT_ALGORITHM],
        )
        assert decoded["sub"] == complex_data["sub"]
        assert decoded["tenant_id"] == complex_data["tenant_id"]
        assert decoded["role"] == complex_data["role"]
        assert decoded["permissions"] == complex_data["permissions"]
        assert decoded["metadata"] == complex_data["metadata"]
