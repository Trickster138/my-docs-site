import run_reports
from mkdocs.config import load_config
from mkdocs.commands.build import build
from mkdocs.commands.gh_deploy import gh_deploy
from git import Repo

# Run reports
print("Running reports...")
run_reports.main()  # this updates and pushes docs/index.md
print("Reports completed")

# Build the site
print("Building MkDocs site...")
config = load_config(config_file="mkdocs.yml")
build(config)
print("Site built locally in 'site/' folder")

# Deploy to GitHub Pages
print("Deploying site to GitHub Pages...")
gh_deploy(config, force=True)
print("Site deployed successfully!")
