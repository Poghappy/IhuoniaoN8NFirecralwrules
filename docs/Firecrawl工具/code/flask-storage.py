"""
Flask Session Storage for Supabase Client

This module provides Flask session storage implementation for Supabase client.
"""

from typing import Any, Dict, Optional
from flask import session


class FlaskSessionStorage:
    """
    Flask session storage adapter for Supabase client.

    This class implements the storage interface required by Supabase client
    to store session data in Flask's session object.
    """

    def get(self, key: str) -> Optional[str]:
        """
        Get a value from storage.

        Args:
            key: The storage key

        Returns:
            The stored value or None if not found
        """
        return session.get(key)

    def set(self, key: str, value: str) -> None:
        """
        Set a value in storage.

        Args:
            key: The storage key
            value: The value to store
        """
        session[key] = value

    def remove(self, key: str) -> None:
        """
        Remove a value from storage.

        Args:
            key: The storage key to remove
        """
        session.pop(key, None)
