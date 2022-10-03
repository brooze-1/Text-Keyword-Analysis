## 🍾文本关键词分析脚本

### 1、🍗文本分析功能

这个文本分析功能最开始是因为当时老师让我们最近写文章，然后好的文章不是都有关键词吗，所以在写完文章之后我想写个脚本**分析全文**总结出全文中**出现频率最高的词**作为文章的关键词🤔，说干就干好吧👻！
然后我就花时间写了个类，代码在下面：

```python
# coding:utf-8
import jieba

# TKA代表着Text Keyword Analysis
class TKA(object):
    def __init__(self, filename, len_keywords=2, list_keywords=10, up_or_down=True):
        # 注意传入的文件类型参数要是txt类型
        self.filepath=filename
        file = open("wait_to_analysis/" + self.filepath, "r", encoding="utf-8")
        self.content = file.read()
        file.close()

        # len_keywords(int)参数是用于筛选关键字长度大于等于len_keywords的关键字,默认值为3
        self.len_keywords=len_keywords
        # list_keywords(int)参数是默认的展示的关键字条数以及存储的关键字条数，默认值为10，当真实关键字条数小于list_keywords，将真实关键字条数赋值给list_keywords
        self.list_keywords=list_keywords
        # up_or_down(bool)参数用来选择是升序排列还是降序排列，升序和降序是相对于关键字在文章中的出现次数来排序的(up_or_down的类型是bool类型)，传入True表示升序,传入False表示降序，默认是True
        self.up_or_down=up_or_down
        # self.d用于临时存储解析的文本
        self.d={}

    # 解析文本获取关键字及其出现次数
    def Parse_text(self):
        # 使用jieba库的lcut方法对文本内容进行分词，生成列表对象
        words = jieba.lcut(self.content)
        for word in words:
            # 若关键字长度小于len_keywords则跳过
            if len(word) < self.len_keywords:
                continue
            # 关键字长度大于等于len_keywords时，则存储至临时字典d中
            else:
                self.d[word] = self.d.get(word,0) + 1


    # 对关键字进行排序
    def sort_content(self):
        # 生成列表对象
        self.items = list(self.d.items()) # 形如[("jason",8),("egon",6)...]
        # print(self.items)
        # print(len(self.items))
        self.tmp_items = list(self.d)
        # print(self.tmp_items)
        # 按照关键字出现的次数进行关键字的排序
        self.items.sort(key=lambda x:x[1],reverse=self.up_or_down)


    # 输出分析结果
    def input(self):
        # list_keywords(int)参数是默认的展示条数以及存储条数当真实数据条数小于list_keywords，将数据的长度赋值给list_key_words
        if len(self.items) < self.list_keywords:
            self.list_keywords = len(self.items)
        for i in range(self.list_keywords):
            k,v = self.items[i]
            if i<self.list_keywords - 1:
                print("{}:{}".format(k,v),end=",")
            else:
                print("{}:{}".format(k,v))


    # 将分析结果存储至文件中
    def up_to_file(self):
        # 处理filename
        self.filepath = ".".join(self.filepath.split("."))
        f1=open("analysis_result/" + self.filepath, "w", encoding="utf-8")
        if len(self.items) < self.list_keywords:
            self.list_keywords = len(self.items)
        for i in range(self.list_keywords):
            k,v = self.items[i]
            f1.write("{}:{}\n".format(k,v))
        f1.close()


    # 主函数
    def main(self):
        self.Parse_text()
        self.sort_content()
        self.input()
        self.up_to_file()

if __name__=="__main__":
    filename = "test.txt"   # 注意文件名要带后缀 默认只处理txt文件
    obj = TKA(filename=filename)
    obj.main()
```

(☞ﾟヮﾟ)☞首先**使用该代码之前需要先在代码文件的同级目录之下创建wait_to_analysis和analysis_result这两个文件夹**，**wait_to_analysis**文件夹用于**存放待分析txt文件**，**analysis_result**文件夹**用于存储分析后的结果txt文件**📢。

