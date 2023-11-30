#!/bin/bash

# Connect to the remote server using SSH, disable strict host key checking, and set UserKnownHostsFile to /dev/null
ssh $VM_USERNAME@$VM_IP -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "cd /var/jenkins_home/jobs/ && find . -name 'config.xml' -print0 | xargs -0 zip -0 -r /tmp/config_files.zip"

# Copy the generated zip file from the remote server to the local machine using SCP
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $VM_USERNAME@$VM_IP:/tmp/config_files.zip config_files.zip && unzip -o config_files.zip -d config_files/