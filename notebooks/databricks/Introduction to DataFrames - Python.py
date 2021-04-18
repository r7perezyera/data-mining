# Databricks notebook source
# MAGIC %md
# MAGIC # Introduction to DataFrames - Python

# COMMAND ----------

#https://docs.microsoft.com/en-us/azure/databricks/spark/latest/dataframes-datasets/introduction-to-dataframes-python
# import pyspark class Row from module sql
from pyspark.sql import *

# Create Example Data - Departments and Employees

# Create the Departments
department1 = Row(id='123456', name='Computer Science')
department2 = Row(id='789012', name='Mechanical Engineering')
department3 = Row(id='345678', name='Theater and Drama')
department4 = Row(id='901234', name='Indoor Recreation')

# Create the Employees
Employee = Row("firstName", "lastName", "email", "salary")
employee1 = Employee('michael', 'armbrust', 'no-reply@berkeley.edu', 100000)
employee2 = Employee('xiangrui', 'meng', 'no-reply@stanford.edu', 120000)
employee3 = Employee('matei', None, 'no-reply@waterloo.edu', 140000)
employee4 = Employee(None, 'wendell', 'no-reply@berkeley.edu', 160000)
employee5 = Employee('michael', 'jackson', 'no-reply@neverla.nd', 80000)

# Create the DepartmentWithEmployees instances from Departments and Employees
departmentWithEmployees1 = Row(department=department1, employees=[employee1, employee2])
departmentWithEmployees2 = Row(department=department2, employees=[employee3, employee4])
departmentWithEmployees3 = Row(department=department3, employees=[employee5, employee4])
departmentWithEmployees4 = Row(department=department4, employees=[employee2, employee3])

print(department1)
print(employee2)
print(departmentWithEmployees1.employees[0].email)

# COMMAND ----------

#Create DataFrames for a list of rows
departmentsWithEmployeesSeq1 = [departmentWithEmployees1, departmentWithEmployees2]
df1 = spark.createDataFrame(departmentsWithEmployeesSeq1)

display(df1)

departmentsWithEmployeesSeq2 = [departmentWithEmployees3, departmentWithEmployees4]
df2 = spark.createDataFrame(departmentsWithEmployeesSeq2)

display(df2)

# COMMAND ----------

#Union two DataFrames
unionDF = df1.union(df2)
display(unionDF)

# COMMAND ----------

#Write the unioed DataFrame to a Parquet file
# Remove the file if it exists
dbutils.fs.rm("/tmp/databricks-df-example.parquet", True)
unionDF.write.parquet("/tmp/databricks-df-example.parquet")

# COMMAND ----------

#Read a DataFrame from the Parquet file
parquetDF = spark.read.parquet("/tmp/databricks-df-example.parquet")
display(parquetDF)

# COMMAND ----------

#Explode the employees column
from pyspark.sql.functions import explode

explodeDF = unionDF.select(explode("employees").alias("e"))
flattenDF = explodeDF.selectExpr("e.firstName", "e.lastName", "e.email", "e.salary")

flattenDF.show()
explodeDF.show()

# COMMAND ----------

#Use filter() to return the rows that match a predicate
filterDF = flattenDF.filter(flattenDF.firstName == "xiangrui").sort(flattenDF.lastName)
display(filterDF)

# COMMAND ----------

from pyspark.sql.functions import col, asc

# Use `|` instead of `or`
filterDF = flattenDF.filter((col("firstName") == "xiangrui") | (col("firstName") == "michael")).sort(asc("lastName"))
display(filterDF)

# COMMAND ----------

#The where() clause is equivalent to filter()
whereDF = flattenDF.where((col("firstName") == "xiangrui") | (col("firstName") == "michael")).sort(asc("lastName"))
display(whereDF)

# COMMAND ----------

#Replace null values with -- using DataFrame NA function
nonNullDF = flattenDF.fillna("--")
display(nonNullDF)

# COMMAND ----------

#Retrieve only rows with missing firstName of lastName
filterNonNullDF = flattenDF.filter(col("firstName").isNull() | col("lastName").isNull()).sort("email")
display(filterNonNullDF)

# COMMAND ----------

#Example aggregations using agg() and countDistinct()
from pyspark.sql.functions import countDistinct

countDistinctDF = nonNullDF.select("firstName", "lastName")\
  .groupBy("firstName")\
  .agg(countDistinct("lastName").alias("distinct_last_names"))

display(countDistinctDF)