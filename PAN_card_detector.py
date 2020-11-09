import re
import pytesseract
import cv2
import numpy
import string

try:
    from PIL import Image
except ImportError:
    import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class PAN_OCR:

    def __init__(self):
        pass

    def ocr_text(self,filename):
        gray = cv2.cvtColor(filename, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (32, 32))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        im2 = filename.copy()
        text = ""
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped = im2[y:y + h, x:x + w]
            text = pytesseract.image_to_string(cropped)
        return text

    def ocr_core(self,filename):
        try:
            text = pytesseract.image_to_string(filename)
            Birthdate_Result = self.Birthdate_isValid(text)
            PanNo_Result = self.PanNo_isvalid(text)
            Full_Name, Father_name = self.extract_Name(text)
            if Full_Name == "" and Father_name == "":
                Full_Name, Father_name = self.extract_Name2(text)
            List_result = [Full_Name, Father_name, str(Birthdate_Result), str(PanNo_Result)]

        except:
            file = filename
            opencvImage = cv2.cvtColor(numpy.array(file), cv2.COLOR_RGB2BGR)
            cv2text = self.ocr_text(opencvImage)
            result = "".join([s for s in cv2text.strip().splitlines(True) if s.strip()])
            Birthdate_Result = self.Birthdate_isValid(result)
            PanNo_Result = self.PanNo_isvalid(result)
            Full_Name, Father_name = self.extract_Name2(result)
            if Full_Name == "" and Father_name == "":
                Full_Name, Father_name = self.extract_Name(result)
            List_result = [Full_Name, Father_name, str(Birthdate_Result), str(PanNo_Result)]

        return List_result

    def Birthdate_isValid(self, readdata):
        try:
            Result = re.compile("([0-9]{2}\/[0-9]{2}\/[0-9]{4})")
            Result1 = Result.findall(readdata)
            return str(Result1[0])
        except:
            return None

    def PanNo_isvalid(self, readdata):
        try:
            Result = re.compile("[A-Z]{3}[P]{1}[A-Z]{1}[0-9]{4}[A-Z]{1}")
            # Result = re.compile("[A-Za-z]{5}\d{4}[A-Za-z]{1}")
            PanNo = Result.findall(readdata)
            return str(PanNo[0])
        except:
            return None

    def extract_Name(self, readdata):
        try:
            PanNo_Result = self.PanNo_isvalid(readdata)
            try:
                res = readdata.split("INDIA")[1].split(PanNo_Result)[0].strip()
            except:
                res = readdata.split("TAX")[1].split(PanNo_Result)[0].strip()
            seperate_res_line = [line for line in res.split('\n') if line.strip() != '']
            final_result = []
            full_name = ""
            father_name = ""
            for single_line in seperate_res_line:
                single_line = str(single_line)
                result = ""
                if len(single_line) > 1 :
                    str_result = re.findall('([A-Z][A-Z]+)', single_line)
                    for word_res in str_result:
                        result = result + word_res + " "
                    if len(result) > 1:
                        final_result.append(str(result))

            for f_res in final_result:
                f_text = f_res.split()
                if len(f_text) == 1:
                    final_result.remove(f_res)

            if len(final_result) == 2:
                full_name = final_result[0]
                father_name = final_result[1]
            return full_name, father_name
        except:
            return None,None

    def extract_Name2(self, readdata):
        try:
            Birth_date = self.Birthdate_isValid(readdata)
            PanNo_Result = self.PanNo_isvalid(readdata)
            filter_string = readdata.split(str(Birth_date))[0].split(PanNo_Result)[1]
            filter_string = filter_string.translate(str.maketrans('', '', string.punctuation)).strip()
            str_split_line = [line for line in filter_string.split( result = ""
'\n') if line.strip() != '']
            final_result = []
            full_name = ""
            father_name = ""
            for split_line in str_split_line:
                split_line = str(split_line)
                if len(split_line) > 1:
                    result_string = re.findall('([A-Z][A-Z]+)', split_line)
                    for res_string in result_string:
                        result = result + res_string + " "
                    if len(result) > 1:
                        final_result.append(str(result))

            for f_res in final_result:
                f_text = f_res.split()
                if len(f_text) == 1:
                    final_result.remove(f_res)

            if len(final_result) == 2:
                full_name = final_result[0].rstrip()
                father_name = final_result[1].rstrip()
            return full_name,father_name
        except:
            return None, None

# obj = OCR()
# text = '''
#  sree feat
# INCOME TAX DEPARTMENT
# GAIKWAD GANESH DHARMA
#
#
#
# DHARMA SHRIPATI GAIKWAD
#
# 14/07/1988
# Permanent Account Nu
#
# AYMPG6130B
# '''
# birth = obj.Birthdate_isValid(text)
# pan = obj.PanNo_isvalid(text)
# name, father = obj.extract_Name(text)
# print(birth,pan,name,father)