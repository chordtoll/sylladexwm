import subprocess

def runProcess(process):
    print(f"Running: {process}")
    result=subprocess.Popen(process)

