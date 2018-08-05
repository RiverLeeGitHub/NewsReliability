# -*- coding: <utf-8> -*-
from __future__ import print_function, unicode_literals
import requests
import json
import re


class New:
    PressName="作者"
    Title="标题"
    RawText="正文"
    Sentences=[]
    Coordinate=[]
    # SumOfDistance=0
    Reliability=0
    URL="未知网址"
    Time="未知时间"
    Cluster=-1
    DistToCentroid=-1
    Sentiment=-1
    def __init__(self,PressName,Title,Time="未知时间",URL="",RawText="",Sentences=[]):
        self.PressName=PressName
        self.Time=Time
        self.Title=Title
        self.URL=URL
        self.RawText=RawText
        self.Sentences=Sentences
        

SUMMARY_URL = 'http://api.bosonnlp.com/summary/analysis'
# 注意：在测试时请更换为您的API Token
headers = {'X-Token': 'iVr388Im.25213.akIYrDR90nCB'}
def summary(rawtext):
    def trim(List):
        text=[]
        for i in range(len(List)):
            if len(List[i])>0:
                text.append(List[i])
        return text
    source = {
            'not_exceed': 0,
            'percentage': 0.2, # 原文的20%也不是很短，可以改成50（50字）
            'title': '',
            'content': rawtext
        }
    resp = requests.post(
        SUMMARY_URL,
        headers=headers,
        data=json.dumps(source).encode('utf-8'))
    resp.raise_for_status()
#    print(resp.text)
    text=re.split(r'[\\n|\\t]',resp.text[1:-1])
#    print("!",text)
    text=trim(text)
#    print("!@@",text)
    return text

