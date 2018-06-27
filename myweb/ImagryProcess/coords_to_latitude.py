import gdal
import numpy
from myweb.ImagryProcess import WCS_transform

def transform(x,y):
    gdal.AllRegister()
    filePath='./GF2_PMS2_E117.4_N39.1_20170510_L1A0002351826-MSS2_fusionR.tif'
    ds=gdal.Open(filePath)
    adfGeoTransform = ds.GetGeoTransform()

    px = adfGeoTransform[0] + x * adfGeoTransform[1] + y * adfGeoTransform[2]
    py = adfGeoTransform[3] + x * adfGeoTransform[4] + y * adfGeoTransform[5]
    # print(px,py)
    [ppy,ppx]=WCS_transform.wgs2mercator(py,px)
    return [ppx,ppy]


def main():
    transform(0, 30855)
    return 0


if __name__ == '__main__':
    main()


    #117.58081074582175 39.025083830304325
    #117.25855238897582 39.025083830304325