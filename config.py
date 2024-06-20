import os
# 源数据的根路径设置
ROOT = r"F:\数据集\GermPredDataset\ZeaMays"
#源数据的名称
DATASET_NAME = 'ZeaMays'
#源数据的类别
CATEGORY_LIST = ["zm_im", "zm_el"]

#####################################################################################
#源数据的注释根路径
ANNOTATION_ROOT=os.path.join(ROOT,"true_ann")
#源数据的图像根路径
IMG_ROOT = os.path.join(ROOT,"img")
#划分的txt存储路径 该txt存放划分好训练数据的xml的文件名
TARGETROOT=os.path.join(ROOT,"ImageSets")
