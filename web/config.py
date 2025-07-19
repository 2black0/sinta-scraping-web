#!/usr/bin/env python3
"""
Configuration management for SINTA Scraping Application

This module handles all configuration settings and provides a centralized
way to manage application configuration.
"""


class ConfigManager:
    """Manage application configuration with default values"""
    
    def __init__(self):
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """Load default configuration"""
        self._load_default_config()
    
    def _load_default_config(self):
        """Load default configuration"""
        self.config = {
            'session': {
                'test_url': 'https://sinta.kemdikbud.go.id/authors',
                'login_url': 'https://sinta.kemdikbud.go.id/logins',
                'session_file': '.config/session_data.json'
            },
            'scraping': {
                'request_delay': 1,
                'max_retries': 3,
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
            },
            'output': {
                'directory_format': 'output-{date}',
                'date_format': '%d%m%Y',
                'csv_encoding': 'utf-8'
            },
            'lecturers': {
                'config_file': 'dosen.txt'
            },
            'logging': {
                'level': 'INFO',
                'show_emoji': True
            }
        }
    
    def get(self, key_path, default=None):
        """Get configuration value by dot notation (e.g., 'session.test_url')"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_session_config(self) -> dict:
        """Get session configuration"""
        return {
            'test_url': str(self.get('session.test_url', 'https://sinta.kemdikbud.go.id/authors')),
            'login_url': str(self.get('session.login_url', 'https://sinta.kemdikbud.go.id/logins')),
            'session_file': str(self.get('session.session_file', '.config/session_data.json'))
        }
    
    def get_user_agent(self) -> str:
        """Get User Agent from config"""
        user_agent = self.get('scraping.user_agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36')
        return str(user_agent) if user_agent is not None else 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'


# Global config instance
config = ConfigManager()
