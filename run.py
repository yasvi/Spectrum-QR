import customtkinter as ctk 
from tkinter import filedialog
from PIL import Image as img
import numpy as np
import math


def text_QR():
    I_txt=I_textbox.get('1.0','end')
    bdata=I_txt.encode('utf-8') 
    databin=''
    bitlist=[]
    #a string of bytes of the variable 
    for byte in bdata:
        databin+=format(byte,'08b')


    #a list of bits of the variable
    for i in range(0,len(databin),2):
        bitlist.append(databin[i:i+2])

    #mapping bits to numbers - according to their colour combinations
    dict_bit={'00':0,'01':1,'10':2,'11':3}
    num_list=[dict_bit[chunk] for chunk in bitlist]


    # np.set_printoptions(threshold=np.inf)

    #matrix for QR
    global size ,module_size
    size=math.ceil(math.sqrt(len(num_list)))
    matrix = np.zeros((size,size),dtype='uint8')

    # print(matrix)
    index=0
    for row in range(size):
        for column in range(size):
            if index<len(num_list):
                matrix[row,column]=num_list[index]
                index+=1

    #mappting numberts to their rgb values
    colour_map={0:(0,0,0),
                1:(255,0,0),
                2:(0,255,0),
                3:(0,0,255)}

    module_size=20 
    col_matrix=np.zeros((size*module_size,size*module_size,3),dtype=np.uint8)

    for row in range(size):
        for column in range(size):

                temp = matrix[row,column]
                colour=colour_map[temp]

                y_start=row * module_size   #increase the size of each block
                y_end= module_size +y_start

                x_start=column * module_size
                x_end= module_size +x_start

                col_matrix[y_start:y_end,x_start:x_end]=colour

    qr=img.fromarray(col_matrix)
    qr.save('qr.png')
    out_image=ctk.CTkImage(dark_image=img.open('qr.png'),size=(370,370))
    out_label.configure(image=out_image)
    out_label.image = out_image #type: ignore


def QR_text(module_size=20):

    #decoding colour QR
    file_path=filedialog.askopenfilename(title='Select a QR png file',filetypes=[('PNG Files','*.png')])

    if not file_path:
        return
    
    colour_qr = img.open(file_path)
    decod_array=np.array(colour_qr)

    #mapping from rgb values to numbers
    colour_num={(0,0,0):0,
                (255,0,0):1,
                (0,255,0):2,
                (0,0,255):3}
    
    size=int(decod_array.shape[0]//module_size)
    
    decod_num=np.zeros((size,size),dtype=np.uint8)
    i=0
    for row in range(0,size*module_size,module_size):
        j=0
        for column in range(0,size*module_size,module_size):
            temp=decod_array[row,column]
            decod_num[i,j]=colour_num[tuple(temp)]
            j+=1
        i+=1


    #mapping numbers back to bits with accordance to teir numbers
    num_bits={0:'00',1:'01',2:'10',3:'11'}

    dec_list=[]
    for row in range(size):
        for column in range(size):
                dec_list.append(int(decod_num[row,column]))
                

    dec_bits='' 
    for i in dec_list:
        dec_bits+=num_bits[i]


    normal_string=''.join(chr(int(dec_bits[i:i+8],2)) 
                        for i in range(0,len(dec_bits),8))
    O_textbox.configure(state='normal')
    O_textbox.delete('1.0','end')
    O_textbox.insert('1.0',normal_string) 
    O_textbox.configure(state='disabled')

def download():
    save_path=filedialog.asksaveasfilename(title='Save the QR as',defaultextension='.png',
                                            filetypes=[('PNG Files','*.png')])
    
    if not save_path:
        return
    else:   
        try:
            qr=img.open('qr.png')
            qr.save(save_path)
        except FileNotFoundError:
            return 
          
                  
app=ctk.CTk()
app.title('Spectrum QR')
app.geometry('1200x800')
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

bg=ctk.CTkImage(dark_image=img.open('bg.jpg'),size=(1200,800))
bg_label=ctk.CTkLabel(app,text='',image=bg)
bg_label.place(x=0,y=0,relwidth=1,relheight=1)

qr_frame=ctk.CTkFrame(app,width=500,height=500,corner_radius=30,fg_color="#4C5752")
qr_frame.place(x=575,y=125)

input_button=ctk.CTkButton(app,text='Convert Text To QR',
                           width=200,height=80,corner_radius=30,
                           command=text_QR,font=('Times',24),fg_color="#4C5752")
input_button.place(x=145,y=270)

I_textbox=ctk.CTkTextbox(app,width=450,height=200,corner_radius=30,font=('Times',22))
I_textbox.place(x=50,y=50)

O_textbox=ctk.CTkTextbox(app,width=450,height=200,corner_radius=30,font=('Times',22))
O_textbox.configure(state='disabled')
O_textbox.place(x=50,y=400)


output_button=ctk.CTkButton(app,text='Convert QR To Text',corner_radius=30,
                            width=200,height=80,command=QR_text,
                            font=('Times',24),fg_color="#4C5752")
output_button.place(x=145,y=630)

out_label=ctk.CTkLabel(qr_frame,text='')
out_label.place(x=65,y=65)

download_button=ctk.CTkButton(app,text='Download',
                           width=200,height=80,corner_radius=30,
                           command=download,font=('Times',24),fg_color="#494E4C")
download_button.place(x=900,y=650)



app.mainloop()






  



          


































































