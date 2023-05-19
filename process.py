import subprocess

class Process:

    @staticmethod
    def create():
        return Process(subprocess)

    @staticmethod
    def create_null():
        class NullSubprocess:
            def run(self, command):
                pass
        return Process(NullSubprocess())

    def __init__(self, subprocess):
        self.subprocess = subprocess

    def run(self, command):
        print("PROCESS =>")
        print(f"  command: {command}")
        self.subprocess.run(command)
