from posixpath import join
import cv2 as cv
import numpy as np
import os
import random
import math
import base64
import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory

#from skimage.metrics import structural_similarity as ssim
#import sklearn.metrics as skm

# your basic path
#exp_path = '/DATA/yangmengmeng/liufei/DeepHomography-master/Data/annotation/'
# # new warp img save path
# warp_save_path = exp_path+'warp_i/'
# v_file_path = exp_path+'visible/'
# i_file_path = exp_path+'infrared/'
# txt_point_path_i = exp_path+'point_annotation/i_point_annotation/'
# txt_point_path_v = exp_path+'point_annotation/v_point_annotation/'

class warp_lf_2(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master

        self.pack()
        self.visible_dir = ''
        self.infrared_dir = ''
        self.exp_path = ''
        self.point_i_dir = ''
        self.point_v_dir = ''
        self.warp_save_path = ''
        self.img_order = 0
        self.img_num = 0
        # ----------------- GUI 部件 ---------------------
        # dir entry & load
        self.create_btns()



    def create_btns(self):
        self.label0 = Label(self, text="标注根目录:")
        self.label0.grid(row=0, column=0, sticky=E+W)

        self.label1 = Label(self, text="Z目录:")
        self.label1.grid(row=3, column=0, sticky=E+W)

        self.label2 = Label(self, text="T目录:")
        self.label2.grid(row=1, column=0, sticky=E+W)

        self.label3 = Label(self, text="Z标注目录:")
        self.label3.grid(row=4, column=0, sticky=E+W)

        self.label4 = Label(self, text="T标注目录:")
        self.label4.grid(row=2, column=0, sticky=E+W)

        self.label6 = Label(self, text="开始:")
        self.label6.grid(row=6, column=0, sticky=E+W)

        self.btn0 = Button(self, text="选择root文件夹",
                            command = self.get_exp_dir)
        self.btn0.grid(row=0, column=1, sticky=E+W)

        self.btn1 = Button(self, text="选择Z文件夹",
                           command=self.get_v_dir)
        self.btn1.grid(row=3, column=1, sticky=E+W)

        self.btn2 = Button(self, text="选择T文件夹",
                           command=self.get_i_dir)
        self.btn2.grid(row=1, column=1, sticky=E+W)

        self.btn3 = Button(self, text="选择Z_point文件夹",
                           command=self.get_point_v_dir)
        self.btn3.grid(row=4, column=1, sticky=E+W)

        self.btn4 = Button(self, text="选择T_point文件夹",
                           command=self.get_point_i_dir)
        self.btn4.grid(row=2, column=1, sticky=E+W)


        self.ldBtn = Button(self, text="开始加载", command=self.warp)
        self.ldBtn.grid(row=6, column=1, columnspan=2, sticky=N+E+W)


        # self.v_file_path = self.get_v_dir()
        # self.i_file_path = self.get_i_dir()
        # self.exp_path = self.get_exp_dir()
        # self.point_i_dir = self.get_point_v_dir()
        # self.point_v_dir = self.get_point_i_dir()
        return 

    
    def get_v_dir(self):
        self.visible_dir = askdirectory()
        print(self.visible_dir)

    def get_i_dir(self):
        self.infrared_dir = askdirectory()
        print(self.infrared_dir)

    def get_point_v_dir(self):
        self.point_v_dir = askdirectory()
        print(self.point_v_dir)

    def get_point_i_dir(self):
        self.point_i_dir = askdirectory()
        print(self.point_i_dir)

    def get_exp_dir(self):
        self.exp_path = askdirectory()
        print(self.exp_path)

    def get_warp_dir(self):
        self.warp_save_path = askdirectory()
        print(self.warp_save_path)



    def read_points(self, txt_point_path):

        count = 0
        if not os.path.exists(txt_point_path):
            print('No .txt label file found in the specified dir!')
            messagebox.showwarning(
                title='警告', message="文件夹中没有对应图像的txt标注文件")
            return 
        else:
            for index, line in enumerate(open(txt_point_path,'r')):
                count += 1

            with open(txt_point_path, 'r') as f:
                p = [[]]
                for i in range(0,count):
                    line = f.readline().split()
                    p[i] = [int(line[0]),int(line[1])]
                    p.append(p[i])
                return p

    def warp(self):
        motion_blur_num = 0
        gaussian_blur_num = 0
        gaussian_noise_num = 0
        rotate_random_num = 0
        self.warp_save_path = os.path.join(self.exp_path, 'annotation')
        # for file_order,file_name_v in enumerate(os.listdir(self.v_file_path)):

        #     file_order = "{:0>3}".format(file_order + 1) 
        #     file_num = len(os.listdir(self.v_file_path))
        #     file_name_i = file_name_v.replace('v','i')
        self.img_num = len(os.listdir(self.visible_dir))
        #     file_num = "{:0>3}".format(file_num)
        #     print('file_name: '+file_name_i.replace('_i','')+' file_num: %s'%file_order+'/%s'%file_num)
        for self.img_order,img_name_v in enumerate(os.listdir(self.visible_dir)):
            img_name_i = img_name_v.replace('Z','T')
            self.img_order = "{:0>3}".format(self.img_order + 1) 
            #original_image = cv.imread(exp_path+'infrared/'+'i%s'%order+'.jpg')
            img_path_i = os.path.join(self.infrared_dir,img_name_i)
            original_image = cv.imread(img_path_i)

            #target_image = cv.imread(exp_path+'visible/'+'v%s'%order+'.jpg')
            img_path_v = os.path.join(self.visible_dir,img_name_v)
            target_image = cv.imread(img_path_v)
            annotation_point_i = os.path.join(self.point_i_dir,img_name_i.replace('jpg','txt'))
            annotation_point_v = os.path.join(self.point_v_dir,img_name_v.replace('jpg','txt'))
            src_more_i_point= np.float32(
                self.read_points(annotation_point_i)
                ).reshape(-1,1,2)

            den_more_v_point= np.float32(
                self.read_points(annotation_point_v)
                ).reshape(-1,1,2)

            #H, status = cv.findHomography(src_more_i_point, den_more_v_point, cv.RANSAC ,6.0)#num from 1 to 10
            H1, status = cv.findHomography(src_more_i_point, den_more_v_point, 0)
        
            H_Random = self.Random_H()
            if int(self.img_order)%7 == 0:
                H_Random = self.Random_rotate_H()
                rotate_random_num = rotate_random_num + 1
            
            H2 = np.dot(H_Random,H1)
            
            for i in range(0,3):
                for j in range(0,3):
                    H2[i][j] = H2[i][j]/H2[2][2]
            homo_save_path_h1 = self.exp_path + '/gt_homography.txt'
            homo_save_path_h2 = self.exp_path + '/gt_and_random_homography.txt'
            
            self.homo_writer(H1,homo_save_path_h1)
            self.homo_writer(H2,homo_save_path_h2)


            warp_random_i_1 = cv.warpPerspective(original_image, H2, (target_image.shape[1], target_image.shape[0]))
            warped_i = cv.warpPerspective(original_image, H1, (target_image.shape[1], target_image.shape[0]))
            target_random_v = cv.warpPerspective(target_image, H_Random, (target_image.shape[1], target_image.shape[0]))
            warp_i_save_path = os.path.join(self.warp_save_path, 'warp_i')
            warp_i_random_save_path = os.path.join(self.warp_save_path,'warp_i_random')

            # if int(self.img_order)%9 == 0:
            #     target_random_v = self.motion_blur(target_random_v)
            #     motion_blur_num = motion_blur_num + 1
            
            # if int(self.img_order)%13 == 0 and int(self.img_order)%9 !=0:
            #     self.GaussianBlur(target_random_v)
            #     gaussian_blur_num = gaussian_blur_num + 1
            
            # if int(self.img_order)%17 == 0 and int(self.img_order)%9 !=0 and int(self.img_order)%13 !=0:
            #     self.gaussian_noise(target_random_v)
            #     gaussian_noise_num = gaussian_noise_num + 1

            random_v_save_path = os.path.join(self.warp_save_path,'random_visible')
            if not os.path.exists(warp_i_random_save_path):
                os.makedirs(warp_i_random_save_path)
            if not os.path.exists(warp_i_save_path):
                os.makedirs(warp_i_save_path)
            if not os.path.exists(random_v_save_path):
                os.makedirs(random_v_save_path)
            warp_i_img_path = os.path.join(warp_i_save_path,img_name_i.replace('T','warp_T'))
            random_v_img_path = os.path.join(random_v_save_path,img_name_v.replace('Z','random_Z'))
        
            cv.imwrite(warp_i_img_path,warped_i)
            cv.imwrite(random_v_img_path,target_random_v)

            #measure_index(warp_i_img_path,random_v_img_path,img_path_v,warped_i,target_image,original_image)

            #warp_random_i_2 = cv.warpPerspective(warped_i, H_Random, (target_image.shape[1], target_image.shape[0]))
            cv.imwrite(os.path.join(warp_i_random_save_path,img_name_i.replace('T','warp_T_gt2random')),
                                                                                    warp_random_i_1)
            #cv.imwrite(warp_save_path+img_name_i+'_warpi_gt2random_2step.jpg',warp_random_i_2)
            #checker_board_path = exp_path + '/checker_board/' + file_name_i.replace('i','checker_board')
            checker_board_path = os.path.join(self.warp_save_path,"check_board")
            if not os.path.exists(checker_board_path):
                os.makedirs(checker_board_path)
            checker_board_path_1 = os.path.join(checker_board_path,"normal_warp")
            checker_board_path_2 = os.path.join(checker_board_path,"random_warp")
            if not os.path.exists(checker_board_path_1):
                os.makedirs(checker_board_path_1)
            if not os.path.exists(checker_board_path_2):
                os.makedirs(checker_board_path_2)
            checker_name1 = os.path.join(checker_board_path_1,img_name_v.replace('DJI','').replace('Z','Z_warp_T'))
            checker_name2 = os.path.join(checker_board_path_2,img_name_v.replace('DJI','').replace('Z','random_Z_T'))
            #checker_name3 = checker_board_path +'/checker_board_gt2random_2step_warpi_v.jpg'
            self.checker_board(warped_i,target_image,checker_name1)
            self.checker_board(warp_random_i_1,target_random_v,checker_name2)

            self.img_num = "{:0>3}".format(self.img_num)
            print('  image_num: %s'%self.img_order+'/%s'%self.img_num)  
            print('rotate random num:',rotate_random_num,' motion blur num:',
                            motion_blur_num,' gaussian blur num:',gaussian_blur_num,
                            ' gaussian noise num:',gaussian_noise_num) 

        
        
        messagebox.showinfo(
                title='完成', message="此文件夹warp图像已成功生成!")


    def homo_writer(self, H,homo_txt_path):
        with open(homo_txt_path,'a+') as f:
            for i in range(0,3):
                for j in range(0,3):
                    f.write(str('{:.10f}'.format(H[i][j])))
                    f.write(' ')
            f.write('\n')

    def homo_reader(self, homo_txt_path):
        H = np.zeros((3,3))
        with open(homo_txt_path,'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                num = 0
                for i in range(0,3):
                    for j in range(0,3):
                        H[i][j] = float(line.split(' ')[num])
                        num = num +1
        return H

    def checker_board(self, img_i,img_v,checker_name):
        checker_img = img_v
        block_width = 1920//16
        block_height = 1080//10
        black_block = img_i
        for row in range(10):
            for col in range(16):
                if (row+col)%2==0:
                    row_begin = row*block_height
                    row_end = row_begin+block_height
                    col_begin = col*block_width
                    col_end = col_begin+block_width
                    checker_img[row_begin:row_end,col_begin:col_end] = black_block[row_begin:row_end,col_begin:col_end]
        cv.imwrite(checker_name,checker_img)

    def Random_H(self):
        H = np.zeros((3,3))
        H[0][0] = random.uniform(0.8, 1.1)
        H[1][1] = random.uniform(0.8, 1.1)
        H[0][1] = random.uniform(-0.3, 0.3)
        H[1][0] = random.uniform(-0.2, 0.2)
        H[0][2] = random.randint(-200, 200)
        H[1][2] = random.randint(-100, 100)
        H[2][0] = random.uniform(-0.0001, 0.0001)
        H[2][1] = random.uniform(-0.0001, 0.0001)
        H[2][2] = 1

        return H

    def Random_rotate_H(self):

        num = random.uniform(-0.1,0.1)

        #大于0时向下旋转
        theta = math.pi * num
        H = np.zeros((3,3))
        H[2][2] = 1
        H[0][0] = math.cos(theta)
        H[1][1] = math.cos(theta)
        H[0][1] = -math.sin(theta)
        H[1][0] = math.sin(theta)
        if num>0:
            H[0][2] = 2500 * num
            H[1][2] = -2500 * num
        else:
            H[0][2] = 1300 * num
            H[1][2] = -3000 * num
        H[2][0] = 0
        H[2][1] = 0
        print('random rotate theta:',theta)

        return H

    def motion_blur(self, image, degree=10, angle=20):
        image = np.array(image)
        # 这里生成任意角度的运动模糊kernel的矩阵， degree越大，模糊程度越高
        M = cv.getRotationMatrix2D((degree/2, degree/2), angle, 1)
        motion_blur_kernel = np.diag(np.ones(degree))
        motion_blur_kernel = cv.warpAffine(motion_blur_kernel, M, (degree, degree))
        
        motion_blur_kernel = motion_blur_kernel / degree        
        blurred = cv.filter2D(image, -1, motion_blur_kernel)
        # convert to uint8
        cv.normalize(blurred, blurred, 0, 255, cv.NORM_MINMAX)
        blurred = np.array(blurred, dtype=np.uint8)
        return blurred

    def GaussianBlur(self, image,degree=10):
        image = cv.GaussianBlur(image, ksize=(degree, degree), sigmaX=0, sigmaY=0)
        return image

    def gaussian_noise(self, image, degree=None):
        row, col, ch = image.shape
        mean = 0
        if not degree:
            var = np.random.uniform(0.004, 0.01)
        else:
            var = degree
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        cv.normalize(noisy, noisy, 0, 255, norm_type=cv.NORM_MINMAX)
        noisy = np.array(noisy, dtype=np.uint8)
        return noisy


if __name__=="__main__":

    open_icon = open("D:\py36\chessboard.ico","rb")
    b64str = base64.b64encode(open_icon.read())
    icon = b64str
    icondata= base64.b64decode(icon)
    ## The temp file is icon.ico
    tempFile= "icon.ico"
    iconfile= open(tempFile,"wb")
    ## Extract the icon
    iconfile.write(icondata)
    iconfile.close()
    root = Tk()
    root.wm_iconbitmap(tempFile)
    ## Delete the tempfile
    os.remove(tempFile)

    root.title('配准棋盘格生成—lf')
    root.geometry("300x200+700+300") 
    tool = warp_lf_2(master = root)
    root.mainloop()






