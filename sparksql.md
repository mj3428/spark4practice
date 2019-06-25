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
