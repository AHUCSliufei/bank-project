import cv2
import os


def save_img(video_path):
    videos = os.listdir(video_path)
    for video_name in videos:
        if video_name.find('T')>0:
            file_name_i = video_name.split('.')[0]
            folder_name_i = os.path.join(video_path, file_name_i)
            file_name_v = file_name_i.replace('T','Z')
            folder_name_v = os.path.join(video_path, file_name_v)
            if not os.path.exists(folder_name_i):
                os.makedirs(folder_name_i, exist_ok=True)
            if not os.path.exists(folder_name_v):
                os.makedirs(folder_name_v, exist_ok=True)
            video_path_i = video_path+'/'+file_name_i+'.mp4'
            video_path_v = video_path+'/'+file_name_v+'.mp4'
            vc_i = cv2.VideoCapture(video_path_i)
            vc_v = cv2.VideoCapture(video_path_v)
            c = 0
            path_list_i = []
            path_list_v = []
            frame_num = 0
            rval_i = vc_i.isOpened()
            

            while rval_i:
                c = c + 1

                rval_i, frame_i = vc_i.read()
                rval_v, frame_v = vc_v.read()

                if c %50 == 0:
                    frame_num = frame_num + 1
                    if rval_i:
                        frames = "{:0>5}".format(c)
                        frame_path_i = os.path.join(folder_name_i, 'i_' + str(frames) + '.jpg')
                        frame_path_v = os.path.join(folder_name_v, 'v_' + str(frames) + '.jpg')
                        if frame_num > 1:
                            frame_last_path_i = path_list_i[-1]
                            ahash= hash_index_com(frame_i,frame_last_path_i)
                            if ahash > 30:
                                print('average hash similarity: ',str(ahash))
                                print(frame_last_path_i.replace('i','i_v'))
                                print(frame_path_i.replace('i','i_v'))
                                cv2.imwrite(frame_path_i, frame_i)
                                cv2.imwrite(frame_path_v, frame_v)
                                path_list_i.append(frame_path_i)
                                path_list_v.append(frame_path_v)
                        else:
                            cv2.imwrite(frame_path_i, frame_i)
                            cv2.imwrite(frame_path_v, frame_v)
                            path_list_i.append(frame_path_i)
                            path_list_v.append(frame_path_v)
                        cv2.waitKey(1)
                    else:
                        break
            vc_i.release()
            print('save_success')
            print(folder_name_i.replace('i','i_v'))


#均值哈希算法
def aHash(img):
    # 缩放为8*8
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

#差值感知算法
def dHash(img):
    #缩放8*8
    img=cv2.resize(img,(9,8),interpolation=cv2.INTER_CUBIC)
    #转换灰度图
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hash_str=''
    #每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if   gray[i,j]>gray[i,j+1]:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
    return hash_str

#Hash值对比
def cmpHash(hash1,hash2):
    n=0
    #hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    #遍历判断
    for i in range(len(hash1)):
        #不相等则n计数+1，n最终为相似度
        if hash1[i]!=hash2[i]:
            n=n+1
    return n

def hash_index_com(img1,img2_path):
    
    img2=cv2.imread(img2_path)
    hash1= aHash(img1)
    hash2= aHash(img2)
    ahash=cmpHash(hash1,hash2)

    return ahash

if __name__ == '__main__':
    # path to video folds eg: video_path = './Test/'

    videos_path = 'E:/UAV_DATA/2021-10-08'
    videos_list = os.listdir(videos_path)
    for videos in videos_list:
        video_path = os.path.join(videos_path,videos)
        save_img(video_path)

    