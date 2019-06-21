## 使用SparkConf配置Spark
对spark进行性能调优通过SparkConf类对Spark进行配置。  
```

# 创建一个conf对象
conf = new SarkConf()
conf.set("spark.app.name", "My Spark APP")
conf.set("spark.master", "local[4]")
conf.set("spark.ui.port", "36000") # 重载默认端口配置

# 使用这个配置对象创建一个SparkContext
sc = SparkContext(conf)
```
