# Databricks notebook source
# MAGIC %md #Date and timestamps
# MAGIC Significant changes to Date and Timestamp datatypes in Databricks Runtime 7.0:
# MAGIC * Date type and associated calendar.
# MAGIC * Timestamp type and how it relates to timezones. Time zone offset resolution, behavior changes in the new time API in Java 8, used by Databricks Runtime 7.0.
# MAGIC * APIs to construct date and timestamp values.
# MAGIC * Common pitfalls and best practices for collecting date and timestamp objects on the Apache Spark Driver.
# MAGIC 
# MAGIC Source: https://docs.microsoft.com/en-us/azure/databricks/spark/latest/dataframes-datasets/dates-timestamps
# MAGIC 
# MAGIC 
# MAGIC Date is a combination of year, month and day.
# MAGIC Timestamp extends the Date type with: hour, minute, second and a global (session scoped) timezone.

# COMMAND ----------

# MAGIC %scala
# MAGIC java.time.ZoneId.systemDefault

# COMMAND ----------

# MAGIC %scala
# MAGIC java.sql.Timestamp.valueOf("1883-11-10 00:00:00").getTimezoneOffset / 60.0

# COMMAND ----------

spark.createDataFrame([(2020, 6, 26), (1000, 2, 29), (-44, 1, 1)],['Y', 'M', 'D']).createTempView('YMD')
df = sql('select make_date(Y, M, D) as date from YMD')
df.printSchema()

# COMMAND ----------

df.show()

# COMMAND ----------

df = spark.createDataFrame([(2020, 6, 28, 10, 31, 30.123456), \
(1582, 10, 10, 0, 1, 2.0001), (2019, 2, 29, 9, 29, 1.0)],['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND'])
df.show()

# COMMAND ----------

ts = df.selectExpr("make_timestamp(YEAR, MONTH, DAY, HOUR, MINUTE, SECOND) as MAKE_TIMESTAMP")
ts.printSchema()

# COMMAND ----------

ts.show(truncate=False)

# COMMAND ----------

df = spark.createDataFrame([(2020, 6, 28, 10, 31, 30, 'UTC'),(1582, 10, 10, 0, 1, 2, 'America/Los_Angeles'), \
(2019, 2, 28, 9, 29, 1, 'Europe/Moscow')], ['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND', 'TZ'])
df = df.selectExpr('make_timestamp(YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, TZ) as MAKE_TIMESTAMP')
df = df.selectExpr("date_format(MAKE_TIMESTAMP, 'yyyy-MM-dd HH:mm:SS VV') AS TIMESTAMP_STRING")
df.show(truncate=False)

# COMMAND ----------

# MAGIC %sql
# MAGIC select CAST(-123456789 AS TIMESTAMP);
# MAGIC -- 1966-02-02 05:26:51

# COMMAND ----------

# MAGIC %sql
# MAGIC select timestamp '2020-06-28 22:17:33.123456 Europe/Amsterdam', date '2020-07-01';
# MAGIC -- 2020-06-28 23:17:33.123456        2020-07-01

# COMMAND ----------

# MAGIC %sql
# MAGIC select cast('2020-06-28 22:17:33.123456 Europe/Amsterdam' as timestamp), cast('2020-07-01' as date);
# MAGIC -- 2020-06-28 23:17:33.123456        2020-07-01

# COMMAND ----------

# MAGIC %sql
# MAGIC select to_timestamp('28/6/2020 22.17.33', 'dd/M/yyyy HH.mm.ss');
# MAGIC -- 2020-06-28 22:17:33

# COMMAND ----------

# MAGIC %sql 
# MAGIC select timestamp 'yesterday', timestamp 'today', timestamp 'now', timestamp 'tomorrow';
# MAGIC -- 2020-06-27 00:00:00        2020-06-28 00:00:00        2020-06-28 23:07:07.18        2020-06-29 00:00:00
# MAGIC select date 'yesterday', date 'today', date 'now', date 'tomorrow';
# MAGIC -- 2020-06-27        2020-06-28        2020-06-28        2020-06-29

# COMMAND ----------

import datetime
df = spark.createDataFrame([(datetime.datetime(2020, 7, 1, 0, 0, 0), datetime.date(2020, 7, 1))], ['timestamp', 'date'])
df.show()

# COMMAND ----------

# MAGIC %scala
# MAGIC Seq(java.sql.Timestamp.valueOf("2020-06-29 22:41:30"), new java.sql.Timestamp(0)).toDF("ts").show(false)

# COMMAND ----------

# MAGIC %scala
# MAGIC Seq(java.time.Instant.ofEpochSecond(-12219261484L), java.time.Instant.EPOCH).toDF("ts").show

# COMMAND ----------

# MAGIC %scala
# MAGIC Seq(java.time.LocalDate.of(2020, 2, 29), java.time.LocalDate.now).toDF("date").show

# COMMAND ----------

# MAGIC %scala
# MAGIC df.collect()

# COMMAND ----------

# MAGIC %scala
# MAGIC [Row(timestamp=datetime.datetime(2020, 7, 1, 0, 0), date=datetime.date(2020, 7, 1))]
