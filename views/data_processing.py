from PIL import Image
import pydicom
from pydicom import dcmread
import SimpleITK as sitk
import numpy as np
from io import BytesIO
import base64
import json


def dicom_load(path, imgmode=1):
    dicomdata = dcmread(path)
    PatientID, PatientName, Rows, Columns = get_tag(path)

    WW, WL = get_WW_WL(path)
    if imgmode:
        img_byte = dicom_img(path)
    else:
        img_byte = None

    data = {
        "PID":str(PatientID),
        "PName":str(PatientName),
        "Rows":str(Rows),
        "Columns":str(Columns),
        "WW":str(WW),
        "WL":str(WL),
        "image":img_byte
    }
    # data = json.dumps(data)

    return data


def dicom_renew(path, data):
    dicomdata = dcmread(path)
    PI = dicomdata.PhotometricInterpretation
    WW = int(data["ww"])
    WL = int(data["wl"])
    inverse = data["inverse"]
    print(WW,WL,inverse)

    imgarray = get_imgarray(path)
    newimgarray = norm(imgarray, WL, WW)
    newimgarray = np.uint8(newimgarray * 255)
    if inverse == "1":
        newimgarray = img_inverse(newimgarray)

    if PI == "RGB":
        img_byte = img_to_byte(newimgarray[0],"RGB")
    else:
        img_byte = img_to_byte(newimgarray[0],"L")

    newdata = {
        "ok":True,
        "WW":str(WW),
        "WL":str(WL),
        "inverse":inverse,
        "image":img_byte
    }
    # data = json.dumps(data)

    return newdata


def get_tag(path):
    dicomdata = dcmread(path)
    try :
        PatientID = dicomdata.PatientID
        # patientID = dicomdata[0x0010, 0x0020].value
    except :
        PatientID = ""
    try :
        PatientName = dicomdata.PatientName
        # PatientName = dicomdata[0x0010, 0x0010].value
    except :
        PatientName = ""
    try :
        Rows = dicomdata.Rows
        Columns = dicomdata.Columns
        # Rows = dicomdata[0x0028, 0x0010].value
        # Columns = dicomdata[0x0028, 0x0011].value
    except :
        array = get_imgarray(path)
        Rows = len(array.shape[1])
        Columns = len(array.shape[2])

    return PatientID, PatientName, Rows, Columns


def get_WW_WL(path):
    dicomdata = dcmread(path)
    try:
        if type(dicomdata.WindowWidth) == pydicom.valuerep.DSfloat or type(dicomdata.WindowCenter) == pydicom.valuerep.DSfloat:
            WW = float(dicomdata.WindowWidth)
            WL = float(dicomdata.WindowCenter)
        elif type(dicomdata.WindowWidth) == pydicom.multival.MultiValue or type(dicomdata.WindowCenter) == pydicom.multival.MultiValue:
            WW = float(dicomdata.WindowWidth[0])
            WL = float(dicomdata.WindowCenter[0])
    except :
        imgarray = get_imgarray(path)
        WW, WL = WWWL_from_array(imgarray)

    WW = int(round(WW))
    WL = int(round(WL))
    # print(WW, WL)

    return WW, WL


def get_imgarray(path):
    # load from sitk
    sitk_image = sitk.ReadImage(path)
    rescale_image = sitk.GetArrayFromImage(sitk_image)
    # print(rescale_image.shape)
    # (張數, 高h, 寬w)
    # RGB
    # (張數, 高h, 寬w, 3)

    # load from pydicom
    # rescale_image = rescale_pixelarray(path)

    return rescale_image


def rescale_pixelarray(path):
    # load from pydicom
    dicomdata = dcmread(path)
    image = dicomdata.pixel_array
    try :
        RescaleSlope = float(dicomdata.RescaleSlope)
    except :
        RescaleSlope = 1.0
    try :
        RescaleIntercept = float(dicomdata.RescaleIntercept)
    except :
        RescaleIntercept = 0

    rescale_image = image * RescaleSlope + RescaleIntercept

    return rescale_image


def WWWL_from_array(array):
    WW = float(array.max()-array.min())
    WL = float((array.max()+array.min())/2)

    # print(array.max(),array.min())
    # print(WW,WL)
    return WW, WL


def norm(data, WL, WW):
    newdata = data
    newdata = newdata - WL + (WW/2)
    newdata = newdata / WW
    newdata[newdata < 0] = 0
    newdata[newdata > 1] = 1

    return newdata


def dicom_img(path):
    dicomdata = dcmread(path)
    PI = dicomdata.PhotometricInterpretation
    Modality = dicomdata.Modality
    imgarray = get_imgarray(path)
    if Modality == "CR" or Modality == "DX":
        newimgarray = imgarray[0].astype("uint8")
        img_byte = img_to_byte(newimgarray,"L")
    else:
        if PI == "RGB":
            newimgarray = imgarray[0].astype("uint8")
            # newimgarray = img_inverse(newimgarray)
            img_byte = img_to_byte(newimgarray,"RGB")
        else:
            WW, WL = get_WW_WL(path)
            newimgarray = norm(imgarray, WL, WW)
            newimgarray = np.uint8(newimgarray * 255)
            # newimgarray = img_inverse(newimgarray)
            img_byte = img_to_byte(newimgarray[0],"L")
    
    return img_byte


def img_inverse(array):
    # 黑白翻轉
    # img = 255 - array
    img = 255 - np.array(array)

    return img


def img_to_byte(array, mode):
    img = Image.fromarray(np.uint8(array), mode)
    # img.show()
    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    img_byte = u'data:img/jpeg;base64,' + data64.decode('utf-8')

    return img_byte


def dicom_img_save(path, img_path):
    dicomdata = dcmread(path)
    PI = dicomdata.PhotometricInterpretation
    Modality = dicomdata.Modality
    imgarray = get_imgarray(path)
    if Modality == "CR" or Modality == "DX":
        newimgarray = imgarray[0].astype("uint8")
        mode = "L"
    else:
        if PI == "RGB":
            newimgarray = imgarray[0].astype("uint8")
            mode = "RGB"
        else:
            WW, WL = get_WW_WL(path)
            newimgarray = norm(imgarray, WL, WW)
            newimgarray = np.uint8(newimgarray * 255)
            newimgarray = newimgarray[0]
            mode = "L"
    img = Image.fromarray(np.uint8(newimgarray), mode)
    img.save(img_path)


