import maketxt
import split_datasets
import voc2coco
maketxt.maketxt(0.8,0.8) # (train, val): test=0.8:0.2  train:val=0.8:0.2
split_datasets.split()
voc2coco.voco2coco()