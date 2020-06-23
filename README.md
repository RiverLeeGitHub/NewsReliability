# NewsReliability
System for analyzing news similarity and reliability <br>
新闻可信度的评判与分析(2018.5)

## Abstract
The main function of our program is to retrieve relative news searched by users via Wechat interaction, and return the classified news as well as each abstract, link, emotion, the class it belongs to, reliability and recommendation. The news we find and relative reports are only written in Chinese.<br>
本程序用于检索用户从微信接口查询的相关新闻，并返回给用户分类好的新闻及其链接、摘要、情感、可信度和相关建议。新闻分析仅限中文内容。

## How to run
### Prerequisite
  Python 3.6: 安装并配置 pip<br>
  Itchat: 微信端框架，安装命令$ pip install Itchat<br>
  Bosonnlp: 玻森中文语义开放平台，安装命令$ pip install -U bosonnlp<br>
  Aip: 百度开放平台，安装命令$ pip install baidu-aip<br>
  Please keep the network unblocked at runtime. 运行时请保持网络畅通。
### Module Function
  WechatInteraction.py：The entrance of the whole program, using Wechat to interact with user.程序入口，与用户进行微信交互。<br>
  MainLine.py：The mainline code to call other modules and implement news analyzing.主线代码，用于调用其他模块并进行新闻分析。<br>
  BaiduNews.py：Search news from Baidu website. 从百度新闻里搜索相关新闻。<br>
  VectorGeneration.py：Generate semantic vectors. 生成语义向量。<br>
  NewsLocation.py：News coordinates location. 新闻坐标点定位。<br>
  NewsAnalyzing.py：News analysing. 新闻分析。<br>
  Demostration.py：Provide a demostrative news. 提供一则演示性新闻。

