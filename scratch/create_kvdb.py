import urllib.request
import urllib.parse
import json
import time
import re
import uuid

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

def make_request(url, data=None, method=None, extra_headers=None):
    headers = HEADERS.copy()
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    return urllib.request.urlopen(req)

def main():
    print("1. Fetching available domains from mail.tm...")
    try:
        res = make_request('https://api.mail.tm/domains')
        domains_data = json.loads(res.read().decode())
        domain = domains_data['hydra:member'][0]['domain']
        print(f"Selected Domain: {domain}")
    except Exception as e:
        print(f"Failed to fetch domains: {e}")
        return

    random_id = str(uuid.uuid4())[:8]
    email_address = f"dmcashield_{random_id}@{domain}"
    password = f"Pass_{random_id}_123"
    print(f"Creating account: {email_address} ...")

    create_data = json.dumps({'address': email_address, 'password': password}).encode()
    try:
        make_request('https://api.mail.tm/accounts', data=create_data, method='POST')
        print("Account created successfully!")
    except Exception as e:
        print(f"Failed to create account: {e}")
        return

    print("Getting token...")
    try:
        token_res = make_request('https://api.mail.tm/token', data=create_data, method='POST')
        token_data = json.loads(token_res.read().decode())
        token = token_data['token']
        print("Token obtained successfully!")
    except Exception as e:
        print(f"Failed to get token: {e}")
        return

    print("\n2. POSTing to kvdb.io to create a bucket...")
    kvdb_data = urllib.parse.urlencode({'email': email_address}).encode()
    try:
        res = make_request(
            'https://kvdb.io', 
            data=kvdb_data, 
            extra_headers={'Content-Type': 'application/x-www-form-urlencoded'},
            method='POST'
        )
        bucket_id = res.read().decode().strip()
        print(f"Bucket created! Bucket ID: {bucket_id}")
    except Exception as e:
        print(f"Failed to create bucket: {e}")
        return

    print("\n3. Waiting for kvdb.io confirmation email...")
    body = None
    for attempt in range(1, 13):
        print(f"Polling inbox... Attempt {attempt}/12")
        try:
            list_res = make_request(
                'https://api.mail.tm/messages',
                extra_headers={'Authorization': f'Bearer {token}'}
            )
            messages_data = json.loads(list_res.read().decode())
            messages = messages_data.get('hydra:member', [])
        except Exception as e:
            print(f"Inbox poll failed: {e}")
            messages = []
        
        if messages:
            print(f"Found {len(messages)} messages!")
            for msg in messages:
                if "kvdb.io" in msg["from"]["address"].lower() or "kvdb" in msg["subject"].lower():
                    msg_id = msg["id"]
                    print(f"Reading message {msg_id}...")
                    try:
                        read_res = make_request(
                            f"https://api.mail.tm/messages/{msg_id}",
                            extra_headers={'Authorization': f'Bearer {token}'}
                        )
                        msg_detail = json.loads(read_res.read().decode())
                        # Check html or text content
                        body = msg_detail.get('text', msg_detail.get('html', ''))
                        break
                    except Exception as e:
                        print(f"Failed to read message: {e}")
            if body:
                break
        time.sleep(5)
        
    if not body:
        print("Failed to receive email.")
        return
        
    print("\n--- FULL EMAIL BODY ---")
    print(body)
    print("-----------------------")

if __name__ == "__main__":
    main()
