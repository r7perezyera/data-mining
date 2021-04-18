# Databricks notebook source
# MAGIC %md #Date and timestamps

# COMMAND ----------

# MAGIC %scala
# MAGIC java.time.ZoneId.systemDefault

# COMMAND ----------

# MAGIC %scala
# MAGIC java.sql.Timestamp.valueOf("1883-11-10 00:00:00").getTimezoneOffset / 60.0
