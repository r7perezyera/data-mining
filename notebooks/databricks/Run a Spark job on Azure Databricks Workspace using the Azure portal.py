# Databricks notebook source
# MAGIC %md
# MAGIC # Run a Spark job on Azure Databricks Workspace using the Azure portal
# MAGIC In this step, create a Spark DataFrame with Seattle Safety Data from Azure Open Datasets, and use SQL to query the data.
# MAGIC 
# MAGIC The following command sets the Azure storage access information. Paste this PySpark code into the first cell and use Shift+Enter to run the code.

# COMMAND ----------

blob_account_name = "azureopendatastorage"
blob_container_name = "citydatacontainer"
blob_relative_path = "Safety/Release/city=Seattle"
blob_sas_token = r"?st=2019-02-26T02%3A34%3A32Z&se=2119-02-27T02%3A34%3A00Z&sp=rl&sv=2018-03-28&sr=c&sig=XlJVWA7fMXCSxCKqJm8psMOh0W4h7cSYO28coRqF2fs%3D"

# COMMAND ----------

The following command allows Spark to read from Blob storage remotely. Paste this PySpark code into the next cell and use Shift+Enter to run the code.

# COMMAND ----------

wasbs_path = 'wasbs://%s@%s.blob.core.windows.net/%s' % (blob_container_name, blob_account_name, blob_relative_path)
spark.conf.set('fs.azure.sas.%s.%s.blob.core.windows.net' % (blob_container_name, blob_account_name), blob_sas_token)
print('Remote blob path: ' + wasbs_path)

# COMMAND ----------

The following command creates a DataFrame. Paste this PySpark code into the next cell and use Shift+Enter to run the code.

# COMMAND ----------

df = spark.read.parquet(wasbs_path)
print('Register the DataFrame as a SQL temporary view: source')
df.createOrReplaceTempView('source')

# COMMAND ----------

Run a SQL statement return the top 10 rows of data from the temporary view called source. Paste this PySpark code into the next cell and use Shift+Enter to run the code.

# COMMAND ----------

print('Displaying top 10 rows: ')
display(spark.sql('SELECT * FROM source LIMIT 100'))

# COMMAND ----------

