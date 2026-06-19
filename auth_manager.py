import subprocess
import os
import time

def main():
    link_file = "/root/auth_link.txt"
    code_file = "/root/auth_code.txt"
    result_file = "/root/auth_result.txt"

    # Clean up any old files
    for f in [link_file, code_file, result_file]:
        if os.path.exists(f):
            os.remove(f)

    print("Starting gcloud auth process...")
    proc = subprocess.Popen(
        ["gcloud", "auth", "application-default", "login", "--no-launch-browser"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Read stdout line by line to capture the URL
    url = None
    output_lines = []
    
    # We will read until we find the URL and the code prompt
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        output_lines.append(line)
        print("GCLOUD:", line.strip())
        if "https://" in line:
            parts = line.split()
            for p in parts:
                if p.startswith("https://"):
                    url = p
        if "Enter authorization code:" in line or "verification code" in line:
            break

    if not url:
        with open(result_file, "w") as f:
            f.write("ERROR: Could not find authentication URL in gcloud output.\n" + "".join(output_lines))
        return

    # Write the URL so the agent can display it to the user
    with open(link_file, "w") as f:
        f.write(url)
    print(f"URL found and written to {link_file}: {url}")

    # Now wait for the code_file to be created
    print("Waiting for verification code from agent...")
    start_time = time.time()
    code = None
    while time.time() - start_time < 300: # 5 minute timeout
        if os.path.exists(code_file):
            time.sleep(0.5) # small pause to ensure file is fully written
            with open(code_file, "r") as f:
                code = f.read().strip()
            break
        time.sleep(1)

    if not code:
        with open(result_file, "w") as f:
            f.write("ERROR: Timeout waiting for verification code from user.")
        proc.terminate()
        return

    print(f"Verification code received: {code[:4]}... Sending to gcloud.")
    # Send code to gcloud process
    proc.stdin.write(code + "\n")
    proc.stdin.flush()

    # Read the rest of the output
    stdout, stderr = proc.communicate()
    print("GCLOUD STDOUT:", stdout)
    
    with open(result_file, "w") as f:
        if proc.returncode == 0:
            f.write("SUCCESS")
        else:
            f.write(f"ERROR: exit code {proc.returncode}\n{stdout}\n{stderr}")

if __name__ == "__main__":
    main()
