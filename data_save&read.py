'''
spark可以通过Hadoop MapReduce所使用的InputFormat和OutputFormat接口访问数据
'''
input = sc.textFile('file:///home/holden/repos/spark/README.md')

# json 筛选出对喜爱熊猫的人保存为json格式
(data.filter(lambda x: x["lovesPandas"])).map(lambda x: json.dumps(x)).saveAsTextFile(outputFile)

#csv 若没有换行符 你也可以使用textFile()读取并解析数据
import csv
import StringIO
def loadRecord(line):
  '''解析一行CSV记录'''
  input = StringIO.StringIO(line)
  reader = csv.DictReader(input, fieldnames=["name", "favouriteAnimal"])
  return reader.next()
input = sc.textFile(inputFile).map(loadRecord)

# 完整读取csv
def loadRecord(line):
  '''解析一行CSV记录'''
  input = StringIO.StringIO(fileNameComtents[1])
  reader = csv.DictReader(input, fieldnames=["name", "favouriteAnimal"])
  return reader
fullFileData = sc.wholeTextFiles(inputFile).flatMap(loadRecords)

#写csv 会把结果放到RDD
def writeRecords(records):
  output = StringIO.StringIO()
  writer = csv.DictWriter(output, filenames=["name", "favouriteAnimal"])
  for record in records:
    writer.writerow(record)
  return [output.getvalue()]
pandaLovers.mapPartitions(writeRecords).saveAsTextFile(outputFile)

#SequenceFile 是Hadoop的MapReduce的输入输出格式
val data = sc.sequenceFile(inFile,"org.apache.hadoop.io.Text", "org.apache.hadoop.io.IntWritable")

# SparkSQL
'''
结构化或者半结构化的数据的方式 
结构化数据指的是有结构信息的数据————也就是所有的数据记录都具有一致字段结构的集合
'''
row[column_number]
row.column_name

#Apache Hive
'''
Hive可以在HDFS内或者在其他存储系统上存储多种格式的表
SparkSQL可以读取Hive支持的任何表
要把sparksql连接到已有的Hive上，你需要提供Hive的配置文件。你需要将hive-site.xml文件复制到Spark的./conf/目录下。
再创建出HiveContext对象，也就是SparkSQL的入口，然后你就可以使用Hive查询语言（HQL）来对你的表进行查询，并以由行组成的RDD的形式拿到返回数据
'''
from pyspark.sql import HiveContext

hiveCtx = HiveContext(sc)
rows = hiveCtx.sql("SELECT name, age FROM users")
firstRow = row.first()
print firstROW.name

#Hive读取JSON
'''
首先需要和使用HIVE一样创建HiveContext,(不过在这种情况下我们不需要安装好Hive,也就是说你也不需要hive-site.xml文件。)然后使用
HiveContext.jsonFile方法来从整个文件中获取由ROW对象组成的RDD。你也可以将RDD注册为一张表，然后从中选出特定的字段。
例如，有这样一个JSON文件：
{"user": {"name": "Holden", "location": "San Francisco"}, "text": "Nice day out today"}
{"user": {"name": "Matei", "location": "Berkeley"}, "text": "Even niceer here :)"}
我们可以读取这些数据，只从中选取username(用户名)和text(文本)字段
'''
tweets = hiveCtx.jsonFile("tweets.json") # 载入
tweets.registerTempTable("tweets") # 命名
results = hiveCtx.sql("SELECT user.name, text FROM tweets")