然后**当前的TKA**类有**四个参数**：

- **filename** - filename(str)文件名，==注意==**只要输入文件名即可**哈！因为在代码中默认是从wait_to_analysis文件下下读取待分析的txt文件，但是要**记得带上文件后缀**，例："test.txt"，可千万别写成了"./wait_to_analysis/test.txt"。
- **len_keywords** - len_keywords(int)参数是用于**筛选关键词长度大于等于len_keywords的关键词**,默认值为3，即默认筛选长度大于3的关键词，就是**筛选出大于指定长度的关键词**。
- **list_keywords** - list_keywords(int)参数是设**置展示的关键词条数以及存储的关键词条数**，默认值为10，即默认展示和存储前10个关键词，当真实关键词条数小于list_keywords，将真实关键词条数赋值给list_keywords。
- **up_or_down** - up_or_down(bool)参数**用来选择是升序排列还是降序排列**，升序和降序是相对于关键词在文章中的出现次数来排序的(up_or_down的类型是bool类型)，传入True表示升序,传入False表示降序，默认是True。

**📽效果演示：**
测试文章：

```
总书记曾说：“一代人有一代人的长征，一代人有一代人的担当。”当代青年应继先辈之信念，振吾辈之中国。作为复兴中学的一员响应时代的号召，选择热爱事业，推动创新，展望未来。
不久前，中央广播电视台连续播放了一组微纪录片，那是为中国共产主义青年团成立100周年而作的专题，展现了一位位现实人物从学生时代，到青年，到有所成就的人生历程。纪录片中的每一个片段、每一个人物都深深地打动了我。
科学家不断完善新思维，获取新知识，以实现北斗导航系统的创新与应用，同时不忘培育下一代的科学素养；摄影家致力于民族文化的传承，让我们建立起文化自信与发展意识；建筑家把理想与人文精神赋予一件件作品，艺术地体现了人与自然、生活与精神的和谐和持续发展。他们从学生向贡献者跨越的、活生生的青春轨迹，深深地刻在我的头脑中，把我拉进现实，使我多夜难眠。
人生归我，但生而为人，不仅是自我，一份社会责任担当，一份与自然和谐发展的愿望，一份积于内心的情感幻化成未来有所作为的力量，才是人生航程中现实的风帆，伴其远航。
心中有信仰，脚下有力量。
63年前，第一代东风人凭借着革命加拼命的精神，住帐篷、睡地窝、饮苦水、吃干菜，顶风冒沙，战天斗地，在茫茫大漠深处创建发射场。这种“特别能吃苦、特别能战斗、特别能攻关、特别能奉献”的精神，在新时代的东风人身上依然清晰可见。63年来，千千万万有志儿女从祖国各地奔赴西北戈壁，在大漠献青春、献终身，让青春在党和人民最需要的地方绚烂绽放。
现在，历史的接力棒已经交到新时代航天人的手中，建设航天强国使命在肩，弘扬航天精神薪火相传。在新的征程上，每一个青年都应担负起自己的使命，让自己的青春在为祖国、为人民的奉献中绽放光彩。我们有理由坚信，有党的领导和全国人民的支持，有伟大航天精神的激励，有一代代中国航天人接续奋斗，一定能够实现航天强国的梦想，开创更加美好的明天！
一代人有一代人的长征路。不能躺在前辈的功劳簿上踟蹰不前，在最好的时代，应该策马扬鞭，撸起袖子加油干；跨越险阻艰难，再谱傲娇向未来。到时候：美丽画卷轻舒展，待我青年自翩跹。国家强盛看巨变，民族复兴开心颜！
```

保存的结果：

```
一代人:6
纪录片:2
深深地:2
总书记:1
复兴中学:1
展望未来:1
不久前:1
电视台:1
中国共产主义青年团:1
100:1
```

<center><img src="https://img-blog.csdnimg.cn/dcac3b06217a44528d5be53259bd110f.gif" width="90%"></center>

