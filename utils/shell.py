import subprocess

class Shell:

    @staticmethod
    def execute_command(command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode()
        except subprocess.CalledProcessError as e:
            return str(e)
