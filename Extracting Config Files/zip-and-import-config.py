import os
import paramiko
import tarfile

def zip_and_download_jobs(host, port, username, password, remote_path, local_path):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Create a temporary compressed archive on the remote server
    remote_archive_path = f"{remote_path.rstrip('/')}_archive.tar.gz"
    local_archive_path = os.path.join(local_path, "jobs_archive.tar.gz")

    with sftp.file(remote_archive_path, 'wb') as remote_archive:
        # Use tar to create a compressed archive of the jobs folder
        command = f"tar czf - -C {remote_path} jobs"
        stdin, stdout, stderr = sftp.exec_command(command)
        remote_archive.write(stdout.read())

    # Download the compressed archive to the local system
    sftp.get(remote_archive_path, local_archive_path)

    # Cleanup: Remove the temporary compressed archive on the remote server
    sftp.remove(remote_archive_path)

    sftp.close()
    transport.close()

# Replace these values with your actual credentials and paths
remote_ip = 'XX.XX.XX.XX'
remote_port = 22
remote_path = "/home/jenkins/CORELOAD-INBLRJENKINS01/jenkins_home"
local_path = r"C:\Users\YourUsername\Documents"
username = 'your_username'
password = 'your_password'

zip_and_download_jobs(remote_ip, remote_port, username, password, remote_path, local_path)
