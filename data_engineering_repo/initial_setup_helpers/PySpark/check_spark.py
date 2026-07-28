import os
import sys

# 1. Manually specify the absolute path to your 3.12 venv python
# We use the raw string (r"") to handle backslashes
venv_python = r"C:\Users\Sai Yarra\Documents\tech_projects\data-engineering-repo-2026\.venv\Scripts\python.exe"

os.environ['PYSPARK_PYTHON'] = venv_python
os.environ['PYSPARK_DRIVER_PYTHON'] = venv_python

# 2. Ensure JAVA_HOME and HADOOP_HOME are explicitly set for this process
os.environ['JAVA_HOME'] = r"C:\PROGRA~1\Microsoft\jdk-17.0.13.11-hotspot" # USE YOUR EXACT FOLDER NAME
os.environ['HADOOP_HOME'] = r"C:\hadoop"

# ... rest of your script
from pyspark.sql import SparkSession

# 1. Force Python to use the correct executable
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# 2. Initialize Spark directly
try:
    spark = SparkSession.builder \
        .appName("Ryzen7_Direct_Init") \
        .master("local[*]") \
        .getOrCreate()

    print("\n" + "="*30)
    print(f"SUCCESS: Spark version {spark.version} is running.")
    print(f"Master: {spark.sparkContext.master}")
    print("="*30 + "\n")
    
    # Test a basic transformation
    df = spark.createDataFrame([("Data Engineer", 1)], ["Role", "ID"])
    df.show()
    
    spark.stop()
except Exception as e:
    print("\n" + "!"*30)
    print("STILL FAILING. Error details below:")
    print(e)
    print("!"*30 + "\n")