## Rationale
### 微信交互 Wechat Interaction
This system uses Itchat for WeChat interaction, and the server scans the QR code popped up by the program as a medium for the program background to interact with users. Users send the news topics of interest to the server's WeChat, and the program background will receive instructions and retrieve the corresponding news.<br>
本系统使用Itchat进行微信交互，测试者扫描程序弹出的二维码，作为程序后台与用户交互的媒介。用户向测试者微信发送感兴趣的新闻话题，程序后台将收到指令并进行相应新闻的检索。
### 新闻检索 News Retrieval
The background of this program receives the content to be searched by WeChat interactive transmission, and firstly crawls the relevant content from Baidu News, gets the news title, author, time, and obtains the news web page link, and then crawls the body part of news link, and then stored in the program for subsequent operations.<br>
程序后台收到微信交互传输进来的待搜索内容，先从百度新闻爬取相关内容，获取新闻标题、作者、时间，并获取新闻网页链接，再在任意新闻链接中爬取其中的正文部分，存储在程序中进行后续操作。
### 语义向量空间生成 Semantic Vector Space Generation
In order to locate the coordinates and analyze each news, we need to build a semantic vector space to represent them. We extract key sentences for each news. Each news can have multiple key sentences. All key sentences of all news generate two or more semantic similarity relationships to obtain a global semantic similarity matrix. We hope that each key sentence is represented by a vector, and the coordinate points of the news are obtained by vector normalization and addition, so the role of semantic similarity is to reflect the angular relationship between the vectors.<br>
为了给每个新闻定位坐标并分析，我们需要建立语义向量空间以表示他们。我们对每个新闻进行关键句提取，每个新闻可以有多个关键句，所有新闻的所有关键句生成两两间的语义相似度关系，得到一个全局语义相似度矩阵。我们希望通过向量来表示每个关键句，新闻的坐标点通过向量归一化相加得到，因此语义相似度的作用则是反映向量之间的角度关系。<br><br>
Because the values of the similarity matrix are not transitive, if the similarity is directly mapped to the space of 0 ° \~ 90 °, when the vector is more than two dimensions, it may not be able to produce a correct angular relationship (cannot meet the requirement of triangle inequity). For example, if only three key sentences are searched in total, a 3 × 3 similarity matrix S = matrix (1 0.1 0.9 // 0.1 1 0.8 // 0.9 0.8 1) is generated. If each key sentence represents a vector, and the angle relationship between vectors a = (1-s) × 90 °, we can obtain the angle matrix A = matrix (0 81 ° 9 ° // 81 ° 0 18 ° // 9 ° 18 ° 0).<br>
由于相似度矩阵的数值不具有传递性，因此如果直接将相似度映射到0°~90°的空间，当向量超过两维，将有可能无法产生正确的角度关系。例如，假设一共只搜索到三个关键句，生成3×3的相似度矩阵S=matrix(1 0.1 0.9//0.1 1 0.8//0.9 0.8 1)，如果每个关键句代表一个向量，那么向量之间的角度关系a=(1-s)×90°，得到角度矩阵A=matrix(0 81° 9°//81° 0 18°//9° 18° 0)。<br><br>
Among them, the angle between the third vector and the other two vectors is 9° and 18° respectively, it means that the angle between the other two vectors should be between 9° \~ 27°, but the angle between the other two vectors is 81°. Obviously, such an angular relationship cannot be drawn in the coordinate system.<br>
其中，第三个向量与另外两个向量的角度分别为9°和18°，那么另外两个向量之间的角度应该在9°\~27°之间，然而另外两个向量之间的角度为81°。显然，这样的角度关系无法在坐标系中画出。<br><br>
We found that if we let each row in the similarity matrix directly represents each vector, we can avoid generating an angular relationship, and thus directly obtain the value of the vector without contradiction. The number of dimensions of each vector is equal to the number of all vectors.<br>
我们发现，如果直接把相似度矩阵中的每一行代表每个向量，则可以避免生成角度关系，从而直接不矛盾地得到向量的值。每个向量的维数等于所有向量的个数。
### 新闻坐标点定位 News Coordinates Location
After the semantic vector space is generated, each news will be mapped into the vector space as a coordinate point. If a news has three key sentences, that is, three vectors, the coordinates of the news are the sum of these three vectors. It is worth noting that each vector needs to be normalized. Considering that the coordinates of the calibrated news not only need to look at the similarity of the news content, but also need to consider the emotions, the coordinates of each news will add a dimension of emotion.<br>
生成了语义向量空间后，每则新闻将作为一个坐标点映射在向量空间内。如果某一新闻有三个关键句即三个向量，那么这个新闻的坐标则是这三个向量的之和，值得注意的是，每加一个向量需要进行归一化处理。考虑到标定新闻的坐标不仅需要看新闻的内容相似性，也需要考虑情感，每个新闻的坐标将再添加一维情感。
### 观点聚类与分析 Viewpoint Clustering and Analyzing
After each news is mapped to the vector space, traditional data mining methods can be used for viewpoint classification and analysis. We use the Mean Shift clustering method which based on feature density, which can automatically determine the number of clusters according to the density threshold. In this program, each cluster represents a similar set of news, and there are several perspectives or viewpoints for several clusters. After the news clustering is completed, the news closest to the center point in each cluster is the most credible and representative. If a news n belongs to cluster C, the distance from this news to the cluster center point is D_n. And cluster C has m news, the sum distance from all cluster news to the cluster center point is ∑_{i = 1}^m {D_i}, then the credibility of the news R = 1 - D_n / (∑_{i = 1}^m {D_i}).<br>
每个新闻映射到向量空间后，可采用传统数据挖掘方法进行观点归类与分析。我们采用的是基于密度的Mean Shift聚类方法，可以通过密度阈值自动决定聚类的簇数。在本程序中，每个簇代表一类相似的新闻集合，有几个簇就有几种角度或观点。在新闻聚类完成之后，每一个簇中最接近中心点的新闻最可信，也最有代表性。如果某一新闻n属于簇C，这条新闻到该簇中心点的距离记为D_n，簇C有m个新闻，所有该簇新闻到该簇中心点的距离记为∑_{i=1}^m {D_i} ，则该新闻的可信度R=1-D_n/(∑_{i=1}^m {D_i})。

## Demonstration
<img src="https://github.com/RiverLeeGitHub/NewsReliability/blob/master/Demonstrations/%E4%B8%AD%E5%85%B4%E4%BA%8B%E4%BB%B6.jpg?raw=true" style="zoom:25%;" />


## Special Thanks
Other groupmates: Jean Chai, Zhibo Gu<br>
Advisor: Yinghua Fu<br>
Enthusiastic teacher: Zhiyong Ju<br>
Project Number: SH10252035<br>
University of Shanghai for Science and Technology<br>
