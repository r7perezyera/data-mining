# Databricks notebook source
https://docs.microsoft.com/en-us/azure/databricks/getting-started/spark/quick-start#requirements

# COMMAND ----------

# Take a look at the file system
display(dbutils.fs.ls("/databricks-datasets/samples/docs/"))

# COMMAND ----------

textFile = spark.read.text("/databricks-datasets/samples/docs/README.md")

# COMMAND ----------

textFile.count()

# COMMAND ----------

# Output the first line from the text file
textFile.first()

# COMMAND ----------

  # Filter all of the lines within the DataFrame
linesWithSpark = textFile.filter(textFile.value.contains("Spark"))

# COMMAND ----------

# Perform a count (action) 
linesWithSpark.count()
Out[11]: 12

# COMMAND ----------

linesWithSpark.take(12)