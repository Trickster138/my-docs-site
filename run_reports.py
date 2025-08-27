import os
import datetime
from git import Repo, GitCommandError

def main():
    # CONFIG
    REPO_URL = "https://github.com/Trickster138/my-docs-site.git"
    LOCAL_DIR = os.getcwd()  # current working directory
    INDEX_FILE = os.path.join(LOCAL_DIR, "docs", "index.md")

    # --- Clone or open existing repo ---
    if not os.path.exists(os.path.join(LOCAL_DIR, ".git")):
        print(f"👉 Cloning repository to {LOCAL_DIR}...")
        repo = Repo.clone_from(REPO_URL, LOCAL_DIR)
    else:
        print(f"👉 Opening existing repo at {LOCAL_DIR}...")
        repo = Repo(LOCAL_DIR)
        origin = repo.remote(name="origin")

        # Fetch latest changes
        print("👉 Fetching latest changes from origin...")
        origin.fetch()

        # Reset local main branch to match origin/main
        try:
            repo.git.checkout("main")
        except GitCommandError:
            repo.git.checkout("-b", "main")  # create if doesn't exist

        print("👉 Resetting local branch to origin/main...")
        repo.git.reset("--hard", "origin/main")

    origin = repo.remote(name="origin")

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
