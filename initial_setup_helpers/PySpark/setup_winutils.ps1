# --- SPARK WINDOWS SETUP BLOCK ---
Write-Host "Starting Spark Environment Setup..." -ForegroundColor Cyan

# 1. Create Folders
$hadoopPath = "C:\hadoop"
if (!(Test-Path "$hadoopPath\bin")) {
    New-Item -Path "$hadoopPath\bin" -ItemType Directory -Force
}

# 2. Download Binaries (Winutils + Hadoop DLL)
Write-Host "Downloading binaries..."
$baseUrl = "https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.5/bin"
curl.exe -L -o "$hadoopPath\bin\winutils.exe" "$baseUrl/winutils.exe"
curl.exe -L -o "$hadoopPath\bin\hadoop.dll" "$baseUrl/hadoop.dll"

# 3. Set User Environment Variables (No Admin Required)
Write-Host "Configuring Environment Variables..."
[Environment]::SetEnvironmentVariable("HADOOP_HOME", $hadoopPath, "User")

# Update Path safely
$oldPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($oldPath -notlike "*C:\hadoop\bin*") {
    [Environment]::SetEnvironmentVariable("Path", "$oldPath;C:\hadoop\bin", "User")
}

Write-Host "Setup Complete! PLEASE RESTART YOUR TERMINAL NOW." -ForegroundColor Green
# --- END BLOCK ---