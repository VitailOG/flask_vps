import paramiko

from contextlib import contextmanager

from config import REMOTE_FOLDER_PATH


class SFTPClient:

    def __init__(self, ip: str, user: str, password: str, run_bash_script: bool = True):
        self.ip = ip
        self.user = user
        self.password = password
        self.run_bash_script = run_bash_script
        self.ssh = paramiko.SSHClient()

    def get(self, filename: str, buffer):
        with self.get_connection() as sftp:
            sftp.getfo(REMOTE_FOLDER_PATH + filename, buffer)
            buffer.seek(0)
            return buffer

    def upload(self, filename: str, data):
        with self.get_connection() as sftp:
            sftp.putfo(data, REMOTE_FOLDER_PATH + filename)

            if self.run_bash_script:
                self.ssh.exec_command(f'./hooks/replication.sh {filename}')

    @contextmanager
    def get_connection(self):
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ip, username=self.user, password=self.password)
            with self.ssh.open_sftp() as sftp:
                yield sftp
        finally:
            self.ssh.close()
