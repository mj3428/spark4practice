# 创建RDD
'''
如：把一个普通的RDD转为pairRDD时，可以调用map()函数实现,原本为单词的序列拆成以首字母为建的键值对
'''
pairs = lines.map(lambda x: (x.split(" ")[0], x))
