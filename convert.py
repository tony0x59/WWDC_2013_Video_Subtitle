#!/usr/bin/evn python
# -*- coding: utf-8 -*-

# 根据https://github.com/qiaoxueshi/WWDC_2013_Video_Subtitle 提供的srt转换命令，
# 生成所有待转换字幕的awk命令列表(只是想偷个懒……)，同时根据puttin提供的标题对照表
#（https://gist.github.com/puttin/6547007#file-title-txt），生成格式化的文件名
# 讲起来好绕口，其实客官您只要拿走converted_files内的文件就可以了...


import os.path


def make_scripts(dstfolder, dic):
    for i in range(100, 715):
        srcpath = '%d.srt' % i
        try:
            dstname = '"%d - %s.srt"' % (i, dic[str(i)])
        except:
            dstname = '%d.srt' % i
        dstpath = '%s/%s' % (dstfolder, dstname)
        if os.path.isfile(srcpath):
            script = r'''awk -v RS="" '{gsub("\n", "-Z"); print}' ''' + srcpath + r''' | awk '$0 !~/^WEB/ {print $0}' | uniq | awk '{printf "\n%s-Z%s", NR,$0 }'  | awk -v ORS="\n\n" '{gsub("-Z", "\n"); print}' >> ''' + dstpath
            print script


def load_titles(filepath):
    dic = {}
    file = open(filepath, 'rb')
    for line in file.readlines():
        try:
            row = line.strip('\n').split(':')
            no, title = row[0], row[1]
            if (no in dic) == False:
                dic[no] = title
            else:
                print 'dic[%s] = %s  -->  %s  pass' % (no, dic[no], title)
        except Exception,e:
            print e
    return dic


if __name__ == '__main__':
    dstfolder='converted_files'
    if os.path.exists(dstfolder) == False:
        os.mkdir(dstfolder)

    dic = load_titles('title.txt')
    make_scripts(dstfolder, dic)

