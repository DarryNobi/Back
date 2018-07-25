
from myweb.ImagryProcess import WCS_transform
class transform:
    def __init__(self, GeoTransform):
        self.adfGeoTransform = GeoTransform
    def transforms(self,x,y):

        px = self.adfGeoTransform[0] + x * self.adfGeoTransform[1] + y * self.adfGeoTransform[2]
        py = self.adfGeoTransform[3] + x * self.adfGeoTransform[4] + y * self.adfGeoTransform[5]
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