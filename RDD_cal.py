# 1
from pyspark import SparkConf, SparkContext

# conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext()

nums = sc.parallelize([1, 2, 3, 4])
squared = nums.map(lambda x:x * x).collect()
for num in squared:
    print("%i" %(num))
# 返回的是序列的迭代器 输出的RDD并不是迭代器，而是一个包含各个迭代器可访问的所有元素的RDD

# 2
from pyspark import SparkContext

sc = SparkContext.getOrCreate()

lines = sc.parallelize(["hello world", "hi"])
words = lines.flatMap(lambda line: line.split(" "))
print(words.first()) # 返回hello

# 总结原理
'''
RDD1:{"coffee panda","happy panda","happiest panda party"}
——>rdd1.map(tokenize):{["coffee","panda"],["happy","panda"],["happiest","panda","party"]}

RDD1:同上
——>rdd1.flatMap(tokenize):{"coffee","panda","happy","panda","happiest","panda","party"}
'''