### 2、🍖生成词云功能

这个生成词云功能，当时我刚好备考计算机二级来着🙃，然后又学习到这方面的相关知识，所以就当练练手把这个功能加上了，前面不是统计了关键词出现的次数嘛，然后就想着**根据**这个**关键词以及关键词的次数来生成一个酷酷的词云**😎。我上面不是有一个设置升序还是降序的功能嘛，**关键词**出现的**次数越多**，**升序**排的话就排在**越前面**，到时候在词云中**生成的字**也就**越大**，**出现次数少的，就会排在后面，在词云中生成的字也就越小**😏。

然后生成词云这个功能就在上面文本分析功能的代码上做了些修改：

```python
# coding:utf-8
import jieba
from wordcloud import WordCloud
from scipy.misc import imread
from matplotlib import colors


class TKA(object):
    def __init__(self,filename,color_list,color_sizes="black",len_keywords=3,list_keywords=10,max_font_size=40,img_templates="cat.png",up_or_down=True,create_png=True,font_path="./词云字体/simhei.ttf"):
        # filename(str)文件名，注意只要输入文件名即可哈！因为在代码中默认是从wait_to_analysis文件下下读取待分析的txt文件，但是要记得带上文件后缀，例："test.txt"，可千万别写成了"./wait_to_analysis/test.txt"。
        self.filename=filename
        file = open("wait_to_analysis/" + self.filename, "r", encoding="utf-8")
        self.content = file.read()
        file.close()

        # len_keywords(int)参数是用于筛选关键字长度大于等于len_keywords的关键字,默认值为3，即默认筛选长度大于3的关键字，就是筛选出大于指定长度的关键字。
        self.len_keywords=len_keywords
        # list_keywords(int)参数是默认的展示的关键字条数以及存储的关键字条数，默认值为10，即默认展示和存储前10个关键字，当真实关键字条数小于list_keywords，将真实关键字条数赋值给list_keywords。
        self.list_keywords=list_keywords
        # up_or_down(bool)参数用来选择是升序排列还是降序排列，升序和降序是相对于关键字在文章中的出现次数来排序的(up_or_down的类型是bool类型)，传入True表示升序,传入False表示降序，默认是True。
        self.up_or_down=up_or_down
        # self.d用于临时存储解析的文本
        self.d={}
        # img_templates(.png)参数用于接受生成词云的模板，声明img_template支持传入列表，当传入的参数为列表时，则会生成多张不同模板的词云图片。
        self.img_templates = img_templates
        # create_png(bool)参数用来选择是否要生成词云，默认是False，表示不生成词云图片，若为True，则会生成词云图片并保存在img_result文件夹下。
        self.create_png = create_png
        # self.d用于临时存储解析的文本
        # 用于存放色号,声明color_sizes支持传入列表 self.color_size适用于存放背景板的颜色 背景板需求的颜色格式是(221,204,210)这样的rgb格式，传入的对象是列表对象(list)。当传入的列表中只有1个颜色时智慧生成一张单色背景的图片，若列表中有3个背景色，则会生成三张不同背景色的图片。
        self.color_sizes = color_sizes
        # max_font_size用于确定形成的词云的字体大小,默认最大字体大小等于30。
        self.max_font_size = max_font_size
        # 建立字体颜色数组，传入的是列表对象(list)，当列表中只有一个颜色时只会生成一张单色字体的图片，若列表中有3个颜色时，则会生成一张含3种字体颜色的词云图片。
        self.color_list = color_list
        # self.color_temp用于存储self.color_list转换好的色号   (221,204,210) => '#DDCCD2' 将rgb色号转成16进制  转换成16进制是因为字体需求的颜色样式是16进制
        self.color_temp = []
        # self.font_path用于设置词云字体的样式，传入字体所在的路径即可，默认是词云字体文件夹下的simhei.ttf字体
        self.font_path = font_path

    # 解析文本获取关键字及其出现次数
    def Parse_text(self):
        # 使用jieba库的lcut方法对文本内容进行分词，生成列表对象
        words = jieba.lcut(self.content)
        for word in words:
            # 若关键字长度小于len_keywords则跳过
            if len(word) < self.len_keywords:
                continue
            # 关键字长度大于等于len_keywords时，则存储至临时字典d中
            else:
                self.d[word] = self.d.get(word,0) + 1


    # 对关键字进行排序
    def sort_content(self):
        # 生成列表对象
        self.items = list(self.d.items()) # 形如[("jason",8),("egon",6)...]
        # print(self.items)
        # print(len(self.items))
        self.tmp_items = list(self.d)
        # print(self.tmp_items)
        # 按照关键字出现的次数进行关键字的排序
        self.items.sort(key=lambda x:x[1],reverse=self.up_or_down)


    # 输出分析结果
    def input(self):
        # list_keywords(int)参数是默认的展示条数以及存储条数当真实数据条数小于list_keywords，将数据的长度赋值给list_key_words
        if len(self.items) < self.list_keywords:
            self.list_keywords = len(self.items)
        for i in range(self.list_keywords):
            k,v = self.items[i]
            if i<self.list_keywords - 1:
                print("{}:{}".format(k,v),end=",")
            else:
                print("{}:{}".format(k,v))


    # 将分析结果存储至文件中
    def up_to_file(self):
        # 处理filename
        self.filename = ".".join(self.filename.split("."))
        f1=open("analysis_result/" + self.filename, "w", encoding="utf-8")
        if len(self.items) < self.list_keywords:
            self.list_keywords = len(self.items)
        for i in range(self.list_keywords):
            k,v = self.items[i]
            f1.write("{}:{}\n".format(k,v))
        f1.close()

    # 当self.img_templates传入的是列表时，判断传入的color_sizes是列表还是字符串
    def judge_color_sizes(self, img_template, lines):
        mask = imread("img_template/" + img_template)
        # 当传入的color_sizes是列表时
        if type(self.color_sizes) == list:
            # 遍历改变背景颜色
            for color in self.color_sizes:
                wc = WordCloud(background_color=color, font_path=self.font_path,
                               max_font_size=self.max_font_size,
                               mask=mask, colormap=self.colormap).generate(lines)
                # 文件命名方式：文件名+词云字体大小+使用的词云模板名+背景色号
                wc.to_file("img_result/{}({}{}{}).png".format(self.filename.split(".")[0], self.max_font_size,
                                                              img_template.split(".")[0], color))
        else:
            # 当传入的color_sizes是字符串时
            wc = WordCloud(background_color=self.color_sizes, font_path=self.font_path,
                           max_font_size=self.max_font_size,
                           mask=mask, colormap=self.colormap).generate(lines)
            # 文件命名方式：文件名+词云字体大小+使用的词云模板名+背景色号
            wc.to_file("img_result/{}({}{}{}).png".format(self.filename.split(".")[0], self.max_font_size,
                                                          img_template.split(".")[0], self.color_sizes))

    # 当self.img_templates传入的是字符串时判断传入的color_sizes是列表还是字符串
    def judge_color_sizes2(self, lines):
        mask = imread("img_template/" + self.img_templates)
        # 当传入的color_sizes是列表时
        if type(self.color_sizes) == list:
            # 遍历改变背景颜色
            for color in self.color_sizes:
                wc = WordCloud(background_color=color, font_path=self.font_path,
                               max_font_size=self.max_font_size,
                               mask=mask, colormap=self.colormap).generate(lines)
                # 文件命名方式：文件名+词云字体大小+使用的词云模板名+背景色号
                wc.to_file("img_result/{}({}{}{}).png".format(self.filename.split(".")[0], self.max_font_size,
                                                              self.img_templates.split(".")[0], color))
        else:
            # 当传入的color_sizes是字符串时
            wc = WordCloud(background_color=self.color_sizes, font_path=self.font_path,
                           max_font_size=self.max_font_size,
                           mask=mask, colormap=self.colormap).generate(lines)
            # 文件命名方式：文件名+词云字体大小+使用的词云模板名+背景色号
            wc.to_file("img_result/{}({}{}{}).png".format(self.filename.split(".")[0], self.max_font_size,
                                                          self.img_templates.split(".")[0], self.color_sizes))

    # 生成词云
    def generate_wordcloud(self):
        if self.create_png:
            # 转化为ListedColormap对象作为字体颜色的参数传入
            self.colormap = colors.ListedColormap(self.color_temp)
            lines = " ".join(self.tmp_items)
            # print(lines)
            # 当传入self.img_templates是个列表时进行判断(即传入了多个模板图片时)
            if type(self.img_templates) == list:
                # 对传入的图片进行循环
                for img_template in self.img_templates:
                    # mask = imread("img_template/"+img_template)
                    # # 莫兰迪配色 (104,84,85) (164,164,164)
                    # wc = WordCloud(background_color=(104,84,85),font_path=self.font_path, max_font_size=50, mask=mask).generate(lines)
                    # # 文件命名方式：文件名+使用的词云模板名
                    # wc.to_file("img_result/{}({}).png".format(self.filename.split(".")[0],img_template.split(".")[0]))
                    self.judge_color_sizes(img_template, lines)
            # 当只传入了一个图片时
            else:
                # mask = imread("img_template/"+self.img_templates)
                # wc = WordCloud(background_color=(104,84,85),font_path=self.font_path, max_font_size=50, mask=mask).generate(lines)
                # wc.to_file("img_result/{}({}).png".format(self.filename.split(".")[0],self.img_templates.split(".")[0]))
                self.judge_color_sizes2(lines)
        else:
            return

    # (221,204,210) => '#DDCCD2' 将rgb色号转成16进制
    def Color_to_color_value(self, value):
        digit = list(map(str, range(10))) + list("ABCDEF")
        if isinstance(value, tuple):
            string = '#'
            for i in value:
                a1 = i // 16
                a2 = i % 16
                string += digit[a1] + digit[a2]
            return string
        elif isinstance(value, str):
            a1 = digit.index(value[1]) * 16 + digit.index(value[2])
            a2 = digit.index(value[3]) * 16 + digit.index(value[4])
            a3 = digit.index(value[5]) * 16 + digit.index(value[6])
            return (a1, a2, a3)

    # 重复操作Color_to_color_value()函数直至列表中所有的色号都转成16进制
    def repeated_color_convert(self):
        # 遍历将color_list中的rgb色号都转换成16进制存储至color_temp中
        for col in self.color_list:
            self.color_temp.append(self.Color_to_color_value(col))

    # 主函数
    def main(self):
        self.Parse_text()
        self.sort_content()
        self.input()
        self.up_to_file()
        self.repeated_color_convert()
        self.generate_wordcloud()


if __name__=="__main__":
    filename = "test.txt"   # 注意文件名要带后缀 默认只处理txt文件
    # color_sizes存储用于背景板的颜色
    color_sizes = [
        (60, 112, 126), (79, 96, 112), (122, 103, 131)
    ]
    # color_list存储用于词云字体的颜色
    color_list = [
        (221, 204, 210), (213, 208, 204), (237, 209, 205)
    ]
    img_templates = ["cat.png","heart.png","thumb.png"]
    obj = TKA(filename=filename,color_list=color_list,color_sizes=color_sizes,img_templates=img_templates)
    obj.main()



```

