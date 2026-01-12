# Project Initialization Guide (2026)

This document details the shell commands required to initialize the `data_engineering_repo_2026` workspace using the `uv` package manager on Windows 11.

## Setup Commands

| Command | Description | Technical Context |
| :--- | :--- | :--- |
| `cd ..` | **Change Directory** | Navigates to the parent directory to ensure the project folder is created in the correct root location. |
| `mkdir data_engineering_repo_2026` | **Make Directory** | Creates the project root folder. |
| `cd data_engineering_repo_2026` | **Navigate** | Enters the project scope. |
| `uv python install 3.14` | **Toolchain Setup** | Downloads and installs the specific Python 3.14 interpreter locally, ensuring version consistency across your ThinkPad and other machines. |
| `uv init` | **Initialize Project** | Bootstraps a `pyproject.toml` file to manage project metadata and dependencies. |
| `uv sync` | **Synchronize Environment** | Creates the `.venv` and locks dependencies to ensure a reproducible environment. |
| `uv add polars pandas pyarrow` | **Dependency Injection** | Installs libraries and updates the lockfile. `pyarrow` is essential for Parquet support in Biotech data workflows. |

## Dependency Rationale
* **Polars**: Optimized for multi-threaded performance on your Ryzen 7 Pro CPU.
* **Pandas**: Legacy support for specific data analysis tasks.
* **PyArrow**: Backend for efficient memory management and cross-library data exchange.


# command for checking all the package list
uv pip list