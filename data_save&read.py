'''
spark可以通过Hadoop MapReduce所使用的InputFormat和OutputFormat接口访问数据
'''
input = sc.textFile('file:///home/holden/repos/spark/README.md')