(☞ﾟヮﾟ)☞首先**使用该代码之前需要先在代码文件的同级目录之下创建wait_to_analysis、analysis_result、img_result、img_template和词云字体这五个文件夹**，**wait_to_analysis**文件夹用于存放待分析txt文件，**analysis_result**文件夹用于存储分析后的结果txt文件，**img_result**文件夹用于存储生成的词云图片，**img_template**文件夹用于存储词云的图片模板，**词云字体**文件夹用于存储生成词云的字体📢。

然后**当前的TKA类有十个参数**：

- **filename** - filename(str)文件名，==注意==**只要输入文件名即可**哈！因为在代码中默认是从wait_to_analysis文件下下读取待分析的txt文件，但是要**记得带上文件后缀**，例："test.txt"，可千万别写成了"./wait_to_analysis/test.txt"。
- **len_keywords** - len_keywords(int)参数是用于**筛选关键词长度大于等于len_keywords的关键词**,默认值为3，即默认筛选长度大于3的关键词，就是**筛选出大于指定长度的关键词**。
- **list_keywords** - list_keywords(int)参数是设**置展示的关键词条数以及存储的关键词条数**，默认值为10，即默认展示和存储前10个关键词，当真实关键词条数小于list_keywords，将真实关键词条数赋值给list_keywords。
- **up_or_down** - up_or_down(bool)参数**用来选择是升序排列还是降序排列**，升序和降序是相对于关键词在文章中的出现次数来排序的(up_or_down的类型是bool类型)，传入True表示升序,传入False表示降序，默认是True。
- **color_list** - **建立字体颜色数组，传入的是列表对象(list)**，当列表中只有一个颜色时只会生成一张单色字体的图片，若列表中有3个颜色时，则会生成一张含3种字体颜色的词云图片。
- **color_sizes** - **用于图片背景存放色号**,声明color_sizes支持传入列表，color_size适用于存放背景板的颜色 背景板需求的颜色格式是(221,204,210)这样的rgb格式，传入的对象是列表对象(list)。当传入的列表中只有1个颜色时智慧生成一张单色背景的图片，若列表中有3个背景色，则会生成三张不同背景色的图片。
- **max_font_size** - **max_font_size用于确定形成的词云的字体大小**,默认最大字体大小等于30。
- **img_templates** - **img_templates(.png)参数用于接受生成词云的模板**，声明img_template支持传入列表，当传入的参数为列表时，则会生成多张不同模板的词云图片，==注意==img_templates传入参数时，首先现将词云模板放在img_template文件夹下，传参的时候就只需要写模板名即可，不需要在加上路径，因为在代码中已经是自动从img_template这个文件夹下加载图片模板的，例"cat.png",千万不要写成"./img_template/cat.png"，也不要忘了写后缀。
- **create_png** - create_png(bool)参数用来选择是否要生成词云图片，默认是False，表示不生成词云图片，若为True，则会生成词云图片并保存在img_result文件夹下。
- **font_path** - **font_path用于设置词云字体的样式**，传入字体所在的路径即可，默认是词云字体文件夹下的simhei.ttf字体

