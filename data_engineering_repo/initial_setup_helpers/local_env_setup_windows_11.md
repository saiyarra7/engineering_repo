# Environment Setup: Data Engineering Stack (Windows 11)
**Project:** data-engineering-repo-2026  
**Target Architecture:** Python 3.14 + UV + VS Code  

## 1. Core Toolchain Installation
Run in an Administrative PowerShell:
```powershell
# Install VS Code & Git
winget install --id Microsoft.VisualStudioCode --source winget --override "/VERYSILENT /MERGETASKS='!runcode,addcontextmenufiles,addcontextmenufolders,addtopath'"
winget install --id Git.Git --source winget


# Install uv
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

cd "C:\Users\Sai Yarra\Documents\tech_projects\data-engineering-repo-2026"
uv sync

# set execution policy in windows to run scripts and enable venv in vscode
# No need to install python seperately as you'd use the python available in venv and uv handles it.