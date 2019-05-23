'''
Spark的数值操作是通过流式算法实现的，允许以每次一个元素的方式构建出模型。这些统计数据都会在调用stats()时通过一次遍历数据计算出来，
并以StatsCounter对象返回。
接下来，
我们会使用汇总统计来从数据中移除一些异常值。由于我们会两次使用同一个RDD（一次用来计算汇总统计数据，另一次用来移除异常值）
'''

# python移除异常值
# 要把String类型RDD转为数字数据，这样才能使用统计函数并移除异常值
distanceNumerics = distances.map(lambda string: float(string))
stats = distanceNumerics.stats()
stddev = stats.stdev()
mean = stats.mean()
reasonableDistances = distanceNumerics.filter(lambda x: math.fabs(x - mean) < 3 * stddev)
print(reasonableDistances.collect())
