#!/usr/bin/python
# -*-coding:utf-8-*-
import numpy as np
import matplotlib.pyplot as plt
import skimage.draw as draw
from skimage import io, exposure, morphology, measure
from skimage import filters
from skimage.measure import find_contours, approximate_polygon

from skimage.viewer import ImageViewer
from skimage.viewer.widgets import Slider
from skimage.viewer.plugins.overlayplugin import OverlayPlugin

from shapely.geometry import Polygon
import gdal


class fit:
    def __init__(self, image):
        self.image = image#np.copy(image)
        self.polys = []

    def poly_fit(self, low_threshold=50, high_threshold=120):
        shy, shx = self.image.shape
        self.image[0, :] = 0  # black border
        self.image[:, 0] = 0
        self.image[shy-1, :] = 0
        self.image[:, shx-1] = 0

        labels = measure.label(self.image)#, connectivity=1)
        for region in measure.regionprops(labels):
            minr, minc, maxr, maxc = region.bbox
            _r = max(minr - 1, 0)
            _c = max(minc - 1, 0)
            __r = min(maxr + 1, shy - 1)
            __c = min(maxc + 1, shx - 1)
            zone = np.array(labels[_r:__r, _c:__c] == region.label)
            if zone.shape[0] < 4 or zone.shape[1] < 4: continue

            contour = find_contours(zone, 0)
            if len(contour) < 10: continue

            coords = approximate_polygon(contour[0], tolerance=0.1)
            if len(coords) < 15: continue

            poly = Polygon(zip(coords[:, 0] + _r, coords[:, 1] + _c))
            if poly.area < 25: continue
            if poly.is_valid:
                self.polys.append(poly)

    def draw_poly(self, image):
        canvas = np.zeros(self.image.shape, dtype=np.uint8)
        [width,height]=image.shape
        for poly in self.polys:
            coordx, coordy = zip(*list(poly.exterior.coords))
            plt.plot([i+1 for i in coordy],coordx)
            plt.show()
            #rr, cc = draw.polygon(coordx, coordy)  # polygon_perimeter
            #draw.set_color(canvas, [rr, cc], 255, alpha=0.4)
        return canvas


def main():
    dataset = gdal.Open('./fusion.png')
    if dataset == None:
        return
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_bands = dataset.RasterCount  # 波段数
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据

    img=im_data
    print(np.unique(img))
    img=(img==1).astype('int8')
    pfit = fit(img)
    pfit.poly_fit()
    pfit.draw_poly(img)

if __name__ == '__main__':
    main()
