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
SparkConf实例包含用户要重载的配置选项的键值对。.set()方法可以添加配置项的设置。当然你也可以调用setAppName()和setMaster()来分别设置
spark.app.name和spark.master的配置值。  
spark-submint工具为常用的spark配置项参数提供了专用的标记，还有一个通用标记 --conf来接收任意spark配置项的值：  
```
$ bin/spark-submit
  --class com.example.MyApp
  --master local[4]
  --name "My Spark App"
  --conf spark.ui.port=36000
  myApp.jar
```
spark-submit也支持从文件中读取配置项的值。默认情况下，spark-submit脚本会在spark安装目中找到conf/spark-defaults.conf文件，尝试读取改文件中
以空格隔开的键值对数据。  
你也可以通过spark-submit的--properties-File标记，自定义改文件的路径。  
```
$ bin/spark-submit
  --class com.example.myApp
  --properties-file my-config.conf
  myApp.jar
## Contents of my-config.conf ##
spark.master local[4]
spark.app.name "My Spark App"
spark.ui.port 36000
```
### Spark有特定的优先级顺序，进行配置
