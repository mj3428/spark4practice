# 创建pairRDD
'''
如：把一个普通的RDD转为pairRDD时，可以调用map()函数实现,原本为单词的序列拆成以第一个单词为建的键值对
'''
pairs = lines.map(lambda x: (x.split(" ")[0], x))

'''
结果如下：
["hello world", "hi"]--->[('hello', 'hello world'), ('hi', 'hi')] 单个字母以自身为键，同时以自身为值
["hello world", "hi man"]--->[('hello', 'hello world'), ('hi', 'hi man')]
'''

# 聚合操作
rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
# \\mapvalues遍历成元组 reduceByKey是聚合，形成新的RDD\\
# MapReduce中的合成器（combiner），调用reduceByKey()和foldByKey()会在为每个键计算全局的总结果之前先自动在每台机器上进行本地合并

# 简单的单词统计（实际也是用聚合）
lines = sc.parallelize(["hello world", "hi man"])
words = lines.flatMap(lambda x: x.split(" "))
result = words.map(lambda x: (x,1)).reduceByKey(lambda x, y: x + y)
# \\output:[('hello', 1), ('world', 1), ('hi', 1), ('man', 1)]
# 当然更快的方式可以尝试
input.flatMap(x => x.plit(" ")).countByValue()

# 行动操作
'''
input:{(1, 2),(3, 4),(3, 6)}
rdd.countByKey() ---> {(1,1), (3,2)}对建的数量进行计数
rdd.collectAsMap() ---> Map{(1, 2),(3, 4),(3, 6)} 结果以映射表的形式返回，以便查询
rdd.lookup(3) ---> [4, 6] 查询键，对应的值的所有组成的列表
'''

# 自定义分区
import urlparse

def hash_domain(url):
    return hash(urlparse.urlparse(url).netloc)
rdd.partitionBy(20, hash_domain) # 创建20个分区
'''
在python中不需扩展Partitioner类，而是把一个特定的哈希函数作为一个额外的参数传给RDD.partitionBy()函数
'''
