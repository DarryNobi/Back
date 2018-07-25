import os,shutil
import numpy as np
import re
import gdal
from myweb.models import Bmap
import tarfile
from myweb.ImagryProcess.coords_to_geojson import geojson_make
from myweb.Detector import detection
def preprogress(id):
    def getUploadFile(uploadfolder):
        try:
            uploadfiles = os.listdir(uploadfolder)  # 上传的文件夹
            while(len(uploadfiles)==1):
                uploadfolder=os.path.join(uploadfolder,uploadfiles[0])
                uploadfiles=os.listdir(uploadfolder)
            for file in uploadfiles:
                if('_fusion.tif' in file):#融合图
                    fusionname=file
                elif re.search(r'PAN\d.jpg',file):#缩略图
                    thumbnailname=file
                elif re.search(r'PAN\d.xml',file):#XML
                    XMLname=file
                elif re.search(r'_rpc.txt',file):#RPC
                    rpcfile=file
                elif re.search(r'MSS\d.rpb',file):
                    rpbfile=file
            return uploadfolder,fusionname,rpcfile,rpbfile,thumbnailname,XMLname
        except Exception:
            return "上传失败，请检查上传图包"

    ####转8比特三通道
    def chaneltransform(fusionimage):
        try:
            gdal.AllRegister()
            driver = gdal.GetDriverByName("GTiff")
            fusionimage = gdal.Open(fusionimage.encode('utf-8').decode(), gdal.GA_ReadOnly)
            im_width = fusionimage.RasterXSize
            im_height = fusionimage.RasterYSize
            transformimage = os.path.join(tempfolder,"chaneltransform.tif")
            dstDS = driver.Create(transformimage,
                                  xsize=im_width, ysize=im_height, bands=3, eType=gdal.GDT_Byte)

            for iband in range(1, 4):
                imgMatrix = fusionimage.GetRasterBand(iband).ReadAsArray(0, 0, im_width, im_height)
                zeros = np.size(imgMatrix) - np.count_nonzero(imgMatrix)
                minVal = np.percentile(imgMatrix, float(zeros / np.size(imgMatrix) * 100 + 0.15))
                maxVal = np.percentile(imgMatrix, 99)

                idx1 = imgMatrix < minVal
                idx2 = imgMatrix > maxVal
                idx3 = ~idx1 & ~idx2
                imgMatrix[idx1] = imgMatrix[idx1] * 20 / minVal
                imgMatrix[idx2] = 255
                idx1=None
                idx2=None
                imgMatrix[idx3] = pow((imgMatrix[idx3] - minVal) / (maxVal - minVal), 0.9) * 255

                if iband==1:
                    dstDS.GetRasterBand(3).WriteArray(imgMatrix)
                    dstDS.FlushCache()
                    imgMatrix = None
                elif iband==2:
                    dstDS.GetRasterBand(2).WriteArray(imgMatrix)
                    dstDS.FlushCache()
                    imgMatrix = None
                else:
                    dstDS.GetRasterBand(1).WriteArray(imgMatrix)
                    dstDS.FlushCache()
                    imgMatrix = None
            fusionimage = None
            dstDS = None
            return transformimage
        except Exception :
            return "上传失败，图像转换出错"

    def RPCOrthorectification(orginalimage,rpcfile,rpbfile,Alpha=True):
        try:
            rpcname=os.path.join(os.path.dirname(orginalimage),os.path.basename(orginalimage).replace(".tif","_rpc.txt"))
            shutil.copyfile(rpcfile,rpcname)
            with open(rpbfile,'r') as f:
                for line in f.readlines():
                    hoffLine=re.search(r'heightOffset = ([\+|\-|\d]\d+\.?\d+)',line)
                    if hoffLine:
                        hoff=hoffLine.group(1)
                        break
            f.close()
            RpcHeight="['RPC_HEIGHT="+str(hoff)+"]'"


            if Alpha:
                warpOP = gdal.WarpOptions(dstSRS='WGS84', rpc=True, multithread=True, errorThreshold=0.0,creationOptions=['Tiled=yes'],
                                      resampleAlg=gdal.gdalconst.GRIORA_Bilinear,transformerOptions=RpcHeight,dstAlpha=True)
            else:
                warpOP = gdal.WarpOptions(dstSRS='WGS84', rpc=True, multithread=True, errorThreshold=0.0,creationOptions=['Tiled=yes'],
                                          resampleAlg=gdal.gdalconst.GRIORA_Bilinear,transformerOptions=RpcHeight,dstNodata=0)
            image = gdal.Open(orginalimage.encode('utf-8'),gdal.GA_ReadOnly)
            RPCOrthImage = os.path.join(tempfolder,os.path.basename(orginalimage).replace(".tif","RPC.tif"))
            srcDS = gdal.Warp(RPCOrthImage.encode('utf-8').decode(), image, options=warpOP)
            image=None
            srcDS=None
            return RPCOrthImage
        except Exception:
            return "上传失败，RPC正射校正出错"

    def buildOverviews(image):
        try:
            gdal.AllRegister()
            TransformDS = gdal.Open(image.encode('utf-8').decode(), gdal.GA_ReadOnly)
            Width = TransformDS.RasterXSize
            Heigh = TransformDS.RasterYSize
            PixelNum = Width * Heigh
            TopNum = 4096
            CurNum = PixelNum / 4
            anLevels = []
            nLevelCount = 0
            while (CurNum > TopNum):
                anLevels.append(pow(2, nLevelCount + 2))
                nLevelCount += 1
                CurNum /= 4
            TransformDS.BuildOverviews(overviewlist=anLevels)
            TransformDS = None
        except Exception:
            return "上传失败，建立金字塔出错"

    def makeDownload():
        try:
            cwd = os.getcwd()
            downloadpath=os.path.join(baseurl,str(id)+'.tar.gz')#前端下载路径
            downloadfile = tarfile.open(downloadpath, "w:gz")
            os.chdir(uploadfiles[0])
            downloadfile.add(uploadfiles[4],recursive=False)
            downloadfile.add(uploadfiles[5],recursive=False)
            os.chdir(tempfolder)
            for file in os.listdir(tempfolder):
                if ".json" in file:
                    downloadfile.add(file,recursive=False)
                if file=="chaneltransformRPC.tif":
                    downloadfile.add(file)
            downloadfile.close()
            os.chdir(cwd)
            return downloadpath
        except Exception:
            # if os.path.exists(downloadpath):
            #     os.remove(downloadpath)
            return "上传失败，无法创建压缩包"

    baseurl = '/media/zhou/文档/Back/Maps'
    if not os.path.exists(baseurl):
        os.makedirs(baseurl)
    uploadfolder = Bmap.objects.get(id=id).sourcefile
    uploadfiles=getUploadFile(uploadfolder)
    tempfolder=os.path.join(uploadfiles[0],"temp")
    if not os.path.exists(tempfolder):
        os.makedirs(tempfolder)
    #result=os.path.join(tempfolder,"fusionRPC.tif")
    #result='./myweb/Detector/temp/label/fusion.tif'
    # if not isinstance(result,Exception):
    #     result=RPCOrthorectification(result,os.path.join(uploadfiles[0],uploadfiles[2]),
    #                      os.path.join(uploadfiles[0],uploadfiles[3]),Alpha=False)
    # if not isinstance(result,Exception):
    #     result=geojson_make(result,tempfolder)
    #     if not isinstance(result,Exception):
    #         result=makeDownload()
    #         Bmap.objects.filter(id=id).update(IsUnit8=1, thumbnail_path=os.path.join(uploadfiles[0],uploadfiles[4]),downloadfile=result)
    #         return '上传成功'
    # result=geojson_make(os.path.join(tempfolder,"fusionRPC.tif"),tempfolder)

    result=chaneltransform(os.path.join(uploadfiles[0],uploadfiles[1]))
    if not isinstance(result,Exception):
        result=RPCOrthorectification(result,os.path.join(uploadfiles[0],uploadfiles[2]),
                                     os.path.join(uploadfiles[0],uploadfiles[3]))
        if not isinstance(result,Exception):
            result=buildOverviews(result)
            if not isinstance(result,Exception):
                result=detection.detection(uploadfiles[0]+"/",uploadfiles[1])
                if not isinstance(result,Exception):
                    result=RPCOrthorectification(result,os.path.join(uploadfiles[0],uploadfiles[2]),
                                     os.path.join(uploadfiles[0],uploadfiles[3]),Alpha=False)
                    if not isinstance(result,Exception):
                        result=geojson_make(result,tempfolder)
                        if not isinstance(result,Exception):
                            result=makeDownload()
                            Bmap.objects.filter(id=id).update(IsUnit8=1, thumbnail_path=os.path.join(uploadfiles[0],uploadfiles[4]),downloadfile=result)
                            return '上传成功'

    # if os.path.exists(Bmap.objects.get(id=id).sourcefile):
    #     shutil.rmtree(Bmap.objects.get(id=id).sourcefile)
    # if os.path.exist('./myweb/Detector/temp'):
    #     shutil.rmtree('./myweb/Detector/temp')
    Bmap.objects.filter(id=id).delete()
    return result