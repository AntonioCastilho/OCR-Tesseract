import cv2
import tkinter.filedialog
import PySimpleGUI as sg
import ctypes
import imutils
import pytesseract
import PySimpleGUI as sg

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def select_ROI(img):
    resp = True
    while resp == True:
        # Read image
        im = img
        showCrosshair = False
        fromCenter = False
        # Select ROI
        myroi = cv2.selectROI("Selecione a área de teste",
                              im, fromCenter, showCrosshair)
        x, y, w, h = myroi
        # Crop image
        imCrop = im[int(myroi[1]):int(myroi[1] + myroi[3]),
                    int(myroi[0]):int(myroi[0] + myroi[2])]

        # Display cropped image
        imCropaumentada = imutils.resize(imCrop, width=300)
        cv2.imshow("ROI", imCropaumentada)
        resp = decide("Escolher", "Extrair caracteres dessa área?")
        if resp:
            texto = extrai_string(imCrop)
            Mbox('Texto extraido', texto, 0)
            cv2.destroyAllWindows()
            resp = False
        else:
            resp = True
            cv2.destroyAllWindows()

    return imCrop


# -==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


# -==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-
def extrai_string(img_crop):
    texto = pytesseract.image_to_string(img_crop)
    return texto


# -==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-
def decide(chart, question):
    box_name = chart
    inquire = question
    layout = [[sg.Text(inquire)],
              [sg.Button("Não"), sg.Button("Sim")],
              ]
    window = sg.Window(box_name, layout)
    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Não" or event == sg.WIN_CLOSED:
            ret = False
            break
        elif event == "Sim":
            ret = True
            break
    window.close()
    return ret


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def OCR_img():
    img = cv2.imread(tkinter.filedialog.askopenfilename())
    w, h, c = img.shape
    if w < 800:
        nw = w
    else:
        nw = 800
    nh = nw * w / h
    img = cv2.resize(img, dsize=(round(nw), round(nh)),
                     interpolation=cv2.INTER_CUBIC)
    resp = select_ROI(img)


box_name = "OCR Imagem"
inquire = 'escolher'

layout = [[sg.Text(inquire)],
          [sg.Button("Selecionar Imagem"), sg.Button("Sair")],
          ]

window = sg.Window(box_name, layout)
window.get_screen_dimensions()

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Sair" or event == sg.WIN_CLOSED:
        break
    elif event == "Selecionar Imagem":
        ret = OCR_img()


window.close()
