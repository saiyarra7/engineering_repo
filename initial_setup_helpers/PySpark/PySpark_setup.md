# Running spark on docker using WSL on windows 11.



Step 1
# Install Microsoft's build of OpenJDK 17
winget install Microsoft.OpenJDK.17

#setup the path

# Set JAVA_HOME for your user account only
[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Microsoft\jdk-17.0.x.x-hotspot", "User")

# Update your user Path (Append bin folder)
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", $userPath + ";%JAVA_HOME%\bin", "User")

Step 2:
Setup winutils.ext for hadoop dependencies. 




Step 3:

uv pip install pyspark
# Then open a python shell and run:
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()
print(f"Spark Version: {spark.version}")