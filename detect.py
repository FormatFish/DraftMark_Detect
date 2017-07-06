#coding=utf-8
import argparse
from image_process import Image_preprocess
import cv2
from skimage import io
import number_identity
from utils import check_words
ap = argparse.ArgumentParser()
ap.add_argument("-i" , "--image" , required = True , help = "path to input image")
ap.add_argument("-k" , "--apikey" , required = True , help="API Key applying from ai.baidu.com")
ap.add_argument("-s" , "--serectkey" , required = True , help="Serect Key applying from ai.baidu.com")
args = vars(ap.parse_args())

ips = Image_preprocess(args["image"])
cnts = ips.detect_contours()
# print [cv2.contourArea(item) for item in cnts]
c = sorted(cnts , key = cv2.contourArea , reverse=True)[0]
rotated , rotated_image = ips.alig_image(c)
wraped = ips.get_target_piece(rotated , rotated_image)
piece_cnts = ips.piece_detect(wraped)
interval , target_c = ips.get_max_cnt_and_interval_from_pieces(piece_cnts)

x , y , w , h = cv2.boundingRect(target_c)
target_image = wraped[y:y+h , x:x+w]

io.imsave("number.jpg" , target_image)

words = number_identity.getTextInfo("number.jpg" , args["apikey"] , args["serectkey"])
res = check_words(words)

res = res - 2 * interval * 0.1

x , y , w , h = cv2.boundingRect(c)
res_image = cv2.rectangle(ips.image.copy() , (x , y) , (x+w , y+h) , (0 , 255 , 0) , 2)
res_image = cv2.putText(res_image , str(res) + "M" , (100 , 100) , cv2.FONT_HERSHEY_SIMPLEX , 3 , (0 , 255 , 0) , 2)

cv2.imshow("result" , res_image)
cv2.waitKey(0)