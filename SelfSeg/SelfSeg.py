# -*- coding: utf-8 -*-
import codecs
import re
import sys

# 返回预分割汉字字串的首位位置，如[(0,8),(11,12),(13,20),(24,31)]
def pre_seg(content):
    i = 0
    ct_begin = 0
    ct_end = 0
    segment = []    #用来保存汉字字串的首位位置[(0,8),(11,12),(13,20),(24,31)]

    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

    while(i < len(content)):
        #如果是汉字
        if(zhPattern.search(content[i])):
            i += 1
        #如果不是汉字
        else:
            ct_end = i
            segment.append((ct_begin, ct_end))
            while (i < len(content)):
                #如果不是汉字
                if (not zhPattern.search(content[i])):
                    i += 1
                #如果是汉字
                else:
                    ct_begin = i
                    i += 1
                    break


    return segment


# 返回根据pre_seg的首位位置列表得出的汉字字串，如['英国外相斯特劳对','说','英国可能将会在','年举办英国斯特劳公民投票']
def pre_seg_str(segment, content):
    s = []
    for i in range(len(segment)):
        s.append(content[segment[i][0]:segment[i][1]])

    return s


# 返回字符串的list，如['英国', '斯特劳', ...]
def str_list(temp_thesaurus):
    strList = []
    for i in range(len(temp_thesaurus)):
        strList.append(temp_thesaurus[i][0])
    return strList


# 返回出现次数大于等于2的ngram的列表
def calculate_ngram(s):
    ini_ngram_list = []
    ngram_list = []

    for i in range(len(s)):
        # 2-gram到5-gram
        for j in range(2, 16):
            # 在s[i]中摘取j-gram
            for k in range(len(s[i]) - j):
                if s[i][k:k + j] in str_list(ini_ngram_list):
                    ini_ngram_list[str_list(ini_ngram_list).index(s[i][k:k + j])][2] += 1
                else:
                    ini_ngram_list.append([s[i][k:k + j], j, 1, i])

    for i in range(len(ini_ngram_list)):
        if ini_ngram_list[i][2] >= 2:
            ngram_list.append(ini_ngram_list[i])

    return ngram_list


def three_characters(ngram_list, i, j):
    # i+1gram在jgram中，且i，i+1与jgram出现的次数均相等，i，i+1与jgram的长度分别为2，2，3
    if ngram_list[i + 1][0] in ngram_list[j][0] and ngram_list[i][2] == ngram_list[i + 1][2] and ngram_list[i][1] == 2 and ngram_list[j][1] == 3:
        #print(ngram_list[j][0])
        return True
    else:
        return False


def four_characters(ngram_list, i, j):
    # i+1gram在jgram中，且i，i+1与jgram出现的次数均相等，i，i+1与jgram的长度分别为3，3，4
    if ngram_list[i + 1][0] in ngram_list[j][0] and ngram_list[i][2] == ngram_list[i + 1][2] and ngram_list[i][1] == 3 and ngram_list[j][1] == 4:
        return True
    else:
        return False


def five_characters(ngram_list, i, j):
    # i+1gram在jgram中，且i，i+1与jgram出现的次数均相等，i，i+1与jgram的长度分别为4，4，5
    if ngram_list[i + 1][0] in ngram_list[j][0] and ngram_list[i][2] == ngram_list[i + 1][2] and ngram_list[i][1] == 4 and ngram_list[j][1] == 5:
        return True
    else:
        return False


def six_characters(ngram_list, i, j):
    # i+1gram在jgram中，且i，i+1与jgram出现的次数均相等，i，i+1与jgram的长度分别为5，5，6
    if ngram_list[i + 1][0] in ngram_list[j][0] and ngram_list[i][2] == ngram_list[i + 1][2] and ngram_list[i][1] == 5 and ngram_list[j][1] == 6:
        return True
    else:
        return False


