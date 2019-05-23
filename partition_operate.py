'''
spark提供基于分区的map和foreach，让你的部分代码只对RDD的每个分区运行一次，这样可以帮助降低这些操作的代价
通过使用基于分区的操作，可以在每个分区内共享一个数据库连接池，来避免建立太多连接，同时还可以重用json解析器。
'''
# pytho中使用共享连接池 承接senior.py文件中的呼号示例
def processCallSigns(signs):
  # 创建一个连接池
  http = urllib3.PoolManager()
  # 与每条呼号记录相关联的URL
  urls = map(lambda x: "http://73s.com/qsos/%s.json" % x, signs)
  # 创建请求（非阻塞）
  requests = map(lambda x: (x, http.request('GET', x)), urls)
  # 获取结果
  result = map(lambda x: (x[0], json.loads(x[1].data)), requests)
  # 删除空的结果并返回
  return  filter(lambda x: x[1] is not None, result)

def fetchCallSigns(input):
  '''获取呼号'''
  return input.mapPartitions(lambda callSigns : processCallSigns(callSigns))
contactsContactList = fetchCallSigns(validSigns)

# 不使用mapPartitions()求均值
def combineCtrs(c1, c2):
  return (c1[0] + c2[0], c1[1] + c2[1])
def basicAvg(nums):
  '''计算平均值'''
  nums.map(lambda num: (num, 1)).reduce(combineCtrs)
# 使用mapPartitions()求均值
def  partitionCtr(nums):
  '''计算分区的sumCounter'''
  sumCount = [0, 0]
  for num in nums:
    sumCount[0] += num
    sumCount[1] += 1
  return [sumCount]
def fastAvg(nums):
  '''计算平均值'''
  nums.mapPartitions(partitionCtr).reduce(combineCtrs)
  return sumCount[0] / float(sumCount[1])