==注意==当color_sizes传入3个背景色，img_templates传入3个词云模板时则会生成9张词云图片，分别是不同背景色和不同词云模板的组合。

**📽效果演示：**
测试文章：

```
总书记曾说：“一代人有一代人的长征，一代人有一代人的担当。”当代青年应继先辈之信念，振吾辈之中国。作为复兴中学的一员响应时代的号召，选择热爱事业，推动创新，展望未来。
不久前，中央广播电视台连续播放了一组微纪录片，那是为中国共产主义青年团成立100周年而作的专题，展现了一位位现实人物从学生时代，到青年，到有所成就的人生历程。纪录片中的每一个片段、每一个人物都深深地打动了我。
科学家不断完善新思维，获取新知识，以实现北斗导航系统的创新与应用，同时不忘培育下一代的科学素养；摄影家致力于民族文化的传承，让我们建立起文化自信与发展意识；建筑家把理想与人文精神赋予一件件作品，艺术地体现了人与自然、生活与精神的和谐和持续发展。他们从学生向贡献者跨越的、活生生的青春轨迹，深深地刻在我的头脑中，把我拉进现实，使我多夜难眠。
人生归我，但生而为人，不仅是自我，一份社会责任担当，一份与自然和谐发展的愿望，一份积于内心的情感幻化成未来有所作为的力量，才是人生航程中现实的风帆，伴其远航。
心中有信仰，脚下有力量。
63年前，第一代东风人凭借着革命加拼命的精神，住帐篷、睡地窝、饮苦水、吃干菜，顶风冒沙，战天斗地，在茫茫大漠深处创建发射场。这种“特别能吃苦、特别能战斗、特别能攻关、特别能奉献”的精神，在新时代的东风人身上依然清晰可见。63年来，千千万万有志儿女从祖国各地奔赴西北戈壁，在大漠献青春、献终身，让青春在党和人民最需要的地方绚烂绽放。
现在，历史的接力棒已经交到新时代航天人的手中，建设航天强国使命在肩，弘扬航天精神薪火相传。在新的征程上，每一个青年都应担负起自己的使命，让自己的青春在为祖国、为人民的奉献中绽放光彩。我们有理由坚信，有党的领导和全国人民的支持，有伟大航天精神的激励，有一代代中国航天人接续奋斗，一定能够实现航天强国的梦想，开创更加美好的明天！
一代人有一代人的长征路。不能躺在前辈的功劳簿上踟蹰不前，在最好的时代，应该策马扬鞭，撸起袖子加油干；跨越险阻艰难，再谱傲娇向未来。到时候：美丽画卷轻舒展，待我青年自翩跹。国家强盛看巨变，民族复兴开心颜！
```

