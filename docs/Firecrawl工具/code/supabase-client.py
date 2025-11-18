"""
Supabase Client for Flask Application

This module provides a Supabase client instance for Flask applications
with session storage support.
"""

import os
from flask import g
from werkzeug.local import LocalProxy
from supabase.client import Client, ClientOptions
from flask_storage import FlaskSessionStorage

# Get Supabase configuration from environment variables
url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")


def get_supabase() -> Client:
    """
    Get or create Supabase client instance.

    This function creates a Supabase client instance and stores it in Flask's
    application context (g) to ensure it's reused across requests.

    Returns:
        Client: Supabase client instance
    """
    if "supabase" not in g:
        g.supabase = Client(
            url,
            key,
            options=ClientOptions(storage=FlaskSessionStorage(), flow_type="pkce"),
        )
    return g.supabase


# Create a LocalProxy for easy access to Supabase client
supabase: Client = LocalProxy(get_supabase)
