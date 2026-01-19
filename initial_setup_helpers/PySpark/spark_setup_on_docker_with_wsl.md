# End-to-End Spark Data Engineering Setup (Windows 11 + Ryzen 7)

This guide provides the full sequence to move from a broken Windows-native Spark environment to a professional containerized Linux environment.

## 1. Hardware & OS Foundation (WSL2)
Docker on Windows requires the Windows Subsystem for Linux (WSL2) to function.

### Step A: Enable Virtualization (BIOS)
1. Open **Task Manager** (Ctrl+Shift+Esc).
2. Go to **Performance > CPU**.
3. Check **Virtualization**. 
   - If **Disabled**: Reboot -> F1 (BIOS) -> Security -> Virtualization -> **SVM Mode: Enabled**.

### Step B: Install WSL2 Components
Run in PowerShell as **Administrator**:
```powershell
# Install WSL and the default Ubuntu distribution
wsl --install

# Force update the kernel to the latest version
wsl --update

# Ensure WSL 2 is the default version for the engine
wsl --set-default-version 2


# Define the list of legacy Spark/Java variables to be deleted
$vars = @("JAVA_HOME", "HADOOP_HOME", "SPARK_HOME", "PYSPARK_PYTHON", "PYSPARK_DRIVER_PYTHON")

foreach ($v in $vars) {
    # Delete from User profile
    [Environment]::SetEnvironmentVariable($v, $null, "User")
    # Delete from System/Machine profile (requires Admin)
    [Environment]::SetEnvironmentVariable($v, $null, "Machine")
    Write-Host "Successfully purged: $v" -ForegroundColor Cyan
}

# Final check: Inform the user to restart the terminal to apply changes
Write-Host "Cleanup complete. Restart your PowerShell session now." -ForegroundColor Green


# Remove the manual Hadoop/Winutils folder from C drive
# This prevents Windows from accidentally finding these old binaries
Remove-Item -Recurse -Force C:\hadoop -ErrorAction SilentlyContinue

#Step 2
# Install Docker Desktop via winget (Standard for DE workflow)
winget install -e --id Docker.DockerDesktop


#step 3 
#Create a file named docker-compose.yml in your data-engineering-repo-2026 root folder.

services:
  spark-master:
    image: apache/spark:3.5.3
    container_name: spark-master
    environment:
      - SPARK_MODE=master
    ports:
      - '8080:8080'
      - '7077:7077'
    volumes:
      - .:/opt/spark/work-dir  # Official images use /opt/spark/work-dir

  spark-worker:
    image: apache/spark:3.5.3
    container_name: spark-worker
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
    volumes:
      - .:/opt/spark/work-dir
    depends_on:
      - spark-master


#5. Execution & Verification
#Step A: Spin up the Spark Cluster
#In your project terminal (the root folder), run:

docker-compose up -d #to start the container
docker-compose down #to stop the container

#6. Run this to test if spark is running successfully.
docker exec -it spark-master /opt/spark/bin/spark-submit /opt/spark/work-dir/initial_setup_helpers/PySpark/check_spark.py