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
