# MLlib
## 概述
MLlib就是RDD上一系列可供调用的函数的集合
**操作步骤如下:**
* 首先用字符串RDD来表示你的消息  
* 运行MLlib中的一个*特征提取(feature extraction)*算法来把文本数据转换为数值特征(适合机器学习算法处理)；该操作会返回一个向量
  RDD。  
* 对向量RDD调用分类算法（比如逻辑回归）；这步会返回一个模型对象，可以使用该对象对新的数据点进行分类。  
* 使用MLlib的评估函数在测试数据集上评估模型。  
*注：MLlib中只包含能够在集群上运行良好的并行算法*  
所有学习算法都是基于正确定义特征。  
*Py版垃圾邮件分类器*
```
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.classification import LogisticRegressionWithSGD

spam = sc.textFile("spam.txt")
normal = sc.textFile("normal.txt")

# 创建一个HashingTF实例来把右键文本映射为包含10000个特征的向量
tf = HashingTF(numFeattures = 10000)
# 个邮件都被切分为单词，每个单词背映射为一个特征
spamFeatures = spam.map(lambda email: tf.transform(email.split(" ")))
normalFeatures = normal.map(lambda email: tf.transform(email.split(" ")))

# 创建LabeledPoint数据集分别存放阳性（垃圾邮件）和阴性（正常邮件）的例子
positiveExamples = spamFeatures.map(lambda features: LabeledPoint(1, features))
negativeExamples = normalFeatures.map(lambda features: LabeledPoint(0, features))
trainingData = positiveExamples.union(negativeExamples)
trainingData.cache() # 因为逻辑回归是迭代算法，所以缓存训练数据RDD

# 使用SGD算法运行逻辑回归
model = LogisticRegressionWithSGD.train(trainingData)

# 以阳性（垃圾邮件）和阴性（正常邮件）的例子分别进行测试。首先使用
# 一样的HashingTF特征来得到特征向量，然后对该向量应用得到的模型
posTest = tf.transform(" O M G GET cheap stuff by sending money to ...".split(" "))
negTest = tf.transform("Hi Dad,I started studying Spark the other ...").split(" "))
print "Prediction for positive test example: %g" % model.predic(posTest)
print "Prediction for negative test example: %g" % model.predic(negTest)
```
## 数据类型
* Vector  
  一个数学向量；可通过mllib.linalg.Vectors类创建出来。
* LabeledPoint  
  在诸如分类和回归这样的监督是学习(supervised learning)算法中，LabeledPoint用来表示带标签的数据点。它包含一个特征向量与一个标签
  （由一个浮点数表示），位置在mllib.regression包中
* Rating  
  用户对一个产品的评分，在mllib.recommendation包中，用于产品推荐  
* 各种model类  
  每个Model都是训练算法的结果，一般有一个predict()方法可以用来对新的数据点或数据点组成的RDD应用该模型进行预测。  
### 操作向量
1. 向量分两种: 稠密向量与稀疏向量  
   稠密向量把所有维度的值放在一个浮点数数组中。例如，一个100维度的向量会存储100个双精度浮点数。相比之下，稀疏向量只把各维度中非
   零向量存储下来。当最多只有10%的元素为非零元素时，我们通常更倾向于使用稀疏向量。
2. 创建向量的方式在各种语言中有一些细微差别。  
*Py创建向量*
```
from numpy import array
from pyspark.mllib.linalg import Vectors

# 创建稠密向量<1.0, 2.0, 3.0>
denseVec1 = array([1.0, 2.0, 3.0]) # NumPy数组可以直接传给MLlib
denseVec2 = Vectors.dense([1.0, 2.0, 3.0]) # 或者使用Vectors类来创建

# 创建稀疏向量<1.0, 0.0, 2.0, 0.0>
# 向量的维度（4）以及非零位的位置和对应的值
# 这些数据可以用一个dictionary来传递，或者使用两个分别代表位置和值的list 
sparseVec1 = Vectors.sparse(4, {0: 1.0, 2: 2.0})
sparseVec2 = Vectors.sparse(4, [0, 2], [1.0, 2.0]})
```
## 算法
### 特征提取
*Py中使用HashingTF*
```
from pyspark.mllib.feature import HashingTF
senntence = "hello hello world"
words = sentence.split() # 将句子切分为一串单词
tf = HashingTF(10000) # 创建一个向量，其尺寸S = 10000
tf.transform(words)
# 结果: SparseVector(10000, {3065: 1.0, 6861: 2.0})
rdd = sc.wholeTextFiles("data").map(lambda (name, text): text.split())
tfVectors = tf.transform(rdd) # 整个RDD进行转化操作
```
*Py中使用TF-IDF*
```
from pyspark.mllib.feature import HashingTF, IDF
# 将若干文本文件读取为TF向量
rdd = sc.wholeTextFiles("data").map(lambda (name, text): text.split())
tf = HashingTF()
tfVectors = tf.transform(rdd).cache

# 计算IDF，然后计算TF-IDF向量
idf = IDF()
idfModel = idf.fit(tfVectors)
tfIdfVectors = idfModel.transform(tfVectors)
```
*Py中缩放向量*
```
from pyspark.mllib.feature import StandardScaler

vectors = [Vectors.dense([-2.0, 5.0, 1.0]), Vectors.dense([2.0, 0.0, 1.0])]
dataset = sc.parallelize(vectors)
scaler = StandardScaler(withMean=True, withStd=True)
model = scaler.fit(dataset)
result = model.transform(dataset)
# 结果:{[-0.7071, 0.7071, 0.0], [0.7071, -0.7071, 0.0]}
```
### 逻辑回归
**逻辑回归是一种二元分类方法，用来寻找一个分割阴性与阳性实例的线性分割平面**  
有两种算法:SGD和LBFGS。LBFGS一般是最好的选择。得出的LogisticRegressionModel可以为每个点求出一个在0-1之间的得分
之后会基于一个阈值返回0或1：默认情况下，对于0.5，它会返回1
