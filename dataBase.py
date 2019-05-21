'''
通过数据库提供的Hadoop连接器或者自定义的Spark连接器，Spark可以访问一些常用的数据库系统
'''

#HBase
'''
由于org.apache.hadoop.hbase.mapreduce.TableInputFormat类的实现，Spark可以通过Hadoop输入格式访问HBase
这个输入格式会返回键值对数据，其中键的类型为org.apache.hadoop.hbase.io.ImmutableBytesWritable,而值的类型为org.apache.hadoop.hbase.client.Result
Result类包含多种根据列获取值的方法
Result API：hbase.apache.org/apidocs/org/apache/hadoop/hbase/clientResult.html
TableInputFormat包含多个可以用来优化对HBase的读取的设置项，比如将扫描限制到一部分列中，以及限制扫描的时间范围
'''

#Elasticsearch
'''
Elasticsearch连接器依赖于在SparkContext中设置的配置项。Elasticsearch的OutputFormat连接器也没有用到Spark所封装的类型，所以我们使用
saveAsHadoopDataSet来代替，这意味着我们需要手动设置更多属性。
就输出而言，Elasticsearch可以进行映射判断，但是偶尔会推断出不正确的数据类型。因此如果你要存储字符串以外的数据类型，最好明确指定类型映射
'''
