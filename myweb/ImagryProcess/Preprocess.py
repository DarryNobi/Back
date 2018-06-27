import os,shutil
import numpy as np
import re
import gdal
from myweb.models import Bmap
import tarfile
from myweb.ImagryProcess import coords_to_geojson
from PIL import Image
def preprogress(id):
    labelpath=""
    cwd=os.getcwd()
    source = Bmap.objects.get(id=id).sourcefile
    gdal.AllRegister()
    driver = gdal.GetDriverByName("GTiff")
    downloadpath=os.path.join(os.path.dirname(source),str(id)+'.tar.gz')
    downloadfile = tarfile.open(downloadpath, "w:gz")
    sourcefiles=os.listdir(source)
    while(len(sourcefiles)==1):
        source=os.path.join(source,sourcefiles[0])
        sourcefiles=os.listdir(source)
    for file in sourcefiles:
        if('_fusion.tif' in file):
            name = file
            folder=source
            image = os.path.join(folder,name)
        elif re.search(r'PAN\d.jpg',file):
            thumbnail_path=os.path.join(source,file)
            os.chdir(source)
            downloadfile.add(file,recursive=False)
            os.chdir(cwd)
        elif re.search(r'PAN\d.xml',file):
            os.chdir(source)
            downloadfile.add(file,recursive=False)
            os.chdir(cwd)
        elif('Label' in file):
            labelpath=os.path.join(source,file)

    try:
            imageDS = gdal.Open(image.encode('utf-8'), gdal.GA_ReadOnly)
            im_width = imageDS.RasterXSize
            im_height = imageDS.RasterYSize
            imageUnit8 = image.replace('.tif','U.tif')
            dstDS = driver.Create(imageUnit8,
                                  xsize=im_width, ysize=im_height, bands=3, eType=gdal.GDT_Byte)

            for iband in range(1, 4):
                imgMatrix = imageDS.GetRasterBand(iband).ReadAsArray(0, 0, im_width, im_height)
                zeros = np.size(imgMatrix) - np.count_nonzero(imgMatrix)
                minVal = np.percentile(imgMatrix, float(zeros / np.size(imgMatrix) * 100 + 0.15))
                maxVal = np.percentile(imgMatrix, 99.988)

                idx1 = imgMatrix < minVal
                idx2 = imgMatrix > maxVal
                idx3 = ~idx1 & ~idx2
                imgMatrix[idx1] = imgMatrix[idx1] * 20 / minVal
                imgMatrix[idx3] = pow((imgMatrix[idx3] - minVal) / (maxVal - minVal), 0.7) * 255
                imgMatrix[idx2] = 255

                dstDS.GetRasterBand(iband).WriteArray(imgMatrix)
                dstDS.FlushCache()
                imgMatrix = None
            imageDS = None
            dstDS = None

            shutil.copyfile(image.replace('.tif','_rpc.txt'),
                            imageUnit8.replace('.tif', '_rpc.txt'))

            rpcFile=open(image.replace('_fusion.tif','.rpb'),'r')
            text=rpcFile.readlines()
            for line in text:
                hoffLine=re.search(r'heightOffset = ([\+|\-|\d]\d+\.?\d+)',line)
                if hoffLine:
                    hoff=hoffLine.group(1)
                    break
            rpcFile.close()
            RpcHeight="['RPC_HEIGHT="+str(hoff)+"]'"

            warpOP = gdal.WarpOptions(dstSRS='WGS84', rpc=True, multithread=True, errorThreshold=0.0,creationOptions=['Tiled=yes'],
                                      resampleAlg=gdal.gdalconst.GRIORA_Cubic,transformerOptions=RpcHeight,dstAlpha=True)
            imageDS = gdal.Open(imageUnit8.encode('utf-8'),gdal.GA_ReadOnly)
            imageRPC = os.path.join(folder, name[:name.find('.tif')] + 'R.tif')

            srcDS = gdal.Warp(imageRPC.encode('utf-8').decode(), imageDS, options=warpOP)
            imageDS=None
            srcDS=None

            os.remove(imageUnit8)
            os.remove(imageUnit8.replace('.tif', '_rpc.txt'))

            DS = gdal.Open(imageRPC.encode('utf-8').decode(), gdal.GA_Update)
            iWidth = DS.RasterXSize
            iHeigh = DS.RasterYSize
            iPixelNum = iWidth * iHeigh
            iTopNum = 4096
            iCurNum = iPixelNum / 4
            anLevels = []
            nLevelCount = 0
            while (iCurNum > iTopNum):
                anLevels.append(pow(2, nLevelCount + 2))
                nLevelCount += 1
                iCurNum /= 4
            DS.BuildOverviews(overviewlist=anLevels)
            DS = None
            if labelpath:
                shutil.copyfile(image.replace('.tif','_rpc.txt'),'Label_rpc.txt')
                warpOP = gdal.WarpOptions(dstSRS='WGS84', rpc=True, multithread=True, errorThreshold=0.0,
                                          creationOptions=['Tiled=yes'],
                                          resampleAlg=gdal.gdalconst.GRIORA_Bilinear, transformerOptions=RpcHeight,
                                          dstNodata=255)
                LabelDS = gdal.Open(labelpath.encode('utf-8'), gdal.GA_ReadOnly)
                LabelRPC = os.path.join(source, 'LabelR.tif')
                srcDS = gdal.Warp(LabelRPC.encode('utf-8').decode(), LabelDS, options=warpOP)
                LabelDS=None
                srcDS=None
                im = Image.open(LabelRPC)
                im.save(os.path.join(source, 'Label.png'))
                coords_to_geojson.geojson_make(os.path.join(source, 'Label.png'),source)
                os.chdir(os.path.dirname(LabelRPC))
                for file in os.listdir(os.path.dirname(LabelRPC)):
                    if "json" in file:
                        downloadfile.add(file)
                os.chdir(cwd)
            os.chdir(os.path.dirname(imageRPC))
            downloadfile.add(os.path.basename(imageRPC))
            downloadfile.close()
            os.chdir(cwd)
            Bmap.objects.filter(id=id).update(IsUnit8=1,thumbnail_path=thumbnail_path,downloadfile=downloadpath)
            return "上传成功！"
    except Exception as err:
        Bmap.objects.filter(id=id).delete()
        return str(err)