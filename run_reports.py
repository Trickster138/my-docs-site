import os
import shutil
import datetime
from git import Repo, GitCommandError

def main():
    # CONFIG
    REPO_URL = "https://github.com/Trickster138/my-docs-site.git"
    LOCAL_DIR = os.getcwd()  # current working directory
    INDEX_FILE = os.path.join(LOCAL_DIR, "docs", "index.md")

    # --- Delete the local repo if it exists ---
    if os.path.exists(LOCAL_DIR):
        print(f"🧹 Removing existing repo at {LOCAL_DIR}...")
        shutil.rmtree(LOCAL_DIR)

    # --- Fresh clone ---
    print(f"👉 Cloning repository to {LOCAL_DIR}...")
    repo = Repo.clone_from(REPO_URL, LOCAL_DIR)
    origin = repo.remote(name="origin")

    # --- Checkout main branch ---
    try:
        repo.git.checkout("main")
    except GitCommandError:
        repo.git.checkout("-b", "main")

    # --- Update index.md with current timestamp ---
    print(f"👉 Updating {INDEX_FILE}...")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(INDEX_FILE, "w") as f:
        f.write("# Latest Reports\n\n")
        f.write(f"This file is automatically updated by run_reports.py on {current_time}.\n")

    # --- Add and commit all changes ---
    print("👉 Committing all changes...")
    repo.git.add(A=True)
    try:
        repo.index.commit("Update index.md via run_reports.py")
    except GitCommandError:
        print("⚠️ Nothing to commit (working tree clean).")

    # --- Push to GitHub ---
    try:
        print("👉 Pushing changes to origin/main...")
        origin.push(refspec="main:main", set_upstream=True)
        print("✅ Changes pushed successfully!")
    except GitCommandError as e:
        print("❌ Git push failed:", e)

if __name__ == "__main__":
    main()
