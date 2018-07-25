#!/usr/bin/python
# -*-coding:utf-8-*-
import numpy as np
import matplotlib.pyplot as plt
import skimage.draw as draw
from skimage import io, exposure, morphology, measure
from skimage import filters
from skimage.measure import find_contours, approximate_polygon
from shapely.geometry import Polygon

class fit:
    def __init__(self, image):
        r_pad = 12
        self.pad = r_pad
        [h, w] = image.shape
        self.image = np.zeros([h + 2 * r_pad, w + 2 * r_pad])
        self.image[r_pad:r_pad + h, r_pad:r_pad + w] = np.copy(image)
        self.polys = []

    def poly_fit(self, low_threshold=50, high_threshold=120):
        [h, w] = self.image.shape
        r_pad = self.pad
        labels = measure.label(self.image)#, connectivity=1)
        for region in measure.regionprops(labels):
            minr, minc, maxr, maxc = region.bbox
            _r = max(minr - r_pad, 0)
            _c = max(minc - r_pad, 0)
            __r = min(maxr + r_pad, h + 2 * r_pad)
            __c = min(maxc + r_pad, w + 2 * r_pad)
            zone = np.array(labels[_r:__r, _c:__c] == region.label)

            if zone.shape[0] < 3 or zone.shape[1] < 3: continue

            contour = find_contours(zone, 0)
            if len(contour) < 1: continue

            coords = approximate_polygon(contour[0], tolerance=0.1)

            if len(coords) < 3: continue

            poly = Polygon(zip(coords[:, 0] + _r - self.pad, coords[:, 1] + _c - self.pad))

            if poly.area < 10: continue

            self.polys.append(poly)

    def draw_poly(self):
        canvas = np.zeros(self.image.shape, dtype=np.uint8)
        for poly in self.polys:
            coordx, coordy = zip(*list(poly.exterior.coords))
            plt.plot([i+1 for i in coordy], coordx)
            plt.show()
            #rr, cc = draw.polygon(coordx, coordy)  # polygon_perimeter
            #draw.set_color(canvas, [rr, cc], 255, alpha=0.4)
        return canvas
    def draw_poly_on(self):

        canvas = np.zeros(self.image.shape, dtype=np.uint8)
        r_pad = self.pad
        [width, height] = self.image.shape
        image = self.image[r_pad:-r_pad, r_pad:-r_pad]
        plt.imshow(image)
        for poly in self.polys:
            coordx, coordy = zip(*list(poly.exterior.coords))
            plt.plot([i+1 for i in coordy], coordx)
        plt.show()
        return canvas

def main():
    path = 'I:/label/GF2_PMS2_E117.4_N39.1_20170510_L1A0002351826-MSS2_fusion_67_50.png'
    img = io.imread(path)
    r = np.unique(img).tolist()
    if 0 in r:
        r.remove(r.index(0))
    for i in r:
        pfit = fit(img == i)
        pfit.poly_fit()
        pfit.draw_poly_on()

if __name__ == '__main__':
    main()
