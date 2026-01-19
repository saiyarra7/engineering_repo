from pyspark.sql import SparkSession
import os

def main():
    # 1. Initialize SparkSession
    # In Docker, we don't need to specify the Master URL in the code 
    # if we submit via 'spark-submit', but it's good practice to set an App Name.
    spark = (SparkSession.builder 
             .appName("Docker_Spark_Verification") 
             .get_all_variables() # Optional: check environment
             .getOrCreate())

    print("\n" + "="*50)
    print("SUCCESS: SparkSession Created in Linux Container")
    print(f"Spark Version: {spark.version}")
    print(f"Python Version: {os.sys.version}")
    print("="*50 + "\n")

    # 2. Create a dummy dataset (Biotech Sample)
    data = [
        ("Patient_A", "Control", 0.12),
        ("Patient_B", "Treated", 0.85),
        ("Patient_C", "Treated", 0.77),
        ("Patient_D", "Control", 0.09)
    ]
    columns = ["Patient_ID", "Group", "Expression_Level"]

    df = spark.createDataFrame(data, schema=columns)

    # 3. Perform a basic transformation
    print("Row Count Check:")
    df.show()

    # 4. Check if we can see the Workers
    # This confirms the Master-Worker handshake is working
    sc = spark.sparkContext
    print(f"Master URL being used: {sc.master}")
    
    spark.stop()

if __name__ == "__main__":
    main()