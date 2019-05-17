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