# 返回清除类似‘斯特’‘特劳’这些gram后的列表
def eliminate_ngram(ngram_list):
    final_thesaurus = []

    # 把类似‘斯特’‘特劳’‘斯特劳’这些gram清为‘’‘’‘斯特劳’，即考虑不同长度gram之间的关系
    for i in range(len(ngram_list)):
        for j in range(i, len(ngram_list)):
            # 如果长的出现多，则保留长的gram
            if ngram_list[i][0] != '' and ngram_list[j][0] != '' and ngram_list[i][1] < ngram_list[j][1] and ngram_list[i][0] in ngram_list[j][0] and ngram_list[i][2] < ngram_list[j][2]:
                #print('del ', ngram_list[i], '  ', ngram_list[i][0], ' < ',  ngram_list[j][0])

                ngram_list[i][0] = ''
                ngram_list[i][1] = 0
                ngram_list[i][2] = 0
            # 如果短的出现多，则保留短的gram
            elif ngram_list[i][0] != '' and ngram_list[j][0] != '' and ngram_list[i][1] < ngram_list[j][1] and ngram_list[i][0] in ngram_list[j][0] and ngram_list[i][2] > ngram_list[j][2]:
                #print('del ', ngram_list[j], '  ', ngram_list[i][0], ' > ', ngram_list[j][0])
                ngram_list[j][0] = ''
                ngram_list[j][1] = 0
                ngram_list[j][2] = 0
            # 如果出现的次数一致，则保留短的gram
            elif ngram_list[i][0] != '' and ngram_list[j][0] != '' and ngram_list[i][1] < ngram_list[j][1] and ngram_list[i][0] in ngram_list[j][0] and ngram_list[i][2] == ngram_list[j][2]:
                # 如果是三字固定词abc，即ab和bc和abc出现的次数相同，则去除ab，bc
                if three_characters(ngram_list, i, j):
                    #print('del3', ngram_list[i], '  ', ngram_list[i + 1], '  ', ngram_list[i][0], ' = ', ngram_list[j][0])
                    ngram_list[i][0] = ''
                    ngram_list[i][1] = 0
                    ngram_list[i][2] = 0
                    ngram_list[i + 1][0] = ''
                    ngram_list[i + 1][1] = 0
                    ngram_list[i + 1][2] = 0
                # 如果是四字固定词abcd，即abc和bcd和abcd出现的次数相同，则去除abc，bcd
                elif four_characters(ngram_list, i, j):
                    #print('del4', ngram_list[i], '  ', ngram_list[i + 1], '  ', ngram_list[i][0], ' = ', ngram_list[j][0])
                    ngram_list[i][0] = ''
                    ngram_list[i][1] = 0
                    ngram_list[i][2] = 0
                    ngram_list[i + 1][0] = ''
                    ngram_list[i + 1][1] = 0
                    ngram_list[i + 1][2] = 0
                # 如果是五字固定词abcde，即abcd和bcde和abcde出现的次数相同，则去除abcd，bcde
                elif five_characters(ngram_list, i, j):
                    #print('del5', ngram_list[i], '  ', ngram_list[i + 1], '  ', ngram_list[i][0], ' = ', ngram_list[j][0])
                    ngram_list[i][0] = ''
                    ngram_list[i][1] = 0
                    ngram_list[i][2] = 0
                    ngram_list[i + 1][0] = ''
                    ngram_list[i + 1][1] = 0
                    ngram_list[i + 1][2] = 0
                # 如果是六字固定词abcdef，即abcde和bcdef和abcdef出现的次数相同，则去除abcde，bcdef
                elif six_characters(ngram_list, i, j):
                    #print('del6', ngram_list[i], '  ', ngram_list[i + 1], '  ', ngram_list[i][0], ' = ', ngram_list[j][0])
                    ngram_list[i][0] = ''
                    ngram_list[i][1] = 0
                    ngram_list[i][2] = 0
                    ngram_list[i + 1][0] = ''
                    ngram_list[i + 1][1] = 0
                    ngram_list[i + 1][2] = 0
                else:
                    #print('dele', ngram_list[j], '  ', ngram_list[i][0], ' = ', ngram_list[j][0])
                    ngram_list[j][0] = ''
                    ngram_list[j][1] = 0
                    ngram_list[j][2] = 0
            else:
                continue

    # 把类似‘网络’‘络安’‘安全’这些gram清为‘网络’‘’‘安全’，即考虑相同长度gram之间的关系
    for i in range(len(ngram_list)):
        # 如果出现的次数既比左边的大，有比右边的大
        if 0 < i < len(ngram_list) - 1 and ngram_list[i][0] != '' and ngram_list[i][2] > ngram_list[i + 1][2] and ngram_list[i][2] > ngram_list[i - 1][2]:
            ngram_list[i + 1][0] = ''
            ngram_list[i + 1][1] = 0
            ngram_list[i + 1][2] = 0
            ngram_list[i - 1][0] = ''
            ngram_list[i - 1][1] = 0
            ngram_list[i - 1][2] = 0
        # 如果左边的出现次数为0（实际上是被清空了），且右边的次数没比自己大，则清空右边的
        elif 0 < i < len(ngram_list) - 1 and ngram_list[i][0] != '' and ngram_list[i - 1][2] == 0 and ngram_list[i][2] >= ngram_list[i + 1][2]:
            ngram_list[i + 1][0] = ''
            ngram_list[i + 1][1] = 0
            ngram_list[i + 1][2] = 0
        # 如果右边的出现次数为0（实际上是被清空了），且左边的次数没比自己大，则清空左边的
        elif 0 < i < len(ngram_list) - 1 and ngram_list[i][0] != '' and ngram_list[i + 1][2] == 0 and ngram_list[i][2] >= ngram_list[i - 1][2]:
            ngram_list[i + 1][0] = ''
            ngram_list[i + 1][1] = 0
            ngram_list[i + 1][2] = 0
        # 特别针对第一个gram的处理
        elif i == 0 and ngram_list[i][0] != '' and ngram_list[i][2] > ngram_list[i + 1][2]:
            ngram_list[i + 1][0] = ''
            ngram_list[i + 1][1] = 0
            ngram_list[i + 1][2] = 0
        else:
            continue

    #print(ngram_list)
    #将剩下来的不为‘’的ngram添加到final_thesaurus中
    for i in range(len(ngram_list)):
        if(ngram_list[i][0] != ''):
            final_thesaurus.append(ngram_list[i])

    return final_thesaurus


