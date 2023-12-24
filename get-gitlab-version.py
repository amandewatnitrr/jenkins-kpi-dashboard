import requests

def get_gitlab_version(url, private_token):
    try:
        response = requests.get(
            f"{url.rstrip('/')}/api/v4/version",
            headers={'Private-Token': private_token},
            timeout=10
        )
        response.raise_for_status()
        gitlab_info = response.json()
    except requests.RequestException as e:
        print(f"Error retrieving GitLab version: {e}")
        return 'N/A'

    version = gitlab_info.get('version', 'N/A')
    return version

# Replace these values with your GitLab server URL and Private Access Token
gitlab_url = 'your_gitlab_url'
private_token = 'your_private_access_token'

# Get GitLab version
gitlab_version = get_gitlab_version(gitlab_url, private_token)

# Print the GitLab version
print(f"GitLab version: {gitlab_version}")
