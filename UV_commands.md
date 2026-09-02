# UV Package Manager Quick Reference Guide

## 1. Project Management (`uv project`)

| Command | Description |
| :--- | :--- |
| `uv init` | Initialize a new Python project in the current directory (`pyproject.toml`). |
| `uv init <project-name>` | Create a new directory and initialize a project inside it. |
| `uv add <package>` | Add and install a dependency to `pyproject.toml` and update `uv.lock`. |
| `uv add <package>@<version>` | Add a dependency with a specific version. |
| `uv add --dev <package>` | Add a development dependency. |
| `uv remove <package>` | Remove a dependency from `pyproject.toml` and update `uv.lock`. |
| `uv remove --dev <package>` | Remove a development dependency. |
| `uv lock` | Create or update the `uv.lock` file without installing packages. |
| `uv sync` | Synchronize environment with `uv.lock` (installs missing, removes extraneous). |
| `uv tree` | Display full project dependency tree. |
| `uv run <command>` | Run a command or script within the managed virtual environment context. |
| `uv run python <script.py>` | Execute a script within the project virtual environment. |
| `uv export --format requirements-txt -o requirements.txt` | Export locked dependencies to standard `requirements.txt`. |

---

## 2. Virtual Environment & Python Management

| Command | Description |
| :--- | :--- |
| `uv venv` | Create a `.venv` virtual environment using the default Python version. |
| `uv venv --python <version>` | Create a virtual environment using a specific Python version (e.g., `3.14`). |
| `uv python list` | List available and installed Python versions on the system. |
| `uv python install <version>` | Download and install a specific Python version managed by `uv`. |
| `uv python pin <version>` | Pin project Python version by writing a `.python-version` file. |

---

## 3. `pip` Interface Compatibility (`uv pip`)

| Command | Description |
| :--- | :--- |
| `uv pip install <package>` | Install a package into the active virtual environment. |
| `uv pip install -r requirements.txt` | Install dependencies from `requirements.txt`. |
| `uv pip list` | Display a flat list of installed packages in the current environment. |
| `uv pip uninstall <package>` | Uninstall a package from the active environment. |
| `uv pip compile pyproject.toml -o requirements.txt` | Compile dependencies to a pinned `requirements.txt`. |
| `uv pip sync requirements.txt` | Force environment to match `requirements.txt` strictly. |
| `uv pip tree` | Display dependency tree for packages in the current environment. |

---

## 4. Tool Execution (`uvx` / `uv tool`)

| Command | Description |
| :--- | :--- |
| `uvx <tool>` | Run an isolated CLI tool without permanent installation (e.g., `uvx ruff check .`). |
| `uv tool install <tool>` | Install a Python CLI tool globally in an isolated environment. |
| `uv tool list` | List globally installed CLI tools. |
| `uv tool upgrade --all` | Upgrade all globally installed tools. |

---

## 5. Cache & Maintenance

| Command | Description |
| :--- | :--- |
| `uv cache clean` | Clear all cached downloads and builds to free disk space. |
| `uv cache dir` | Print path to local `uv` cache directory. |
| `uv self update` | Update `uv` executable to the latest version. |