保存的结果：

```
一代人:6
纪录片:2
深深地:2
总书记:1
复兴中学:1
展望未来:1
不久前:1
电视台:1
中国共产主义青年团:1
100:1
```

词云模板：

<center><img src="https://img-blog.csdnimg.cn/632bda2bdb33467dbe8231c400d00cc8.png" width="80%"></center>

生成的词云：

<center><img src="https://img-blog.csdnimg.cn/69498960fae248c3bbdec642f6fc90d6.png" width="80%"></center>

## 🍌项目目录结构

```

----文字关键字分析\
    |----analysis_result\      # 存储文本分析的结果
    |    |----readme
    |    |----test.txt   
    |----img_result\           # 存放生成的词云图片
    |    |----test(40cat(122, 103, 131)).png
    |    |----test(40cat(60, 112, 126)).png
    |    |----test(40cat(79, 96, 112)).png
    |    |----test(40heart(122, 103, 131)).png
    |    |----test(40heart(60, 112, 126)).png
    |    |----test(40heart(79, 96, 112)).png
    |    |----test(40thumb(122, 103, 131)).png
    |    |----test(40thumb(60, 112, 126)).png
    |    |----test(40thumb(79, 96, 112)).png
    |----img_template\        # 存放词云的图片模板
    |    |----cat.png
    |    |----heart.png
    |    |----readme
    |    |----thumb.png
    |----README.md
    |----requirements.txt
    |----Text keyword analysis.py  # 主函数
    |----wait_to_analysis\         # 存储待分析的txt文件
    |    |----readme.md
    |    |----test.txt
    |----词云字体\                  # 存储生成词云的字体
    |    |----simhei.ttf     
```



==注意== **生成的词云图片命名**为：待分析文本的文件名+词云字体大小+使用的词云模板名+背景色号，生成词云的关键词是筛选之后所有的关键词🍕。

<center><img src="https://img-blog.csdnimg.cn/33e9a81466204a06bedd8ad75075dcec.gif" width="90%"></center>



## 🌭脚本的发文平台及开源平台

[github仓库地址🙈](https://github.com/brooze-1/Text-Keyword-analysis)<br>[gitee仓库地址🙉](https://gitee.com/booze_place/Text-Keyword-Analysis)<br>
[博客首页🙊](https://blog.csdn.net/booze_/article/details/127146221)<br>



## ☕请我喝卡布奇诺

如果本仓库对你有帮助，可以请作者喝杯卡布奇诺☜(ﾟヮﾟ☜)

<center><img src="https://user-images.githubusercontent.com/112611204/192464009-5ecf272b-c818-4fff-9569-7f3d42d5042b.png" width="40%"></center>



