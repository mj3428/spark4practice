# Spark SQL性能
*Spark SQL多列求和*
```
SELECT SUM(user.favouritesCount), SUM(retweetCount), user.id FROM tweets GROUP BY user.id
```
Spark SQL可以利用其对类型的了解来高效地表示数据。当缓存数据时，Spark SQL使用内存式的列式存储
## 另外性能选项
| 选项 | 用途 |
| :-------|:-------------|
| spark.sql.codegen | 设为true时，Spark SQL会把每条查询语句在运行时编译为JAVA二进制代码提高大型查询性能 |
| spark.sql.inMemoryColumnarStorage.compressed | 默认为false;自动对内存中的列式存储进行压缩 |
| spark.sql.inMemoryColumnarStorage.batchSize | 默认为1000;列式缓存时的每个批处理的大小。把这个值调大可能会导致内存不够的异常 |
| spark.sql.paquet.compress.codec | 默认为snappy;使用哪种压缩编码器。可选:uncompressed/snappy/gzip/lzo |
