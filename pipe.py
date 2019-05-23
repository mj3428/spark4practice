'''
Spark在RDD上提供pipe()方法。Spark的pipe()方法可以让我们使用任意一种语言实现Spark作业中的部分逻辑，只要它能读写Unix标准流就行
'''
# 在Python中使pipe()调用findistance.R的驱动器程序
# 使用一个R语言外部程序计算每次呼叫的距离
distScript = "./src/R/finddistance.R"
distScriptName = "findfistance.R"
sc.addFile(distScrpt)
def hasDistInfo(call):
  '''验证一次呼叫是否有计算距离时必需的字段'''
  requiredFields = ['mylat', 'mylong', 'contactlat', 'contactlong']
  return all(map(lambda f: call[f], requiredFields))
def formatCall(call):
  return "{0},{1},{2},{3}".format(call['mylat'], call['mylong'], call['concactlat'], call['contactlat'], call['contactlong'])
pipeInputs = contactsContactList.values().flatMap(lambda calls: map(formatCall, filter(hasDistInfo, calls)))
distances = pipeInputs.pipe(SparkFiles.get(disScriptName))
print distances.collect()
