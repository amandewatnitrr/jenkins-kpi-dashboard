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
async def extract_gitlab_urls(session, config_file):
    url_list = []
    for line in config_file:
        if SEARCH_STRING in line:
            gitlab_url = line.split("'")[1]
            url_list.append(gitlab_url)
    return url_list

# Asynchronous function to check if the Jenkinsfile is used for an Active pipeline on Jenkins
async def check_active_pipeline(session, jenkinsfile_url):
    active_pipeline = False
    pipeline_info = await fetch_url(session, jenkinsfile_url)
    if pipeline_info.startswith("<?xml version"): # Check if the Jenkinsfile is used for an Active pipeline
        pipeline_info_tree = ET.ElementTree(ET.fromstring(pipeline_info))
        for build in pipeline_info_tree.findall(".//build"):
            if build.get("building") == "true":
                active_pipeline = True
                break
    return active_pipeline

# Asynchronous function to fetch the Jenkinsfile from GitLab
async def fetch_jenkinsfile(session, gitlab_url):
    response = await fetch_url(session, gitlab_url)
    response_tree = ET.ElementTree(ET.fromstring(response))
    for file in response_tree.findall(".//file"):
        if file.get("name") == "Jenkinsfile":
            return file.get("content")

# Asynchronous function to check the Jenkinsfile usage in all Active pipelines
async def main():
    async with aiohttp.ClientSession() as session:
        # Replace with the actual config file
        with open("config_file.txt", "r") as config_file:
            gitlab_urls = await extract_gitlab_urls(session, config_file)
            for gitlab_url in gitlab_urls:
                jenkinsfile_url = f"{GITLAB_SERVER}/api/v4/projects/{gitlab_url.split('/')[-1]}/repository/files/Jenkinsfile/raw"
                active_pipeline = await check_active_pipeline(session, jenkinsfile_url)
                if active_pipeline:
                    jenkinsfile_content = await fetch_jenkinsfile(session, gitlab_url)
                    # Do something with the Jenkinsfile content, e.g., write it to a file
                    with open(f"jenkinsfile_{gitlab_url.split('/')[-1]}.txt", "w") as jenkinsfile:
                        jenkinsfile.write(jenkinsfile_content)
                    logging.info(f"Fetched Jenkinsfile from {gitlab_url} with Active pipeline")
                else:
                    logging.info(f"Jenkinsfile from {gitlab_url} is not used for an Active pipeline")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())