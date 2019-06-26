# sparksql功能
1. 可以从各种各种结构化数据源(例如JSON,Hive,Parquet等)中读取数据  

2. 不仅支持在spark程序内使用sql语句进行数据查询，也支持从类似商业Tableau这样的外部工具中通过标准数据库连接器(JDBC/ODBC)连接
   Spark SQL进行查询  
   
3. 当在spark程序内使用sparksql时，spark sql支持sql与常规的Py/java/scala代码高度整合，包括连接RDD与SQL表、公开的自定义的SQL函数

为了实现这些功能，sparksql提供了一种特殊的RDD，叫作SchemaRDD（1.3版本后被称作DataFrame）。SchemaRDD是存放Row对象的RDD，每个Row对象代表一行记录。
SchemaRDD还包含记录的结构信息（即数据字段）。在SchemaRDD内部，可以利用结构信息更加高效地存储数据。  
## 连接SparkSQL
Apache Hive是Hadoop上的SQL引擎，Spark SQL编译时可以包含Hive支持，也可以不包含。包含Hive支持的SparkSQL可以支持Hive表访问、UDF（用户自定义函数）、
SerDe（序列化格式和反序列化格式），以及Hive查询语言（HiveQL/HQL）。如果要在SparkSQL中包含HIVE的库，并不需要事先安装HIVE。一般来说，最好
还是在编译SparkSQL时引入Hive支持，这样就可以使用这些特性了。  
**注：** 如果你的应用于Hive之间发生了依赖冲突，并且无法通过依赖排除以及依赖封装解决问题，你也可以使用没有Hive支持的SparkSQL进行编译和连接。
## 在应用中使用Spark SQL
### 初始化Spark SQL
*例：Scala中SQL的import声明*
```
//导入Spark SQL
import org.apache.spark.sql.hive.HiveContext
//如果不能使用hive依赖的话
import org.apache.spark.sql.SQLContext
```
*例：Scala中SQL需要导入的隐式转换支持*
```
// 创建Spark SQL的HiveContext
val hiveCtx = ...
//导入隐式转换支持
import hiveCtx._
```
*例：Py中SQL的import声明*
```
# 导入Spark SQL
from pyspark.sql import HiveContext, Row
# 当不能引入Hive依赖时
from pysqpark.sql import SQLContext, Row
```
添加好import声明后，需要创建出一个HiveContext对象。而如果无法引入Hive依赖，就创建出一个SQLContext对象作为SQL的上下文环境  
*在Scala中创建SQL上下文环境*
```
val sc = new SparkContext(...)
val hiveCtx = new HiveContext(sc)
```
*在Py中创建SQL上下文环境*
```
hiveCtx = HiveContext(sc)
```
有了HiveContext或SQLContext之后，我们就可以准备读取数据并进行查询了
### 基本查询示例
先从JSON文件中读取一些推特数据，把这些数据注册为一张临时表并赋予该表一个名字，然后就可以用SQL来查询它了。  
*例：在Py中读取并查询推文*
```
input = hiveCtx.jsonFile(inputFile)
# 注册输入的SchemaRDD
input.registerTempTable("tweets")
# 依据retweetCount(转发记数)选出推文
SchemaRDD topTweets = hiveCtx.sql("""SELECT text, retweetCount FROM tweets ORDER BY retweetCount LIMIT 10""")
```
### SchemaRDD
从内部机理看，SchemaRDD是一个由Row对象组成的RDD，附带包含每列数据类型的结构信息。Row对象只是对基本数据类型（如整型和字符串类型等）
的数组的封装。  
在Py中，由于没有显式的类型系统，Row对象变得稍有不同。我们使用row[i]来访问第i个元素,同时，还能使用row.col_name的形式使用名字访问其中的字段。
*在Py中访问topTweet这个SchemaRDD中的列*
```
topTweetText = topTweets.map(lambda row: row.text)
```
## 读取数据和存储数据
### Apache Hive
要把spark sql连接到已经部署好的Hive上，你需要提供一份Hive配置。你只需要把你的hive-site.xml文件复制到spark的./conf/目录下即可。
如果你只是想探索一下sparksql而没有配置hive-site.xml文件,那么spark sql会使用本地的Hive元数据仓，并且同样可以轻松地将数据读取到
Hive表中进行查询。  
*使用Py从Hive读取*
```
from pyspark.sql import HiveContext

hiveCtx = HiveContext(sc)
rows = hiveCtx.sql("SELECT key, value FROM mytable")
keys = rows.map(lambda row: row[0])
```
### Parquet
*Py中的Parquet数据读取*
```
# 从一个有name和favouriteAnimal字段的Parquet文件中读取数据
rows = hiveCtx.parquetFile(parquetFile)
names = rows.map(lambda row: row.name)
print "Everyone"
print name.collect()
```
*Py中的Parquet数据查询*
```
# 寻找熊猫爱好者
tbl = rows.registerTempTable("people")
pandasFriends = hiveCtx.sql("SELECT name FROM people WHERE favouriteAnimal = \"panda\")
print "Panda friends"
print pandaFriends.map(lambda row: row.name).collect()
```
*Py中的Parquet文件保存*
```
pandaFriends.saveAsParquetFile("hdfs://...")
```
