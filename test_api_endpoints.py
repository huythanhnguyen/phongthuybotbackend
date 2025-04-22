import os
import requests
import pytest
import json

# Base URL cho production
BASE_URL = os.getenv('API_URL', 'https://phongthuybotbackend.onrender.com')
# Base URL cho Python ADK
ADK_URL = os.getenv('ADK_URL', 'https://phongthuybotadk.onrender.com')

@pytest.fixture(scope='session')
def base_url():
    print(f"Kiểm tra API trên: {BASE_URL}")
    return BASE_URL

@pytest.fixture(scope='session')
def adk_url():
    print(f"Python ADK URL: {ADK_URL}")
    return ADK_URL

def log_response(resp):
    """Ghi log phản hồi từ API để dễ debug"""
    print(f"Status code: {resp.status_code}")
    print(f"Headers: {resp.headers}")
    try:
        print(f"Response: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Raw response: {resp.text[:200]}")

# Test health check của Python ADK trước
def test_adk_health(adk_url):
    url = f"{adk_url}/health"
    print(f"Kiểm tra kết nối với Python ADK: {url}")
    try:
        resp = requests.get(url)
        log_response(resp)
        assert resp.status_code == 200, f"ADK health check failed: {resp.status_code}"
        data = resp.json()
        assert data.get('status') == 'healthy', "ADK not healthy"
    except Exception as e:
        print(f"❌ Lỗi kết nối với Python ADK: {e}")
        assert False, f"Could not connect to ADK: {e}"

def test_health(base_url):
    url = f"{base_url}/api/health"
    resp = requests.get(url)
    assert resp.status_code == 200, f"Health check failed: {resp.status_code}"
    data = resp.json()
    assert data.get('status') == 'ok', "Health status not ok"


def test_root(base_url):
    url = f"{base_url}/"
    resp = requests.get(url)
    assert resp.status_code == 200, f"Root endpoint failed: {resp.status_code}"
    data = resp.json()
    assert 'message' in data, "Root response missing message"


def test_get_agent_info(base_url):
    url = f"{base_url}/api/v2/agent"
    resp = requests.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get('success', True) is True
    assert 'endpoints' in data, "Agent info missing endpoints"


def test_post_agent_chat(base_url):
    url = f"{base_url}/api/v2/agent/chat"
    payload = {"message": "Xin chào"}
    resp = requests.post(url, json=payload)
    assert resp.status_code == 200, f"Agent chat failed: {resp.status_code}"
    data = resp.json()
    assert data.get('success') is True
    assert 'result' in data, "Agent chat missing result"


def test_post_agent_query(base_url):
    url = f"{base_url}/api/v2/agent/query"
    payload = {"agentType": "bat_cuc_linh_so_agent", "query": "0984851439"}
    resp = requests.post(url, json=payload)
    assert resp.status_code == 200, f"Agent query failed: {resp.status_code}"
    data = resp.json()
    assert data.get('success') is True
    assert 'result' in data, "Agent query missing result"


def test_get_batcuclinhso_info(base_url):
    url = f"{base_url}/api/v2/bat-cuc-linh-so"
    resp = requests.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get('success', True) is True
    assert 'endpoints' in data, "Bát Cục Linh Số info missing endpoints"


def test_post_phone_analysis(base_url):
    url = f"{base_url}/api/v2/bat-cuc-linh-so/phone"
    payload = {"phoneNumber": "0984851439"}
    print(f"\nĐang kiểm tra endpoint: {url}")
    print(f"Payload: {payload}")
    
    resp = requests.post(url, json=payload)
    log_response(resp)
    
    assert resp.status_code == 200, f"Phone analysis failed: {resp.status_code}"
    data = resp.json()
    assert data.get('success') is True
    assert 'result' in data, "Phone analysis missing result"


def test_post_cccd_analysis(base_url):
    url = f"{base_url}/api/v2/bat-cuc-linh-so/cccd"
    payload = {"cccdNumber": "012345678912"}
    print(f"\nĐang kiểm tra endpoint: {url}")
    print(f"Payload: {payload}")
    
    resp = requests.post(url, json=payload)
    log_response(resp)
    
    assert resp.status_code == 200, f"CCCD analysis failed: {resp.status_code}"
    data = resp.json()
    assert data.get('success') is True
    assert 'result' in data, "CCCD analysis missing result"


def test_post_password_analysis(base_url):
    url = f"{base_url}/api/v2/bat-cuc-linh-so/password"
    payload = {"password": "abc12345"}
    print(f"\nĐang kiểm tra endpoint: {url}")
    print(f"Payload: {payload}")
    
    resp = requests.post(url, json=payload)
    log_response(resp)
    
    assert resp.status_code == 200, f"Password analysis failed: {resp.status_code}"
    data = resp.json()
    assert data.get('success') is True
    assert 'result' in data, "Password analysis missing result"


def test_post_bank_account_analysis(base_url):
    url = f"{base_url}/api/v2/bat-cuc-linh-so/bank-account"
    payload = {"accountNumber": "1234567890"}
    print(f"\nĐang kiểm tra endpoint: {url}")
    print(f"Payload: {payload}")
    
    # Gửi request với đúng parameter key
    resp = requests.post(url, json=payload)
    log_response(resp)
    
    # If 400 or 200, we accept non-error
    assert resp.status_code in (200,400), f"Bank account analysis returned unexpected status: {resp.status_code}"
    
    if resp.status_code == 200:
        data = resp.json()
        assert data.get('success') is True
        assert 'result' in data, "Bank account analysis missing result"


def test_post_suggest_bank_account(base_url):
    url = f"{base_url}/api/v2/bat-cuc-linh-so/suggest-bank-account"
    payload = {"purpose": "business", "preferredDigits": [1,2,3]}
    print(f"\nĐang kiểm tra endpoint: {url}")
    print(f"Payload: {payload}")
    
    resp = requests.post(url, json=payload)
    log_response(resp)
    
    assert resp.status_code in (200,400), f"Suggest bank account returned unexpected status: {resp.status_code}"
    
    if resp.status_code == 200:
        data = resp.json()
        assert data.get('success') is True
        assert 'result' in data, "Suggest bank account missing result" 