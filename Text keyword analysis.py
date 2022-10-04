# 开发时间：2021/9/18  9:15
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
    def parse_text(self):
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
    def output(self):
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
    def color_to_color_value(self, value):
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
            self.color_temp.append(self.color_to_color_value(col))

    # 主函数
    def main(self):
        self.parse_text()
        self.sort_content()
        self.output()
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

