from fileinput import filename
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.tix import IMAGE
from PIL import ImageTk, Image
from matplotlib import image
from img_to_text import image_to_text, find_closest_subject, find_grade
import config
import numpy as np
from tkinter.messagebox import askyesno, showerror, showinfo

def load_image_tk(filename, size):
    img = Image.open(filename).resize(size)
    img_tk =  ImageTk.PhotoImage(img)
    return img_tk

IMAGE_SIZE = (400, 600)
FONT = ('Arial', 25)

root = Tk()
root.title("Book Detection")
root.geometry("1200x900")

filename = ''
closest_sub = 'Không xác định'
grade = 'Không xác định'

def btn_choose_action():
    global filename, closest_sub, grade
    filename = askopenfilename()
    if not filename:
        return
    
    new_img_tk = load_image_tk(filename, IMAGE_SIZE)
    lbl_image.config(image=new_img_tk)
    lbl_image.image = new_img_tk
    
    text = image_to_text(filename)
    print(text)
    closest_sub, distance = find_closest_subject(text, config.SUBJECTS)
    grade = find_grade(text, config.GRADES)
    if distance > len(closest_sub) // 2:
        closest_sub = 'Không xác định'
    
    if grade == '0':
        grade = 'Không xác định'
    
    index_subject = subject_list.index(closest_sub)
    cbx_subject.current(index_subject)
    
    index_grade = grade_list.index(grade)
    cbx_grade.current(index_grade)


def btn_reset_action():
    global filename, closest_sub, grade
    
    img_tk =  ImageTk.PhotoImage(Image.fromarray(np.ones(IMAGE_SIZE[::-1]) * 111))
    lbl_image.config(image=img_tk)
    lbl_image.image = img_tk
    
    cbx_subject.current(0)
    cbx_grade.current(0)
    
    filename = ''
    closest_sub = 'Không xác định'
    grade = 'Không xác định'

def btn_save_action():
    global filename, closest_sub, grade
    if filename == '':
        showerror("Erorr", "You have to choose book's picture!")
        return
    
    if closest_sub == 'Không xác định':
        showerror("Erorr", "You have to choose book's name!")
        return
    
    if grade == 'Không xác định':
        showerror("Erorr", "You have to choose book's grade!")
        return
    
    confirm = askyesno(title='confirmation', message='Do you want to save to the database?')
    if confirm:
        with open('db.csv', 'a') as f:
            f.write(f"{filename},{closest_sub},{grade}\n")
    
    showinfo('Success', 'You book has been saved successfully!')
    btn_reset_action()

btn_choose = Button(root, text='Choose Image', command=btn_choose_action, font=FONT)
btn_choose.place(x=175, y=100)

img_tk =  ImageTk.PhotoImage(Image.fromarray(np.ones(IMAGE_SIZE[::-1]) * 111))
# image = PhotoImage('images/tieng_viet_1.jpg')
lbl_image = Label(root, image=img_tk)
lbl_image.place(x=100, y=200)

lbl_subject_name = Label(root, text="Subject", font=FONT)
lbl_subject_name.place(x=675, y=50)

subject_list = ['Không xác định'] + config.SUBJECTS
cbx_subject = ttk.Combobox(root, values=subject_list, state='readonly', font=FONT)
cbx_subject.current(0)
cbx_subject.place(x=675, y=100)

lbl_grade_name = Label(root, text="Grade", font=FONT)
lbl_grade_name.place(x=675, y=350)

grade_list = ['Không xác định'] + config.GRADES
cbx_grade = ttk.Combobox(root, values=grade_list, state='readonly', font=FONT)
cbx_grade.current(0)
cbx_grade.place(x=675, y=400)

btn_save = Button(root, text='Save', command=btn_save_action, font=FONT)
btn_save.place(x=700, y=700)

btn_reset = Button(root, text='Reset', command=btn_reset_action, font=FONT)
btn_reset.place(x=875, y=700)

root.mainloop()