# 累加器
'''
向SPARK传递函数时，集群中运行的每个任务都会得到这些变量的一份新的副本，更新这些副本的值也不会影响驱动器中的对应变量。
Spark的两个共享变量，累加器与广播变量，分别为结果聚合与广播这两种常见的通信模式突破了这一限制
# 在Python中累加空行
'''
file = sc.textFile(inputFile)
# 创建Accumulator[Int]并初始化为0
blankLines = sc.accumulator(0)

def extractCallSigns(line):
  global blankLines # 访问全局变量
  if (line== ""):
    blankLines += 1
  return line.split(" ")

callSigns = file.flatMap(extractCallSigns)
callSigns.saveAsTextFile(outputDir + "/callsigns")
print("Blank lines: %d" % blankLines.value)
'''
只有在运行saveAsTextFile()行动操作后才能看到正确的计数，因为行动操作前的转化操作flatMap()是惰性的，
所以作为计算副产品的累加器只有在惰性的转化操作flatMap()被saveAsTextFile()行动操作强制触发时才会开始求值
'''

# 累加器总结
'''
- 通过在驱动器中调用SparkContext.accumulator(initialValue)方法，创建出存有初始值的累加器。返回值为org.apache.spark.Accumulator[T]对象，
其中T是初始值initialValue的类型。
- Spark闭包里的执行器代码可以使用累加器的 += 方法（在JAVA中是add）增加累加器的值。
- 驱动器程序可以调用累加器的value属性（在JAVA中使用value()或setValue()）来访问累加器的值。
'''

# 累加器进行错误计数
'''
例：验证呼号，并且只有在大部分输入有效时才输出。
国际电信联盟在19号文件对业余电台的呼号格式进行了规范，我们可以根据这一规范，使用正则表达式来验证呼号
'''
# 创建用来验证呼号的累加器
validSignCount = sc.accumulator(0)
incalidSignCount = sc.accumulator(0)

def validateSign(sign):
  global validSignCount, invalidSignCount
  if re.match(r"\A\d?[a-zA-Z]{1,2}\d{1,4}[a-zA-Z]{1,3}\Z", sign): # 匹配规范文档
    validSignCount += 1
    return True
  else:
    invalidSignCount += 1
    return False
# 对于每个呼号的联系次数进行计数
validSigns = callSigns.filter(validateSign)
contactCount = validSigns.map(lambda sign: (sign, 1)).reduceByKey(lambda (x, y): x + y)
# 强制求值计算计数
contactCount.count()
if invalidSignCount.value < 0.1 * validSignCount.value:
  contactrCount.saveAsTextFile(outputDir +"/contactCount")
else:
  print("Too many errors : %d in %d" % (invalidSignCount.value, validSignCount.value))

# 累加器与容错性
'''
某节点执行map()操作的节点失败了，spark会在另一个节点上重新运行该任务。即使该节点没有崩溃，而只是处理速度比别的节点慢很多，
spark也可以抢占式地在另一个节点上启动一个“投机”speculative型的任务副本，如果该任务更早结束就可以直接获取结果。即使没有节点失败，
spark有时也需要重新运行任务来获取缓存中被移除出内存的数据。因此最终结果就是同一个函数可能对同一个数据运行了多次，这取决于集群发生了什么。
那累加器如何处理？
- 如果想要一个无论在失败还是重复计算时都绝对可靠的累加器，我们必须把它放在foreach()这样的行动操作中。
- 对于在RDD转化操作中使用的累加器，就不能保证有这种情况了。转化操作中累加器可能会发生不止一次更新，所以在转化操作中，累加器通常只用于调试目的。
'''

# 自定义累加器
'''
spark还支持其他Double、Long和Float型的累加器
'''

# 广播变量 Spark第二个共享变量类型
'''
它可以让程序员高效地向所有工作节点发送一个较大的只读值，以供一个或多个spark操作使用。
如：你的应用需要向所有节点发送一个较大的只读查询表，甚至是机器学习算法中的一个很大的特征向量，广播变量用起来都很顺手。
'''
# python中查询国家
# 查询RDD contactCounts中的呼号的对应位置。将呼号前缀
# 读取为国家代码来进行查询
signPrefixes = loadCallSignTable()

def processSignCount(sign_count, signPrefixes):
  country = lookupCountry(sign_count[0], signPrefixes)
  count = sign_count[1]
  return(country, count)
countryContactCounts = (contactCounts.map(processSignCount).reduceByKey((lambda x, y: x + y)))
'''
上述代码可以运行，但如果表很大，signPrefixes很容易就会达到数MB大小，从主节点为每个任务发送一个这样的数组就会代价巨大。而且，
如果之后还要再次使用signPrefixes这个对象（可能还要在file2.txt上运行同样的代码），则还需要向每个节点再发送一遍。
接下来，用广播变量解决
'''
# 查询RDD contactCounts中的呼号的对应位置。将呼号前缀
# 读取国家代码来进行查询
signPrefixes = sc.broadcast(loadCallSignTable())

def processSignCount(sign_count, signPrefixes):
  country = lookupCountry(sign_count[0], signPrefixes)
  count = sign_count[1]
  return(country, count)
countryContactCounts = (contactCounts.map(processSignCount).reduceByKey((lambda x, y: x + y)))
countryContactCounts.saveAsTextFile(outputDir + "/countries.txt")
'''
类型为spark.broadcast.Broadcast[T]的一个对象，其中存放着类型为T的值。可以在任务中通过对Broadcst对象调用value来获取该对象的值。
这个值智慧被发送到各节点一次，使用的是一种高效的类似BitTorrent的通信机制。
'''

# 广播的优化
'''
当广播一个比较大的值时，选择既快又好的序列化格式是很重要的
python解决方法
为你的数据类型实现自己的序列化方式，使用reduce()方法为python的pickle库定义自定义的序列化
'''
