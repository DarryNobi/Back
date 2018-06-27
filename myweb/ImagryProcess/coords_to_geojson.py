import json
from skimage import io
import os
import datetime
from itertools import chain
import gdal
import numpy as np
from myweb.ImagryProcess.poly_fit import fit
from myweb.ImagryProcess.coords_to_latitude import transform

def geojson_make(img_path,save_path):
    dataset = gdal.Open(img_path)
    if dataset == None:
        return
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_bands = dataset.RasterCount  # 波段数
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
    del dataset
    types=[2,3,4,5,6,7]#np.unique(im_data)
    label_area={}
    for label_type in types:
        geojsons=[]
        img = (im_data == label_type).astype('int8')
        pfit = fit(img)
        pfit.poly_fit()
        label_area[label_type]=0
        for poly in pfit.polys:
            segmentation=list(chain.from_iterable(zip(poly.boundary.xy[1], poly.boundary.xy[0])))
            geojson=dict()
            geometry=dict()
            geometry['coordinates']=[[transform(segmentation[i],segmentation[i+1]) for i in range(0,len(segmentation),2)]]
            geometry['type']="Polygon"
            geojson['geometry']=geometry
            geojson['properties']={'type':str(label_type)}
            geojson['type']='Feature'
            geojsons.append(geojson)
            label_area[label_type]=label_area[label_type]+poly.area
        with open(os.path.join(save_path,'geojsons_t'+str(label_type)+'.json'), 'w') as json_file:
            json.dump(geojsons, json_file, ensure_ascii=False)
    with open(os.path.join(save_path,'label_area.json'), 'w') as json_file:
        json.dump(label_area, json_file, ensure_ascii=False)
    return 0
# def main():
#     img_path='./fusion84NoL.png'
#     geojson_make(img_path)
#     return 0
#
# if __name__ == '__main__':
#     main()
