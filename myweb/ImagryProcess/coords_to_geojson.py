import json
import os
from itertools import chain
import gdal
import numpy as np
from myweb.ImagryProcess.poly_fit_new import fit
from myweb.ImagryProcess import WCS_transform

def geojson_make(label_path, save_path):

    app=6.4e-07
    def transforms(x,y):
        # pass
        px = GeoTransform[0] + x * GeoTransform[1] + y * GeoTransform[2]
        py = GeoTransform[3] + x * GeoTransform[4] + y * GeoTransform[5]
        # print(px,py)
        [ppy,ppx]=WCS_transform.wgs2mercator(py,px)
        return [ppx,ppy]
    try:
        dataset = gdal.Open(label_path)
        GeoTransform=dataset.GetGeoTransform()
        if dataset == None:
            return
        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数
        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
        dataset=None
        types = np.unique(im_data)

        # types=np.array([0]).astype('uint8')
        label_area = {}
        for label_type in types:
            geojsons = []
            img = (im_data == label_type).astype('int8')
            pfit = fit(img)
            pfit.poly_fit()
            label_area[int(label_type)] = 0
            for poly in pfit.polys:
                segmentation = list(chain.from_iterable(zip(poly.boundary.xy[1], poly.boundary.xy[0])))
                geojson = dict()
                geometry = dict()
                geometry['coordinates'] = [[transforms(segmentation[i], segmentation[i+1]) for i in range(0, len(segmentation), 2)]]
                geometry['type'] = "Polygon"
                geojson['geometry'] = geometry
                geojson['properties'] = {'type': str(label_type)}
                geojson['type'] = 'Feature'
                geojsons.append(geojson)
                label_area[label_type] = label_area[label_type]+poly.area
            with open(os.path.join(save_path, 'geojsons_t' + str(label_type)+'.json'), 'w') as json_file:
                json.dump(geojsons, json_file, ensure_ascii=False)
        # label_area={0:12,1:56,3:45,4:89}
        with open(os.path.join(save_path, 'label_area.json'), 'w') as json_file:
            label_area_dict=[]
            for key,value in label_area.items():
                label_area_dict.append({key:value*app})
            json.dump(label_area_dict, json_file, ensure_ascii=False)
    except Exception as e:
        return e
def main():
    img_path = './fusion84NoL.png'
    geojson_make('./GF2_PMS2_E117.4_N39.1_20170510_L1A0002351826-MSS2_fusionR.tif', img_path, './')
    return 0

if __name__ == '__main__':
    main()
