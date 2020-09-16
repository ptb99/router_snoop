#! /usr/bin/python3

###
### wrapper for remote command pipe using paramiko
###

import paramiko


class RemoteExec:
    """Wrapper for an SSH connection reading output from a command"""
    def __init__(self, server, user='root'):
        self.server = server
        self.username = user
        self.connect()

    def __del__(self):
        if self.conn:
            self.conn.close()

    def connect(self):
        self.conn = paramiko.SSHClient()
        self.conn.load_system_host_keys()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #Loads the user's local known host file (done by default?)
        #path = os.path.expanduser(os.path.join("~", ".ssh", "known_hosts"))
        #self.conn.load_host_keys(path)

        #Connects to the local SSH agent and tries to obtain the private key
        self.conn.connect(self.server, username=self.username, allow_agent=True)

    def exec_command(self, command):
        """Return merged stdout/stderr a line at a time."""
        _, ss_stdout, _ = self.conn.exec_command(command)

        # grab SSH Channel object and set to merge stdout/stderr
        ss_stdout.channel.set_combine_stderr(True)

        # turn ourselves into an iterator over all lines in stdout/stderr
        for line in ss_stdout:
            yield line



## Alternate code using a select loop
# stdin, stdout, stderr = ssh.exec_command(command)
# # TODO() : if an error is thrown, stop further rules and revert back changes
# # Wait for the command to terminate
# while not stdout.channel.exit_status_ready():
#     # Only print data if there is data to read in the channel
#     if stdout.channel.recv_ready():
#         rl, wl, xl = select.select([ stdout.channel ], [ ], [ ], 0.0)
#         if len(rl) > 0:
#             tmp = stdout.channel.recv(1024)
#             output = tmp.decode()
#             print output


# def execute(cmd):
#     popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
#     	    		     stderr=subprocess.STDOUT, universal_newlines=True)
#     for stdout_line in iter(popen.stdout.readline, ""):
#         yield stdout_line 
#     popen.stdout.close()
#     return_code = popen.wait()
#     if return_code:
#         raise subprocess.CalledProcessError(return_code, cmd)

# # Example
# for path in execute(["locate", "a"]):
#     print(path, end="")


if __name__ == '__main__':

    host = '192.168.1.1'
    #cmd = 'ls -l /tmp'
    cmd = 'top -b -d 10'

    try:
        remote = RemoteExec(host)
        for line in remote.exec_command(cmd):
            print ("GOT: ", line.rstrip())
    except KeyboardInterrupt:
        print('')
