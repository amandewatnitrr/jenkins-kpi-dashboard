import requests

def get_gitlab_version(url, username, password):
    # Disable SSL certificate verification (not recommended for production)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # Make a request to the GitLab API to fetch version details
    try:
        response = requests.get(
            f"{url.rstrip('/')}/version",
            auth=(username, password),
            timeout=10,
            verify=False  # Disable SSL verification
        )
        response.raise_for_status()
        gitlab_info = response.json()
    except requests.RequestException as e:
        # Handle the exception (e.g., log the error)
        print(f"Error retrieving GitLab version: {e}")
        return 'N/A'

    # Extract the GitLab version
    version = gitlab_info.get('version', 'N/A')
    return version

# Replace these values with your GitLab server URL, username, and password
gitlab_url = 'your_gitlab_url'
gitlab_username = 'your_username'
gitlab_password = 'your_password'

# Get GitLab version
gitlab_version = get_gitlab_version(gitlab_url, gitlab_username, gitlab_password)

# Print the GitLab version
print(f"GitLab version: {gitlab_version}")
