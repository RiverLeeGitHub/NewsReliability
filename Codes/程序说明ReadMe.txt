感谢您对本程序的兴趣，以下是程序运行的说明：

●作品名称：

  新闻可信度的评判与分析系统

●运行环境：

  Python 3.6: 安装并配置 pip
  Itchat: 微信端框架，安装命令$ pip install Itchat
  Bosonnlp: 玻森中文语义开放平台，安装命令$ pip install -U bosonnlp
  Aip: 百度开放平台，安装命令$ pip install baidu-aip

  运行时请保持网络畅通。

●程序说明：

  WechatInteraction.py：程序入口，与用户进行微信交互。
  MainLine.py：主线代码，用于调用其他模块并进行新闻分析。
  BaiduNews.py：从百度新闻里搜索相关新闻。
  VectorGeneration.py：生成语义向量。
  NewsLocation.py：新闻坐标点定位。
  NewsAnalyzing.py：新闻分析。
  Demostration.py：提供一则演示性新闻。

  程序入口为WechatInteraction.py，服务器接口角色用微信扫描程序下载的二维码登录，其他用户用微信向服务器接口角色发送需要查询的新闻主题，程序主线内容开始运行。运行过程可以在Python控制台查看，运行结果将通过服务器接口角色以微信消息方式反馈给用户。具体细节请参看“参赛作品报告”和“运行示例展示”。