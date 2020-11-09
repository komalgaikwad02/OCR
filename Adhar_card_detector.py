import re
import pytesseract
import cv2

try:
    from PIL import Image
except ImportError:
    import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class Adhar_OCR:

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
        text = pytesseract.image_to_string(filename)
        # print("***********\n",text)
        Birthdate_Result = self.Birthdate_isValid(text)
        AdharNO_Result = self.Adhar_no_isvalid(text)
        Full_Name = self.extract_Name(text)
        Gender = self.extract_Gender(text)

        List_result = [Full_Name,str(Gender),str(Birthdate_Result), str(AdharNO_Result)]
        return List_result

    def Birthdate_isValid(self, readdata):
        try:
            try:
                Result = re.compile("([0-9]{2}\/[0-9]{2}\/[0-9]{4})")
                Birth = Result.findall(readdata)
                return Birth[0]
            except:
                Result = re.compile("([1-9]{4})")
                gender = self.extract_Gender(readdata)
                res = readdata.split('Birth :')[1].split(gender)[0]
                Birth = Result.findall(res)
                return Birth[0]
        except:
            return None

    def Adhar_no_isvalid(self, readdata):
        try:
            AdharNo = re.findall("([2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4})", readdata)
            return str(AdharNo[0])
        except:
            return None

    def extract_Name(self, readdata):
        try:
            birth = self.Birthdate_isValid(readdata)
            res = readdata.split(birth)[0]
            try:
                Full_name = re.findall('([A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+)', res)
                return Full_name[0]
            except:
                Full_name = re.findall('([A-Z][a-z]+\s[A-Z][a-z]+)', res)
                return Full_name[0]

        except:
            return None

    def extract_Gender(self, readdata):
        try:
            text = readdata.lower()
            # print("1st string",text)
            substring = "female"
            # print("2nd string", substring)
            if text.find(substring) != -1 :    # not empty string
                gender = "Female"
            elif text.find("male") != -1 :
                gender = "Male"
            # print(gender)
            return gender
        except:
            return None


    # def extract_Gender(self, readdata):
    #     try:
    #         text = readdata.lower()
    #         print (text)
    #         text ="ma1e"
    #         if ('female' or 'fema1e') in text:
    #             gender = "Female"
    #             print ("Yes, String found")
    #             return gender
    #         elif ('male' or 'ma1e' )in text:
    #             gender = "Male"
    #             print ("No, String not found")
    #             return  gender
    #         else:
    #             print("INVALID INPUT")
    #     except:
    #         return None


