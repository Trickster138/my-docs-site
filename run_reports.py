import os
from git import Repo, GitCommandError

def main():
    # CONFIG
    REPO_URL = "https://github.com/Trickster138/my-docs-site.git"
    LOCAL_DIR = os.path.expanduser("~/my-docs-site")
    INDEX_FILE = os.path.join(LOCAL_DIR, "docs", "index.md")

    # --- Clone or open existing repo ---
    if not os.path.exists(LOCAL_DIR):
        print(f"👉 Cloning repository to {LOCAL_DIR}...")
        repo = Repo.clone_from(REPO_URL, LOCAL_DIR)
    else:
        print(f"👉 Opening existing repo at {LOCAL_DIR}...")
        repo = Repo(LOCAL_DIR)

    origin = repo.remote(name="origin")

    # --- Stash local changes if any ---
    if repo.is_dirty(untracked_files=True):
        print("⚠️ Local changes detected, stashing all changes...")
        repo.git.stash("save", "--include-untracked")

    # --- Fetch latest changes and reset local main ---
    print("👉 Fetching latest changes from origin/main...")
    origin.fetch()
    try:
        repo.git.checkout("main")
    except GitCommandError:
        repo.git.checkout("-b", "main")  # create main if it doesn't exist
    repo.git.reset("--hard", "origin/main")

    # --- Restore stashed changes ---
    if repo.git.stash("list"):
        print("👉 Restoring stashed changes...")
        repo.git.stash("pop")

    # --- Update index.md ---
    print(f"👉 Updating {INDEX_FILE}...")
    with open(INDEX_FILE, "w") as f:
        f.write("# Latest Reports\n\n")
        f.write("This file is automatically updated by run_reports.py.\n")

    # --- Commit changes if any ---
    if repo.is_dirty(untracked_files=True):
        repo.git.add(A=True)
        repo.index.commit("Update index.md via run_reports.py")

    # --- Push to GitHub ---
    try:
        print("👉 Pushing changes to origin/main...")
        origin.push(refspec="main:main", set_upstream=True)
        print("✅ Changes pushed successfully!")
    except GitCommandError as e:
        print("❌ Git push failed:", e)

if __name__ == "__main__":
    main()

