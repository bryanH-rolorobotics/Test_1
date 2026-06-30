import subprocess

branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
commit_count = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], text=True).strip()

print(f"Current branch: {branch}")
print(f"Total commits: {commit_count}")
