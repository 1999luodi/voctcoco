import os
import random
import shutil
import config
from config import ROOT

'''
对图片数据集进行随机分类
train:val:test 比例可以自己调控
生成3个txt文件存划分文件名

'''
# (train, val): test=0.9:0.1  train:val=0.8:0.2


def maketxt(trainval_percentc, train_trainval_percentc):
    xmlfilepath = config.ANNOTATION_ROOT  # 获取你源数据的注释路径
    txtsavepath = config.TARGETROOT  # 设置你txt的保存路径
    # 递归删除之前存放txt的文件夹，并新建一个
    try:
        shutil.rmtree(txtsavepath)
    except OSError:
        pass
    os.makedirs(txtsavepath,exist_ok=True)
    total_xml = os.listdir(xmlfilepath)  # 获取xml文件列表

    num = len(total_xml)  # 获取xml文件的数量
    list_indices = list(range(num)) # 获取xml文件的序列号
    random.shuffle(list_indices)  # 使用shuffle函数打乱列表的次序

    train_trainval_percent = train_trainval_percentc
    trainval_percent = trainval_percentc
    tv = int(num * trainval_percent)  # 划分训练集和验证机的数量
    tr = int(tv * train_trainval_percent)  # 划分训练集的数量

    trainval = random.sample(list_indices, tv)
    train = random.sample(trainval, tr)

    with open(os.path.join(txtsavepath, 'trainval.txt'), 'w') as ftrainval, \
            open(os.path.join(txtsavepath, 'test.txt'), 'w') as ftest, \
            open(os.path.join(txtsavepath, 'train.txt'), 'w') as ftrain, \
            open(os.path.join(txtsavepath, 'val.txt'), 'w') as fval:
        for i in list_indices:
            # 获取文件名称中.xml之前的部分
            name = os.path.splitext(total_xml[i])[0] + '\n'

            if i in trainval:
                ftrainval.write(name)
                if i in train:
                    ftrain.write(name)
                else:
                    fval.write(name)
            else:
                ftest.write(name)
