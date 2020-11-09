import os
from PIL import ImageEnhance
from flask import Flask, render_template, request
from PAN_card_detector import PAN_OCR
from Adhar_card_detector import Adhar_OCR
from img_orientation import Image_Orientation
from db_handler import PAN_DataUpdate,Adhar_DataUpdate

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')

        file = request.files['file']
        # print(file)
        card = request.form['card']
        # print(card)

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))

            img_ori = Image_Orientation()
            img1 = img_ori.handle_image_orientation(file)

            if not request.form.getlist('card'):
                return render_template('upload.html',
                                       msg='Selection Error: please select Aadhar card or pan card..!')

            if card == "aadhar":
                enhancer = ImageEnhance.Brightness(img1)
                factor = 0.5
                img1 = enhancer.enhance(factor)

                adhar_obj = Adhar_OCR()
                extracted_text = adhar_obj.ocr_core(img1)
                length = len(extracted_text)
                print(extracted_text, "************")
                Full_Name = extracted_text[0]
                Gender = extracted_text[1]
                Birthdate = extracted_text[2]
                Adharno = extracted_text[3]

                if (Full_Name == None or Gender == None or Birthdate == None or Adharno == None):
                    print("Value is Null not able to insert .... !")
                    return  render_template('upload.html',msg ='Invalid Document..!')
                    # return render_template('upload.html', msg='Image Error: please scan your Aadhar Card properly on Bright Environment & then upload..!')
                else:
                    Adhar_DataUpdate(Full_Name, Gender, Birthdate, Adharno)


            if card == "pan":
                ocr_obj = PAN_OCR()
                extracted_text = ocr_obj.ocr_core(img1)
                length = len(extracted_text)
                print(extracted_text,"************")
                Full_Name = extracted_text[0]
                Father_name = extracted_text[1]
                Birthdate_Result = extracted_text[2]
                PanNo_Result = extracted_text[3]
                # print(PanNo_Result[3])

                if Full_Name == None or Father_name == None or Birthdate_Result == None or PanNo_Result == None:
                    print("Value is Null not able to insert .... !")
                    return  render_template('upload.html',msg='Invalid Document..!')

                    # return render_template('upload.html',msg='Image Error: please scan your PAN Card properly on Bright Environment & then upload..!')

                else:
                    PAN_DataUpdate(Full_Name, Father_name, Birthdate_Result, PanNo_Result)

            # extract the text and display it.
            return render_template('upload.html',
                                   len=length,
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)

    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()
