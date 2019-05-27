# 集群与Spark
Spark应用通过一个叫做**集群管理器**的外部服务在集群中的机器上启动。Spark自带的集群管理器被称为独立集群管理器。  
Spark也能运行在Hadoop YARN和Apache Mesos这两大开源集群管理器上。  

Spark驱动器是执行你的程序中的main()方法的进程。它执行用户编写的用来创建SC、创建RDD、以及RDD转化操作和行动操作的代码。  
**驱动器程序在Spark应用中有下属两个职责：**   
  * 把用户程序转为任务  
    Spark驱动器程序负责吧用户程序转为多个物理执行的单元，这些单元也被成为任务(task)  
    Spark程序其实是隐式地创建出了一个由操作组成的逻辑上的有向无环图(Directed Acyclic Graph,简称DAG)。  
    当驱动器程序运行时，它会把这个逻辑图转为物理执行计划。  
    Spark把逻辑计划转为一系列步骤(stage)。而每个步骤又由多个步骤组成。这些任务会被打包并被送到集群中。
    
    - 任务是Spark中最小的工作单元  
  
  * 为执行器节点调度任务  
    有了物理执行计划之后，Spark驱动器程序必须在各执行器进程间协调任务的调度。  
    每个执行器节点代表一个能够处理任务和存储RDD数据的进程。  
    当任务执行时，执行器进程会把缓存数据存储起来，而驱动器进程同样会跟踪这些缓存数据的位置，并且利用这些位置信息来调度以后的任务，以尽量减少传输。  
    驱动器程序会将一些Spark应用的运行时的信息通过网页界面呈现出来，默认端口为4040上。如本地为:http://localhost:4040
    
## 执行器节点
Spark执行器节点是一种工作进程，负责在Spark作业中运行任务，任务间相互独立。  
Spark应用启动是，执行器节点就被同时启动，并且伴随着整个Spark应用的生命周期而存在。如有发生异常或崩溃，spark应用也能继续执行。  
**执行器进程的两大作用：**
  * 负责运行组成Spark应用的任务，并将结果返回给驱动器进程；  
  * 它们通过自身的块管理器（Block Manager）为用户程序中要求缓存的RDD提供内存式存储。RDD是直接缓存在执行器进程内的，因此任务可以在运行时，  
    充分利用缓存数据加速运算
  
  - 特例：在本地模式下，Spark驱动器程序和各执行器程序在同一个JAVA进程中运行。