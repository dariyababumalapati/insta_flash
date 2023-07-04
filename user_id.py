from user_agents import parse

import hashlib

def generate_user_id(request):
    # Get the user agent string from request headers
    ua_string = request.headers.get('User-Agent')
    screen_resolution = request.form['screenResolution']
    user_agent = parse(ua_string)  # Parse user agent string
    user_ip = get_ip_address(request)
    cookies = request.cookies  # Get cookies from the request

    # Combine relevant data for uniqueness
    data_to_hash = ua_string + user_ip + str(user_agent.device) + str(user_agent.os) + screen_resolution

    # Include cookies in the data used for generating the user ID
    for key, value in cookies.items():
        data_to_hash += key + value

    # Generate unique hash for the user ID
    user_id = hashlib.md5(data_to_hash.encode()).hexdigest()

    return user_id

def get_ip_address(request):
    # Check if the X-Forwarded-For header is present
    if 'X-Forwarded-For' in request.headers:
        # Get a list of IP addresses in the X-Forwarded-For header
        ip_addresses = request.headers['X-Forwarded-For'].split(',')
        # The client's IP address will be the first address in the list
        client_ip = ip_addresses[0].strip()
    else:
        # Use the remote address if the X-Forwarded-For header is not present
        client_ip = request.remote_addr
    
    return client_ip

