from django.shortcuts import render
from pytesseract import pytesseract
import re
from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCR:
    def __init__(self):
        self.path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def extract(self, filename):
        pytesseract.tesseract_cmd = self.path
        img = Image.open(filename)
        text = pytesseract.image_to_string(img)
        return text

def payment(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']
        ocr = OCR()
        text = ocr.extract(img)
        x = re.split("\n", text)
        for i in x:
            if re.findall("^[0-9]{20}$", i):
                tran_id = i
            if re.findall("Tran.{4}$", i):
                tran_type = i
            if re.findall("^Ma|^Mg|^U|^Daw", i):
                name = i
            if re.findall("^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)", i):
                tme = i
            if re.findall("Ks$", i):
                amount = i
        return render(request, 'show.html', {'tran_id':tran_id, 'tran_type':tran_type, 'name':name, 'tme':tme, 'amount':amount})
    return render(request,'payment.html')