# 返回最后的分割结果（结合pre_seg和ngram）[0, 2, 4, 7, 8, 11, 12, 13, 15, 20, 24, 27, 29, 32, 36]
def final_seg(content, final_thesaurus, segment):
    final_seg_pos = []
    for i in range(len(final_thesaurus)):
        for j in range(len(content) - final_thesaurus[i][1]):
            if (content[j:j + final_thesaurus[i][1]] == final_thesaurus[i][0]):
                if (j not in final_seg_pos):
                    final_seg_pos.append(j)
                if ((j + final_thesaurus[i][1]) not in final_seg_pos):
                    final_seg_pos.append(j + final_thesaurus[i][1])

    if (0 not in final_seg_pos):
        final_seg_pos.append(0)

    for i in range(len(segment)):
        if (segment[i][0] not in final_seg_pos):
            final_seg_pos.append(segment[i][0])
        if (segment[i][1] not in final_seg_pos):
            final_seg_pos.append(segment[i][1])

    final_seg_pos.sort()

    return final_seg_pos


def read(input_file):
    f_text = codecs.open(input_file, 'r', encoding='utf-8')  # 必须事先知道文件的编码格式，这里文件编码是使用的utf-8
    content = f_text.read()  # 如果open时使用的encoding和文件本身的encoding不一致的话，那么这里将将会产生错误
    content = content.replace("\r", "")
    f_text.close()
    return content


def write(final_content, output_file):
    f_result = codecs.open(output_file, 'w', encoding='utf-8')  # 必须事先知道文件的编码格式，这里文件编码是使用的utf-8
    f_result.write(final_content)
    f_result.close()


def SelfSeg(input_file, output_file):
    content = read(input_file)
    final_content = ''
    segment = pre_seg(content)

    s = pre_seg_str(segment, content)

    ngram_list = calculate_ngram(s)
    #print(ngram_list)
    final_thesaurus = eliminate_ngram(ngram_list)
    #print(final_thesaurus)
    final_seg_pos = final_seg(content, final_thesaurus, segment)

    for i in range(len(content)):
        final_content = final_content + content[i]
        if i + 1 in final_seg_pos:
            final_content = final_content + '/'

    write(final_content, output_file)


if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print("Please use: python SelfSeg.py input output")
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    

    SelfSeg(input_file, output_file)
