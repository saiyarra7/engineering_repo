from pyspark.sql import SparkSession
import os

def main():
    # Initialize SparkSession correctly
    spark = (SparkSession.builder 
             .appName("Docker_Spark_Verification") 
             .getOrCreate())

    print("\n" + "="*50)
    print("SUCCESS: SparkSession Created in Linux Container")
    print(f"Spark Version: {spark.version}")
    print(f"Python Version: {os.sys.version}")
    print("="*50 + "\n")

    # Create dummy biotech data
    data = [
        ("Patient_A", "Control", 0.12),
        ("Patient_B", "Treated", 0.85),
        ("Patient_C", "Treated", 0.77),
        ("Patient_D", "Control", 0.09)
    ]
    columns = ["Patient_ID", "Group", "Expression_Level"]

    df = spark.createDataFrame(data, schema=columns)

    print("Sample Data Processing Results:")
    df.show()

    # Confirm connection to the cluster master
    sc = spark.sparkContext
    print(f"Connected to Master: {sc.master}")
    
    spark.stop()

if __name__ == "__main__":
    main()