# 关键性能考量
## 并行度
**RDD的逻辑表示其实是一个对象集合**。  
即在物理执行期间，RDD会被分为一系列的分区，每个分区都是整个数据的子集。当Spark调度并运行
任务时，Spark会为每个分区中的数据创建出一个任务。该任务在默认情况下会需要集群中的一个计算核心来执行。Spark也会针对RDD直接自动推断出合适
的并行度，这对于大多数用例来说已经足够了。  
*例*:从HDFS上读数据的输入RDD会为数据在HDFS上的每个文件区块创建一个分区。从数据混洗后的RDD派生下来的RDD则会采用与其父RDD相同的并行度。  
**Spark有两种方法**对操作的并行度进行调优。i:在数据混洗操作时，使用参数的方式为混洗后的RDD指定并行度。ii：对于任何已有的RDD，可以进行
重新分区来获取更多或者更少的分区数。  
重新分区操作通过repartition()实现，该操作会把RDD随机打乱并分成设定的分区数目。如果你确定要减少RDD分区，可以使用coalese()操作，由于
没有打乱数据该操作比reparttition()更为高效。  
*例*:默认情况下，filter()返回的RDD的分区数和其父节点一样，这样可能会产生很多空分分区或者只有很少数据的分区。  
```
# 也可以匹配数千个文件的通配字符串作为输入
>>>input = sc.textFile("s3n://log-files/2014/*.log")
>>>input.getNumPartitions()
35154
# 排除掉大部分数据的筛选方法
>>>lines = input.filter(lambda line: line.startswith("2014-10-17"))
>>>lines.getNumPartitions()
# 在缓存lines之前先对其进行合并操作
>>>lines = lines.coalesce(5).cache()
>>>lines.getNumPartitions()
4
# 可以在合并之后的RDD上进行后续分析
>>>lines.count()
```
## 序列化格式
Spark需要把数据序列化为二进制格式。序列化会在数据进行混洗操作时发生，此时有可能需要通过网络传输大量数据。  
默认情况，Spark会使用JAVA内建的序列化库。Spark也支持使用第三方序列化库Kryo,但不能直接序列化全部类型对象。几乎所有的应用都能在迁移到Kryo后获得了
更好的性能。  
### 使用Kryo序列化工具并注册所需类
```
val conf = new SparkConf()
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer") //严格要求注册类
conf.set("spark.kryo.registrationRequired", "true")
conf.registerKryoClasses(Array(class0f[MyClass], class0f[MyOtherClass]))
```
## 内存管理
* RDD存储  
  当调用RDD的persist()或chache()方法时，这个RDD的分区会被存储到缓存区中。Spark会根据spark.storage.memoryFraction限制用来
  缓存的内存占整个JVM堆空间的比例大小。如超出限制，旧的分区数据会被移出内存。  

* 数据混洗与聚合的缓存区  
  当数据进行混洗操作时，Spark会创建出一些中间缓存区来存储数据混洗的输出数据。这些缓存区用来存储聚合操作的中间结果，以及数据混洗操作中直接
  输出的部分缓存数据。  
  
* 用户代码  
  Spark可以执行任意的用户代码，所以用户的函数可以自行申请大量内存。例如，如果一个用户应用分配了巨大的数组或者其他对象，那这些都会
  占用总的内存。用户代码可以访问JVM堆空间中除分配给RDD存储和数据混洗存储以外的全部剩余空间。  

默认情况，Spark会使用60%的空间来存储RDD，20%存储数据混洗操作产生的数据，剩下的20%留给用户程序。
## 硬件供给
