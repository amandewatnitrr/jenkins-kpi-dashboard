import logging
import asyncio
import aiohttp
import csv
import json
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET

USERNAME = "USERNAME"
PAT = "PAT"
GITLAB_SERVER = "GITLAB_SERVER"
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
async def fetch_jenkinsfile_from_repository(session, url, library_counts, jenkinsfile_log, total_pipelines, processed_repositories):
    match = re.search(r"(?<=gitlab-gxp.cloud.health.ge.com:)(.*?)(?=\.git|$)", url)
    if match:
        project_path = match.group(0).strip()
    else:
        logging.warning(f"No match found for URL: {url}")
        return

    if project_path in processed_repositories:
        return  # Skip processing if the repository has already been processed

    processed_repositories.add(project_path)

    try:
        start_time = time.time()  # Record start time for this operation

        branches_url = f"https://{GITLAB_SERVER}/api/v4/projects/{project_path.replace('/', '%2F')}/repository/branches"
        async with session.get(branches_url, headers={"PRIVATE-TOKEN": PAT}) as branches_response:
            if branches_response.status == 200:
                branches = [branch['name'] for branch in await branches_response.json()]
                for branch in branches:
                    jenkinsfile_url = f"https://{GITLAB_SERVER}/api/v4/projects/{project_path.replace('/', '%2F')}/repository/files/Jenkinsfile/raw?ref={branch}"
                    async with session.get(jenkinsfile_url, headers={"PRIVATE-TOKEN": PAT}) as response:
                        if response.status == 200:
                            content = await response.text(encoding='latin-1')

                            # Extract dsl_name
                            dsl_name_match = re.search(r"(\w+)\s*{", content)
                            dsl_name = dsl_name_match.group(1).strip() if dsl_name_match else ''

                            # Extract enable_stages
                            enable_stages_match = re.search(r"enable_stages\s*=\s*\[\s*(.*?)\s*\]", content, re.DOTALL)
                            enable_stages = enable_stages_match.group(1).strip() if enable_stages_match else ''

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
                                                csv_writer.writerow([project_path, branch, lib, dsl_name, enable_stages])
                                            print(f"Repository: {project_path} (Branch: {branch}) -> {lib}, DSL Name: {dsl_name}, Enable Stages: {enable_stages}")

                                total_pipelines.add((project_path, branch))
                            else:
                                print(f"No match found in {project_path} (Branch: {branch})")
                        elif response.status == 404:
                            print(f"Jenkinsfile not found for {project_path} (Branch: {branch}). Status code: {response.status}")

                            # Log missing Jenkinsfile
                            jenkinsfile_log.error(f"Jenkinsfile not found for {project_path} (Branch: {branch}). Status code: {response.status}")
                        else:
                            print(f"Failed to retrieve Jenkinsfile for {project_path} (Branch: {branch}). Status code: {response.status}")

                            jenkinsfile_log.error(f"Failed to retrieve Jenkinsfile for {project_path} (Branch: {branch}). Status code: {response.status}")
            else:
                print(f"Failed to retrieve branches for {project_path}. Status code: {branches_response.status}")

                jenkinsfile_log.error(f"Failed to retrieve branches for {project_path}. Status code: {branches_response.status}")

        end_time = time.time()  # Record end time for this operation
        elapsed_time = end_time - start_time
        print(f"Time taken for {project_path}: {elapsed_time} seconds")
    except aiohttp.ClientError as e:
        print(f"An error occurred for {project_path} (Branch: {branch}): {e}")
        jenkinsfile_log.error(f"An error occurred for {project_path} (Branch: {branch}): {e}")


async def main():
    base_path = r'C:\Users\223072287\tech\common-pipeline-lib\config_files'
    all_urls = []
    library_counts = {}
    jenkinsfile_log = logging.getLogger('jenkinsfile_fetch')
    total_pipelines = set()
    processed_repositories = set()

    # Initialize CSV files
    with open('libraries_by_repo.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Repository', 'Branch', 'Library', 'dsl_name', 'enable_stages'])

    with open('library_counts.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Library', 'Count'])

    async with aiohttp.ClientSession() as session:
        subprocess.run(["C:\\Program Files\\Git\\bin\\bash.exe", "C:\\Users\\223072287\\tech\\common-pipeline-lib\\config-extraction\\zip_and_download.sh"])

        tasks = []
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file == 'config.xml':
                    config_file_path = os.path.join(root, file)

                    # Check if the file exists before processing
                    if not os.path.exists(config_file_path):
                        logging.warning(f"File not found: {config_file_path}")
                        continue

                    urls = await extract_urls_from_config_file(config_file_path)
                    all_urls.extend(urls)

        for url in all_urls:
            task = fetch_jenkinsfile_from_repository(session, url, library_counts, jenkinsfile_log, total_pipelines, processed_repositories)
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

        print(f"Total pipelines: {len(total_pipelines)}")

        # Generate JSON files
        with open('libraries_by_repo.json', 'w') as jsonfile:
            json.dump(list(csv.reader(open('libraries_by_repo.csv'))), jsonfile, indent=2)

        with open('library_counts.json', 'w') as jsonfile:
            json.dump(library_counts, jsonfile, indent=2)

if __name__ == '__main__':
    asyncio.run(main())

    
    '''
    async def fetch_jenkinsfile_from_repository(session, url, library_counts, jenkinsfile_log, total_pipelines, processed_repositories, active_jenkinsfiles):
    # ...

    if lines:
        for line in lines:
            # ...

            active_pipelines_url = f"https://{GITLAB_SERVER}/api/v4/projects/{project_path.replace('/', '%2F')}/pipelines?ref={branch}&status=running"
            async with session.get(active_pipelines_url, headers={"PRIVATE-TOKEN": PAT}) as active_pipelines_response:
                if active_pipelines_response.status == 200:
                    active_pipelines = await active_pipelines_response.json()
                    if active_pipelines:
                        active_jenkinsfiles.add((project_path, branch))
                        print(f"Active pipeline found for {project_path} (Branch: {branch})")
                    else:
                        print(f"No active pipeline found for {project_path} (Branch: {branch})")
                else:
                    print(f"Failed to retrieve active pipelines for {project_path} (Branch: {branch}). Status code: {active_pipelines_response.status}")

                    jenkinsfile_log.error(f"Failed to retrieve active pipelines for {project_path} (Branch: {branch}). Status code: {active_pipelines_response.status}")

            # ...
    '''