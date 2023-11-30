import os
import csv
import logging
import asyncio
import xml.etree.ElementTree as ET
import aiohttp
import re
import subprocess

USERNAME = "*********"
PAT = "**********"
GITLAB_SERVER = "gitlab-something.something.com"
SEARCH_STRING = "@Library"

# Configure logging
logging.basicConfig(filename='jenkinsfile_fetch.log', level=logging.INFO)

# Asynchronous function to fetch URL
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

# Asynchronous function to extract GitLab URLs from a config file
async def extract_urls_from_config_file(config_file_path):
    urls = []
    tree = ET.parse(config_file_path)
    root = tree.getroot()
    for url in root.iter('url'):
        if url.text is not None and 'gitlab' in url.text:
            urls.append(url.text)
    return urls

# Asynchronous function to fetch the Jenkinsfile from a repository
async def fetch_jenkinsfile_from_repository(session, url, library_counts, jenkinsfile_log):
    project_path = url.split(":")[1] if ":" in url else url.split("//")[1]
    project_path = project_path.strip('.git').strip('/')

    try:
        branches_url = f"https://{GITLAB_SERVER}/api/v4/projects/{project_path.replace('/', '%2F')}/repository/branches"
        async with session.get(branches_url, headers={"PRIVATE-TOKEN": PAT}) as branches_response:
            if branches_response.status == 200:
                branches = [branch['name'] for branch in await branches_response.json()]
                
                # Prioritize 'master' branch, fallback to 'main' if not available
                target_branches = ['master', 'main']
                branch_to_fetch = next((branch for branch in target_branches if branch in branches), None)

                if branch_to_fetch:
                    jenkinsfile_url = f"https://{GITLAB_SERVER}/api/v4/projects/{project_path.replace('/', '%2F')}/repository/files/Jenkinsfile/raw?ref={branch_to_fetch}"
                    async with session.get(jenkinsfile_url, headers={"PRIVATE-TOKEN": PAT}) as response:
                        if response.status == 200:
                            content = await response.text()
                            lines = [line for line in content.split('\n') if SEARCH_STRING in line and not line.strip().startswith('//') and not line.strip().startswith('#')]
                            if lines:
                                for line in lines:
                                    libraries = re.findall(r"@Library\(\[(.*?)\]", line)
                                    for library in libraries:
                                        for lib in map(str.strip, library.split(',')):
                                            library_counts[lib] = library_counts.get(lib, 0) + 1
                                            # Log library usage by repository
                                            with open('libraries_by_repo.csv', 'a', newline='') as csvfile:
                                                csv_writer = csv.writer(csvfile)
                                                csv_writer.writerow([project_path, branch_to_fetch, lib])
                                            print(f"Repository: {project_path} (Branch: {branch_to_fetch}) -> {lib}")
                            else:
                                print(f"No match found in {project_path} (Branch: {branch_to_fetch})")
                        elif response.status == 404:
                            print(f"Jenkinsfile not found for {project_path} (Branch: {branch_to_fetch}). Status code: {response.status}")
                            # Log missing Jenkinsfile
                            jenkinsfile_log.error(f"Jenkinsfile not found for {project_path} (Branch: {branch_to_fetch}). Status code: {response.status}")
                        else:
                            print(f"Failed to retrieve Jenkinsfile for {project_path} (Branch: {branch_to_fetch}). Status code: {response.status}")
                            jenkinsfile_log.error(f"Failed to retrieve Jenkinsfile for {project_path} (Branch: {branch_to_fetch}). Status code: {response.status}")
                else:
                    print(f"Neither 'master' nor 'main' branch found for {project_path}")
                    jenkinsfile_log.error(f"Neither 'master' nor 'main' branch found for {project_path}")
            else:
                print(f"Failed to retrieve branches for {project_path}. Status code: {branches_response.status}")
                jenkinsfile_log.error(f"Failed to retrieve branches for {project_path}. Status code: {branches_response.status}")
    except aiohttp.ClientError as e:
        print(f"An error occurred for {project_path} (Branch: {branch_to_fetch}): {e}")
        jenkinsfile_log.error(f"An error occurred for {project_path} (Branch: {branch_to_fetch}): {e}")

async def main():

    base_path = r'C:\Users\USERNAME\configfiles_path...'
    all_urls = []
    library_counts = {}
    jenkinsfile_log = logging.getLogger('jenkinsfile_fetch')
    pipeline_count = 0 

    # Initialize CSV files
    with open('libraries_by_repo.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Repository', 'Branch', 'Library'])

    with open('library_counts.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Library', 'Count'])

    async with aiohttp.ClientSession() as session:

        subprocess.run(["C:\\Program Files\\Git\\bin\\bash.exe", "C:\\Users\\USERNAME\\shell_file_path..\\zip-and-download.sh"])

        tasks = []
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file == 'config.xml':
                    config_file_path = os.path.join(root, file)
                    urls = await extract_urls_from_config_file(config_file_path)
                    all_urls.extend(urls)

        for url in all_urls:
            task = fetch_jenkinsfile_from_repository(session, url, library_counts, jenkinsfile_log)
            tasks.append(task)

        await asyncio.gather(*tasks)

        # Write library counts to CSV
        with open('library_counts.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Library', 'Count'])
            for library, count in library_counts.items():
                csv_writer.writerow([library, count])

        print("Library counts:")
        for library, count in library_counts.items():
            print(f"{library}: {count}")

if __name__ == '__main__':
    asyncio.run(main())