import shutil

from tqdm import tqdm
import sys, os, json, glob
import xml.etree.ElementTree as ET

import config

#  数据集的类型
category_list = config.CATEGORY_LIST


def convert_to_cocodetection(dir, datasets_name, output_dir):
    """
    input:
        dir:the path to DIOR dataset
        output_dir:the path write the coco form json file
    """
    annotations_path = config.ANNOTATION_ROOT
    ImageSets_path = config.TARGETROOT
    # train_images_path = os.path.join(dir, "train")
    # val_images_path = os.path.join(dir, "val")
    id_num = 0

    # 将数据集的类别信息 存放到字典中
    label_ids = {name: i + 1 for i, name in enumerate(category_list)}
    categories = []
    for k, v in label_ids.items():
        categories.append({"name": k, "id": v})

    # 读取xml文件并转化为json
    for mode in ["train","val","test","trainval"]:
        images = []
        annotations = []

        with open(os.path.join(ImageSets_path,'%s'%mode+'.txt'),'r') as f:
            file=f.read().strip().split()
            # 依次读取训练集或测试集中的每一张图片的名字
            with tqdm(total=len(file),desc="%s"%mode+".json loading") as pbar:
                for name in file:
                    # name = name.strip()
                    image_name = name + ".jpg"
                    annotation_name = name + ".xml"
                    # xml标注文件信息解析
                    tree = ET.parse(annotations_path + "\\" + annotation_name)
                    root = tree.getroot()

                    # images信息处理
                    image = {}
                    image["file_name"] = image_name
                    image["id"] = name
                    size = root.find('size')
                    # 如果xml内的标记为空，增加判断条件
                    if size != None:
                        # 获得宽
                        image["width"] = int(size.find('width').text)
                        # 获得高
                        image["height"] = int(size.find('height').text)
                    images.append(image)

                    # annotation 注释信息
                    for obj in root.iter('object'):

                        annotation = {}
                        # 获得类别 =string 类型
                        category = obj.find('name').text
                        # 如果类别不是对应在我们预定好的class文件中则跳过
                        if category not in category_list:
                            continue
                        # 找到bndbox 对象
                        xmlbox = obj.find('bndbox')
                        # 获取对应的bndbox的数组 = ['xmin','xmax','ymin','ymax']
                        bbox = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text),
                                float(xmlbox.find('xmax').text), float(xmlbox.find('ymax').text))
                        # 整数化
                        bbox = [int(i) for i in bbox]
                        # 将voc的xyxy坐标格式，转换为coco的xywh格式
                        bbox = xyxy_to_xywh(bbox)
                        # 将xml中的信息存入annotations
                        annotation["image_id"] = name
                        annotation["bbox"] = bbox
                        annotation["category_id"] = category_list.index(category)
                        annotation["id"] = id_num
                        annotation["iscrowd"] = 0
                        annotation["segmentation"] = []
                        annotation["area"] = bbox[2] * bbox[3]
                        id_num += 1
                        annotations.append(annotation)
                    pbar.update(1)

            # 汇总所有信息，保存在字典中
            dataset_dict = {}
            dataset_dict["images"] = images
            dataset_dict["annotations"] = annotations
            dataset_dict["categories"] = categories
            json_str = json.dumps(dataset_dict)
            save_file = f'{output_dir}/{datasets_name}_{mode}.json'
            with open(save_file, 'w') as json_file:
                json_file.write(json_str)

    print("json file write done...")


def xyxy_to_xywh(boxes):
    width = boxes[2] - boxes[0]
    height = boxes[3] - boxes[1]
    return [boxes[0], boxes[1], width, height]


def voco2coco():
    # 数据集的路径
    DATASET_ROOT = config.ROOT
    # 数据集名称
    DATASET_NAME = config.DATASET_NAME
    # 输出coco格式的存放路径
    JSON_ROOT = os.path.join(config.ROOT,'annotation')
    # 递归删除之前存放json的文件夹，并新建一个
    try:
        shutil.rmtree(JSON_ROOT)
    except OSError:
        pass
    os.mkdir(JSON_ROOT)
    convert_to_cocodetection(dir=DATASET_ROOT, datasets_name=DATASET_NAME, output_dir=JSON_ROOT)