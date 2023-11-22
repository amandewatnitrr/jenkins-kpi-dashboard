import os
import zipfile
import paramiko

def zip_and_download(remote_ip, remote_path, local_path):
    # Connect to the remote server using SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Replace 'username' and 'password' with your actual credentials
    ssh.connect(remote_ip, username='username', password='password')

    try:
        # Create a temporary zip file on the remote server
        zip_filename = '/tmp/jobs.zip'
        ssh.exec_command(f'cd {remote_path} && zip -r {zip_filename} jobs')

        # Download the zip file
        transport = paramiko.Transport((remote_ip, 22))
        transport.connect(username='username', password='password')
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(zip_filename, os.path.join(local_path, 'jobs.zip'))
        sftp.close()

    finally:
        # Close the SSH connection
        ssh.close()

# Example usage
remote_ip = 'XX.XX.XX.XX'
remote_path = '/home/jenkins/CORELOAD-INBLRJENKINS01/jenkins_home/'
local_path = 'C:/Users/YourUsername/Documents/'

zip_and_download(remote_ip, remote_path, local_path)