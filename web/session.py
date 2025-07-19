#!/usr/bin/env python3
"""
Session management for SINTA login and authentication

This module handles SINTA login using requests and manages session cookies.
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
from .config import config


class SintaRequestLogin:
    """Login functionality for SINTA using requests only"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': config.get_user_agent(),
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-Ch-Ua': '"Google Chrome";v="138", "Chromium";v="138", "Not:A-Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"'
        }
        self.session.headers.update(self.headers)
    
    def get_csrf_token(self, login_url):
        """Get CSRF token from login page"""
        try:
            print("🔍 Getting CSRF token from login page...")
            response = self.session.get(login_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Debug: Save login page for inspection
            print(f"🔍 Debug: Login page length = {len(response.text)} characters")
            
            # Look for CSRF token in meta tags
            csrf_meta = soup.find('meta', {'name': 'csrf-token'})
            if csrf_meta:
                token = csrf_meta.get('content')
                print(f"✅ Found CSRF token: {token[:20]}...")
                return token
            
            # Look for CSRF token in input fields
            csrf_input = soup.find('input', {'name': '_token'})
            if csrf_input:
                token = csrf_input.get('value')
                print(f"✅ Found CSRF token in input: {token[:20]}...")
                return token
            
            # Look for CSRF token in form
            csrf_form = soup.find('input', {'name': 'csrf_token'})
            if csrf_form:
                token = csrf_form.get('value')
                print(f"✅ Found CSRF token in form: {token[:20]}...")
                return token
            
            # Debug: Look for login form fields
            print("🔍 Debug: Looking for login form fields...")
            forms = soup.find_all('form')
            for i, form in enumerate(forms):
                print(f"   Form {i}: action={form.get('action')}")
                inputs = form.find_all('input')
                for inp in inputs:
                    print(f"     Input: name={inp.get('name')}, type={inp.get('type')}, value={inp.get('value', '')[:20]}...")
                
            print("⚠️ No CSRF token found, proceeding without it")
            return None
            
        except Exception as e:
            print(f"⚠️ Error getting CSRF token: {e}")
            return None
    
    def login(self, username, password):
        """Perform login to SINTA using requests"""
        try:
            session_config = config.get_session_config()
            login_page_url = session_config['login_url']
            
            print("🌐 Accessing SINTA login page...")
            
            # Get CSRF token and find correct form action
            response = self.session.get(login_page_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find login form and its action URL
            login_form = soup.find('form')
            if login_form:
                form_action = login_form.get('action')
                if form_action:
                    if form_action.startswith('http'):
                        login_url = form_action
                    else:
                        login_url = f"https://sinta.kemdikbud.go.id{form_action}"
                else:
                    login_url = login_page_url
            else:
                login_url = login_page_url
            
            # Get CSRF token (simplified version)
            csrf_token = self.get_csrf_token_simple(login_page_url)
            
            # Prepare login data
            login_data = {
                'username': username,
                'password': password
            }
            
            # Add CSRF token if found
            if csrf_token:
                login_data['_token'] = csrf_token
                self.session.headers['X-CSRF-TOKEN'] = csrf_token
            
            print("📝 Submitting login credentials...")
            
            # Update headers for POST request
            self.session.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://sinta.kemdikbud.go.id',
                'Referer': login_page_url
            })
            
            # Submit login form
            response = self.session.post(login_url, data=login_data, timeout=30, allow_redirects=True)
            
            # Check if login was successful
            if response.status_code == 200:
                # Check if we're redirected to dashboard or authors page
                if 'authors' in response.url or 'dashboard' in response.url or 'profile' in response.url:
                    print("✅ Login successful!")
                    return True
                elif 'login' in response.url:
                    print("❌ Login failed - redirected back to login page")
                    # Try to find error message
                    soup = BeautifulSoup(response.content, 'html.parser')
                    error_msg = soup.find('div', {'class': 'alert-danger'})
                    if error_msg:
                        print(f"   Error: {error_msg.get_text().strip()}")
                    return False
                else:
                    print("✅ Login successful!")
                    return True
            else:
                print(f"❌ Login failed with status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def get_csrf_token_simple(self, login_url):
        """Get CSRF token from login page (simplified)"""
        try:
            response = self.session.get(login_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for CSRF token in meta tags
            csrf_meta = soup.find('meta', {'name': 'csrf-token'})
            if csrf_meta:
                return csrf_meta.get('content')
            
            # Look for CSRF token in input fields
            csrf_input = soup.find('input', {'name': '_token'})
            if csrf_input:
                return csrf_input.get('value')
            
            return None
            
        except Exception as e:
            return None
    
    def get_session_data(self):
        """Extract cookies and session data"""
        try:
            cookies_dict = dict(self.session.cookies)
            return {
                'cookies': cookies_dict,
                'headers': dict(self.session.headers)
            }
        except Exception as e:
            print(f"❌ Error getting session data: {e}")
            return None
    
    def test_session(self):
        """Test if current session is valid"""
        try:
            session_config = config.get_session_config()
            test_url = session_config['test_url']
            
            response = self.session.get(test_url, timeout=10)
            
            if response.status_code == 200:
                # Check if we're not redirected to login
                if 'login' not in response.url:
                    return True
                else:
                    return False
            else:
                return False
                
        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False


class SessionManager:
    """Manage SINTA session (login and cookies)"""
    
    def __init__(self):
        self.session = requests.Session()
        self.cookies = {}
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': config.get_user_agent()
        }
        self.session.headers.update(self.headers)
    
    def initialize_session(self, force_new_login=False):
        """Initialize SINTA session using request-based login"""
        try:
            print("🚀 Initializing SINTA session with request-based login...")
            
            # Load environment variables
            load_dotenv()
            
            username = os.getenv('SINTA_USERNAME')
            password = os.getenv('SINTA_PASSWORD')
            
            if not username or not password:
                print("❌ SINTA credentials not found in .env file")
                print("💡 Create .env file with SINTA_USERNAME and SINTA_PASSWORD")
                return False
            
            # Get session config
            session_config = config.get_session_config()
            session_file = session_config['session_file']
            
            # Delete saved session if force new login
            if force_new_login and os.path.exists(session_file):
                os.remove(session_file)
                print("🗑️ Removed old session data")
            
            # Try to load existing session first
            if os.path.exists(session_file) and not force_new_login:
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    self.cookies = session_data['cookies']
                    self.session.cookies.update(self.cookies)
                    
                    # Test if session is still valid
                    if self.test_session():
                        print("✅ Using existing valid session")
                        return True
                    else:
                        print("⚠️ Existing session expired, creating new session...")
                except Exception as e:
                    print(f"⚠️ Error loading existing session: {e}")
            
            # Perform request-based login
            login_handler = SintaRequestLogin()
            if login_handler.login(username, password):
                session_data = login_handler.get_session_data()
                
                if session_data:
                    self.cookies = session_data['cookies']
                    self.session.cookies.update(self.cookies)
                    
                    # Save session data
                    os.makedirs(os.path.dirname(session_file), exist_ok=True)
                    with open(session_file, 'w') as f:
                        json.dump(session_data, f)
                    print("💾 Session data saved")
                    
                    print("✅ Session initialized successfully")
                    return True
                else:
                    print("❌ Failed to get session data")
                    return False
            else:
                print("❌ Failed to login")
                return False
                
        except Exception as e:
            print(f"❌ Error during login: {e}")
            return False
    
    def test_session(self):
        """Test if current session is valid"""
        try:
            print("🧪 Testing session validity...")
            
            # Get test URL from config
            session_config = config.get_session_config()
            test_url = session_config['test_url']
            
            response = self.session.get(test_url, timeout=10)
            
            if response.status_code == 200:
                # Check if we're not redirected to login
                if 'login' not in response.url:
                    print("✅ Session is valid")
                    return True
                else:
                    print("❌ Session invalid - redirected to login")
                    return False
            else:
                print(f"❌ Session invalid: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False


class LecturerManager:
    """Manage lecturer data from TXT file"""
    
    def __init__(self, config_file="dosen.txt"):
        # Get absolute path relative to project root
        if not os.path.isabs(config_file):
            current_dir = Path(__file__).parent  # web directory
            parent_dir = current_dir.parent      # project root
            self.config_file = parent_dir / config_file
        else:
            self.config_file = Path(config_file)
        self.lecturers = []
    
    def load_lecturers(self):
        """Load lecturers from TXT file (one ID per line)"""
        try:
            with open(str(self.config_file), 'r', encoding='utf-8') as file:
                lines = file.readlines()
                self.lecturers = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        try:
                            lecturer_id = int(line)
                            # Store only ID, name will be fetched when needed
                            self.lecturers.append((lecturer_id, None))
                        except ValueError:
                            print(f"⚠️ Skipping invalid ID: {line}")
                            continue
            print(f"✅ Loaded {len(self.lecturers)} lecturers from {self.config_file}")
            return True
        except Exception as e:
            print(f"❌ Error loading lecturers from {self.config_file}: {e}")
            return False
    
    def get_lecturers(self):
        """Get list of lecturers"""
        return self.lecturers
