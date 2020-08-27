from PIL import Image
import glob
from natsort import natsorted
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime

#フォルダ名を入れます
folderName = "./image"
     
#該当フォルダから画像のリストを取得。読み込みたいファイル形式を指定。ここではpng
print('input file')
picList_0 = glob.glob(folderName + "/*.png")

picList = natsorted(picList_0)

print(picList)
     
#figオブジェクトの作成
fig = plt.figure()

# 外枠を消す
plt.axis("off")
     
#空のリスト作成
ims = []
     
#画像ファイルを空のリストの中に1枚ずつ読み込み
for i in range(len(picList)):
    #読み込んで付け加えていく
    tmp = Image.open(picList[i])
    ims.append([plt.imshow(tmp)])     
     
print('making movie')
#アニメーション作成
ani = animation.ArtistAnimation(fig, ims, interval=10)
 
#アニメーション保存。ファイル名を入れてください。ここではtest.gif
now = datetime.datetime.now()
save_filename = "./image/" + now.strftime('%Y%m%d_%H%M%S') + ".gif"
ani.save(save_filename)