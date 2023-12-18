import os
import csv
import logging
import asyncio
import json
import xml.etree.ElementTree as ET
import aiohttp
import re
import subprocess
import time

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
        print(f"No match found for URL: {url}")
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

                # Prioritize 'master' branch, fallback to 'main' if not available
                target_branches = ['master', 'main']
                branch_to_fetch = next((branch for branch in target_branches if branch in branches), None)

                if branch_to_fetch:
                    jenkinsfile_url = f"https://{GITLAB_SERVER}/api/v4/projects/{project_path.replace('/', '%2F')}/repository/files/Jenkinsfile/raw?ref={branch_to_fetch}"
                    async with session.get(jenkinsfile_url, headers={"PRIVATE-TOKEN": PAT}) as response:
                        if response.status == 200:
                            content = await response.text()

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
                                                csv_writer.writerow([project_path, branch_to_fetch, lib, dsl_name, enable_stages])
                                            print(f"Repository: {project_path} (Branch: {branch_to_fetch}) -> {lib}")

                                total_pipelines.add(project_path)
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

        end_time = time.time()  # Record end time for this operation
        elapsed_time = end_time - start_time
        print(f"Time taken for {project_path}: {elapsed_time} seconds")

    except aiohttp.ClientError as e:
        print(f"An error occurred for {project_path} (Branch: {branch_to_fetch}): {e}")
        jenkinsfile_log.error(f"An error occurred for {project_path} (Branch: {branch_to_fetch}): {e}")



async def fetch_jenkins_server_details(session, jenkins_server_url, jenkins_server_log):
    try:
        start_time = time.time()  # Record start time for this operation

        # Example API endpoint to get Jenkins server details
        jenkins_info_url = f"{jenkins_server_url}/api/json"
        async with session.get(jenkins_info_url) as response:
            if response.status == 200:
                jenkins_info = await response.json()
                # Process Jenkins server details as needed
                print("Jenkins Server Details:", jenkins_info)
            else:
                print(f"Failed to retrieve Jenkins server details. Status code: {response.status}")
                jenkins_server_log.error(f"Failed to retrieve Jenkins server details. Status code: {response.status}")

        end_time = time.time()  # Record end time for this operation
        elapsed_time = end_time - start_time
        print(f"Time taken to fetch Jenkins server details: {elapsed_time} seconds")

    except aiohttp.ClientError as e:
        print(f"An error occurred while fetching Jenkins server details: {e}")
        jenkins_server_log.error(f"An error occurred while fetching Jenkins server details: {e}")



async def fetch_pipeline_details(session, jenkins_server_url, job_name, pipeline_log):
    try:
        start_time = time.time()  # Record start time for this operation

        # Example API endpoint to get pipeline details for a specific job
        job_info_url = f"{jenkins_server_url}/job/{job_name}/api/json"
        async with session.get(job_info_url) as response:
            if response.status == 200:
                job_info = await response.json()
                # Process pipeline details as needed
                print(f"Pipeline Details for {job_name}:", job_info)
            else:
                print(f"Failed to retrieve pipeline details for {job_name}. Status code: {response.status}")
                pipeline_log.error(f"Failed to retrieve pipeline details for {job_name}. Status code: {response.status}")

        end_time = time.time()  # Record end time for this operation
        elapsed_time = end_time - start_time
        print(f"Time taken to fetch pipeline details for {job_name}: {elapsed_time} seconds")

    except aiohttp.ClientError as e:
        print(f"An error occurred while fetching pipeline details for {job_name}: {e}")
        pipeline_log.error(f"An error occurred while fetching pipeline details for {job_name}: {e}")

async def main():

    base_path = r'C:\Users\223072287\tech\common-pipeline-lib\config_files\Auto_Deployment'
    all_urls = []
    library_counts = {}
    jenkinsfile_log = logging.getLogger('jenkinsfile_fetch')
    total_pipelines = set()
    processed_repositories = set()

    # Initialize CSV files
    with open('libraries_by_repo.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Repository', 'Branch', 'Library','dsl_name','enable_stages'])

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
                    urls = await extract_urls_from_config_file(config_file_path)
                    all_urls.extend(urls)

        for url in all_urls:
            task = fetch_jenkinsfile_from_repository(session, url, library_counts, jenkinsfile_log, total_pipelines,processed_repositories)
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
