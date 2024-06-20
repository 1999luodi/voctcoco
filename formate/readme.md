# 使用说明
1. 修改config.py 更改源数据的路径信息
2. 更改划分的比例
3. 执行main.py文件


# coco 数据集
coco的annotiaon.json主要部分
```    
包括以下字段：
images部分：
    id：唯一标识图像的ID。
    file_name：图像文件的文件名。
    width：图像宽度（以像素为单位）。
    height：图像高度（以像素为单位）。
    license（可选）：图像的许可证信息。
    
annotations部分：
    id：唯一标识注释的ID。
    image_id：与注释相关联的图像的ID。
    category_id：对象的类别ID，对应于categories部分中的类别。
    segmentation：对象的分割掩码，通常表示为多边形或掩码的像素坐标。
    area：对象的像素面积。
    bbox：对象的边界框，格式为[x, y, width, height]。
    iscrowd：标志位，指示对象是否是“杂乱”（例如，一群对象被视为单个对象）。
    
categories部分：
    id：唯一标识类别的ID。
    name：类别的名称。
    supercategory：类别的超类别，用于组织相关类别。
```