def execute():
#    word=input('Search: ')
    news=[]
    #################################################################################
    raw_text="""中兴违反禁运协议偷偷买美国芯片给伊朗，被美国商务部抓住禁运七年的事儿大家都知道了吧？怎么被抓的呢？本来国际上有专门的中介掮客给禁运国家倒腾东西。但是中兴几个高管不舍得花钱找已经成熟的中介去卖（有说公司批了款，高管自己装腰包了），自己搞了皮包公司，结果立刻露馅。来美国打官司不舍得找好律师，找个野鸡律所，被FBI卧底打入公司内部，然后FBI卧底发现公司服务器所有的机密材料随便下载。其中一份资料是：“华为公司应付美国法律的招数有1，2，3，4。我们可以参考经验，这么这么多干”，于是FBI人赃俱获，同时给华为发了律师信，让他们解释1，2，3，4是怎么回事。美国商务部本来没有彻底封杀中兴，而是判罚9亿美元要求整改，其中一个条件是给35名违规高管发惩戒信或要求辞职。过了一段时间美国法院检查执行情况，竟然大部分涉事高管既没有辞职也没有发惩戒信。而且中兴还信誓旦旦写了两封信说自己都做了。（这也是不了解行情，国企上层不少都是由关系的，怎么可能让他辞职。）这么蠢的谎话当然很快就被拆穿，于是几十亿人民币买来的机会化为乌有，而且美国商务部也没兴趣再跟中兴玩儿了，从罚款整改到彻底封杀，因为你的行为基本上让别人没有办法再相信你。"""
    sentences=summary(raw_text)
    news.append(New(PressName="知乎",
                    Title="中兴大企业的高管们有多蠢，蠢到超出你的想象力",
                    URL="https://tieba.baidu.com/p/5655866855?red_tag=1086559008&traceid=",
                    RawText=raw_text,
                    Sentences=sentences))
    #################################################################################
    raw_text="""央广网北京4月21日消息《新闻和报纸摘要》报道，针对美国商务部此前向中兴通讯发出的7年出口权限禁令，中兴通讯昨天（20日）发布声明并召开发布会表示，制裁极不公平，中兴不能接受。中兴将加大研发投入，绝不放弃。4月16日，美国商务部一记重拳砸向中兴通讯――对涉及历史出口管制违规行为的中兴某些员工未及时扣减奖金和发出惩戒信，并以此前提交给美国政府的两份函件中对此做出虚假陈述为由，激活对中兴通讯和中兴康讯公司拒绝令的决定，即7年内禁止美国企业向中兴通讯出口任何技术、产品。中兴通讯董事长殷一民：我坚决反对美国商务部作出这样的决定，坚决反对不公平不合理的处罚，更反对把贸易问题政治化，美方将细微的问题无限扩大化，对企业造成极大影响。对此公司高度关注。公司将通过一切法律允许的手段来解决问题。中国工程院院士、工程院原副院长邬贺铨：一个政府竟然关心起一个8万多员工的企业里有30多个人的奖金是不是被扣发，而为此大动干戈，背后其实是美国认为中国通讯设备的发展已经威胁到了美国的霸主地位，所以想打击中国的高科技产业。这样的做法，对美国也会适得其反。"""
    sentences=summary(raw_text)
    news.append(New(PressName="凤凰新闻",
                    Title="中兴通讯：美禁令对中兴通讯极不公平，不能接受",
                    URL="https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_15266956208192270016%22%7D&n_type=0&p_from=1",
                    RawText=raw_text,
                    Sentences=sentences))
    #################################################################################
    raw_text="""中兴连4名高管都舍得开除，它有什么理由舍不得扣那35名普通员工的奖金呢？而且它居然冒整个公司被绝杀的风险去保那35人的奖金。美国封杀中兴事件一出，《环球时报》总编辑胡锡进始终力挺中兴。今日凌晨3点，胡锡进在微博发长文章，批评美国所谓“中兴没有扣发35名员工奖金”的封杀理由逻辑奇怪，是欲加之罪，同时对那些论证封杀中兴合理比美国还勤奋的公知，表示“服气”。中国的公知们第一时间就接受了美国的这一说法，完全不去质疑这样一个奇怪的逻辑：中兴连4名高管都舍得开除，它有什么理由舍不得扣那35名普通员工的奖金呢？而且它居然冒整个公司被绝杀的风险去保那35人的奖金。请注意，不是保那35人的饭碗呃，而是奖金!奖金!如果我们当中任何一个人是中兴的领导，会让公司冒这么大的风险而去给那35人发奖金吗？这当中一定有蹊跷。老胡给中兴的朋友打电话，他们不愿意详说。因为美国商务部的决定还没有最后生效，中国政府已经介入，中兴希望事情有转机，他们不愿意在这个时候发声。所以只能忍受那些公知舆论的肆意嘲弄。老胡今晚下夜班后和几名编辑一起查美国司法部和商务部的材料，发现，司法部2017年3月6日作出的判决中，只有要求中兴开除4名高管的条款，而只字没有提扣35员工奖金的事情。我们进一步查阅发现，虽然美国媒体近来的报道都提了35名员工奖金的事，但就是找不到在今年4月15日美商务部对中兴做绝杀处罚之前的任何法律文件中有提到那35名员工的事。是美司法部、商务部与中兴没有谈妥？是双方的理解发生了偏差？如果美国高度重视扣那35名员工奖金的事，为何不写进美司法部2017年3月6日的判决？为何不用法律文件来强调美方这一要求的严肃性？为何又在最后突然拿出这个问题当作绝杀中兴的借口？因为35人的奖金而毁掉一个8万人的大公司，是中兴有这样的愿望，还是美国太需要这样的借口了呢？这就是美国向中国高科技产业发动的一次突袭。欲加之罪，理由还能找不到吗？每一个企业都可能犯错，但是一个一年销售一千多亿的大型高科技企业，会坚持错下去，直到最后冒性价比如此荒唐的致命风险，这个故事太拽了吧!中兴显然成了中美高科技冲突的牺牲品。它作为一个企业如何能对付美国一个国家的算计!这是全球化时代，大公司的采购链都是全球性的，美国突然断供对中兴的打击可想而知。这很粗暴、霸道。我希望中国政府这次要与美方坚决交涉，搞清楚事实真相，为中兴伸张正义。中兴为中国通信业的崛起做出了巨大贡献，它做得没华为好，但它也是中国现代化的功臣。看到它遭此重击，说实话老胡心疼。我不明白那些对它说“活该”的人都是怎么回事。我也不想再骂他们了，夜深了，我把想骂的话变成了一声叹息。对于美制裁中兴一事，商务部新闻发言人高峰19日在回答记者提问时再次强调：美方行径引起了市场对美国贸易和投资环境的普遍担忧，美方的行为表面针对中国，但最终伤害的是美国自身，不仅会使其丧失数以万计的就业机会，还会影响成百上千的美国关联企业，将会动摇国际社会对美国投资和营商环境稳定的信心。希望美方不要自作聪明，否则只会自食其果。也希望美方不要低估中方的决心，如果美方坚持通过单边主义的保护政策，不惜伤害中美两国企业利益，企图遏制中国发展，迫使中国作出让步，那是打错算盘，中方坚决捍卫国家和人民利益的决心和信心不会有丝毫动摇，我们会进行坚决的斗争。"""
    sentences=summary(raw_text)
    news.append(New(PressName="环球时报",
                    Title="媒体：某些中国人现在骂“中兴活该被美国弄死” 太早了吧",
                    URL="http://finance.ifeng.com/a/20180419/16138406_0.shtml",
                    RawText=raw_text,
                    Sentences=sentences))
    #################################################################################
    raw_text="""这几天，中国公司中兴通讯被美国禁售各种零配件的新闻传播得沸沸扬扬，很多网友包括小编在内都深感我国的技术升级还有着迫切的需求。至少，在很多高科技领域，我们还需要大量的努力。中兴和华为在国外遭受的挫折，猝不及防。不过，今天看到的一篇新闻，却让人看到了中兴被美国禁售某些零部件事件中的另一面。有人说，中兴被禁购零部件的原因，竟是中兴自己作死！早在2017年3月，中兴通讯违反了美国对伊朗出口的禁令，被美国惩罚了8.9亿美元。有知道内情的人士介绍到：在当时中兴承认自己确实违反了美国的部分禁令，而且也认罚8.9亿美元的罚款。注意这个“认罚”两个字，这说明中兴自己承认违反了某些规则。所以才会认罚。除了8.9亿美元的罚金，当时美国还开出了3亿美金的罚款额度，会在七年内依据中兴的表现来确定是否执行。当时，中兴也承诺会解雇四名高级员工，并使用其他方式惩罚另外的35名员工。以上这些惩罚内容，都是中兴公司在与美国有关部门沟通后，双方认定的协议内容。然而，正如美国商务部长所说的那样：中兴在当初被美国列入‘实体名单（Entity List）’时向我们撒了谎，在后来的暂缓过程中又向我们撒了谎，最后的调查过程中，还向我们撒谎。言下之意，中兴并没有履行自己的承诺，至少没有惩罚那35名员工。嗯，这就是美国这一次惩罚中兴禁止购入美国相关核心零部件，且长达七年惩罚的原因。所以，有些人就认为，中兴这纯粹是自己作死。现在正好是中美贸易战的关键时期，中兴自己千亿规模的体量，如果因为美国禁购而倒下，对中国造成的影响难以估计。美国之前默不作声，挑着现在这个时间点来惩罚中兴，惩罚这家不遵守承诺的公司，虽然会对中国制造2025造成重大影响。可是，这说到底，还是中兴自己作的。正如某位互联网从业者说得那样：中兴通讯这件事情，在宏观层面上，和中美贸易战有没有关系，这个恐怕不好判断。但是从最简单的常理来说，一个国家的政府被一家公司以如此低劣的手段忽悠糊弄。明知故犯，答应的东西在骗人，调查期间继续顶风作案，哪怕没有中美贸易战这个事情，这只鸡不杀了给猴看，是不是全世界都可以照葫芦画瓢了呢？所以中兴通讯被美国禁购主要零部件，说起来还是活该！"""
    sentences=summary(raw_text)
    news.append(New(PressName="搜狐",
                    Title="撒谎成性！撒谎成性！中兴被美禁购，原来是活该",
                    URL="http://www.sohu.com/a/228632555_100088233",
                    RawText=raw_text,
                    Sentences=sentences))
    
    for i in range(len(news)):
        news[i].Sentences.append(news[i].Title)
    return news
    