"""
用于数据集的划分，将全部图片分为train和val，并拷贝到不同文件夹下
"""
import shutil
import os
from config import ROOT, TARGETROOT, IMG_ROOT
from tqdm import tqdm


def split():
    sets = ['train', 'val', 'test','trainval']  # 划分数据集的类型'train','val','test'

    for img_set in sets:
        NEW_ROOT = os.path.join(ROOT, img_set)  # 获取存放的train val test的数据路径

        # 递归删除之前存放json的文件夹，并新建一个
        try:
            shutil.rmtree(NEW_ROOT)
        except OSError:
            pass
        os.makedirs(NEW_ROOT, exist_ok=True)
        with open(os.path.join(TARGETROOT, '%s.txt' % (img_set)), 'r') as file:
            img_ids = file.read().strip().split()
            '''
            read():读取数据
            strip()：移除两端空白数据
            split():分割数据
            '''
            # 使用tqdm来创建一个进度条，这里我们使用len(img_ids)作为总数
            with tqdm(total=len(img_ids), desc='%s ' % img_set + 'Copying images') as pbar:
                for img_id in img_ids:
                    src_root = os.path.join(IMG_ROOT, img_id + '.jpg')  # 源图片路径
                    tar_root = os.path.join(NEW_ROOT, img_id + '.jpg')  # 复制的图片路径
                    shutil.copy(src=src_root, dst=tar_root)
                    # 更新进度条
                    pbar.update(1)


if __name__ == '__main__':
    split()
