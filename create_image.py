import os
import numpy as np
import re

import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.animation as animation
import numpy as np; np.random.seed(0)
import pandas as pd

count = 0
inputDir = './'
flag_vector_plot = -1
output_val_num = -1

def create_full_path(file_name):
    global inputDir
    return inputDir + file_name

def isd(N):
    return bool(re.compile("^[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?$").match(N))

def sort(A):
    B=list(np.copy(A))
    B.sort(key = lambda x: float(x) if isd(x) else x)
    return B

def create_f(f_name):
    global count
    #print(f_name)
    plt.cla()  

    # ファイル読み込み
    pd_para_data = pd.read_csv(f_name, nrows=1)
    data = np.loadtxt(f_name, delimiter=",", skiprows=3)

    # パラメータの設定
    time_data = pd_para_data.iat[0,1]
    nc = pd_para_data.iat[0,2]
    nl1 = pd_para_data.iat[0,3]
    nl2 = pd_para_data.iat[0,4]
    all_domain = pd_para_data.iat[0,5]

    nc1 = nc+1
    interface_start = (nc1 * nc1) + 4 * nc * (nl1-1)


    # 3: velocity
    # 5: B
    # 8: al

    if flag_vector_plot == 1:
        #plt.quiver(np_crd_x,np_crd_y,np_v_x,np_v_y,angles='xy',scale_units='xy',scale=None, width=0.01)

        plt.quiver(data[:, 1],
                    data[:, 2],
                    data[:, int(output_val_num)],
                    data[:, int(output_val_num + 1)],
                    angles='xy',scale_units='xy',scale=None, width=0.01)

    # 界面描画
    for i in range(4*nc):
        if i == 4*nc - 1:
            plt.plot([data[int(i+interface_start), 1], data[int(interface_start), 1]], [data[int(i+interface_start), 2], data[int(interface_start), 2]],'m-.', lw=1.0, label = "Interface")
        else:
            plt.plot([data[int(i+interface_start), 1], data[int(i+1+interface_start), 1]], [data[int(i+interface_start), 2], data[int(i+1+interface_start), 2]],'m-.', lw=1.0)

    plt.xlabel('$\it{x}$'+' [m]')
    plt.ylabel('$\it{y}$'+' [m]')
    plt.xlim(-1.0*all_domain, all_domain)
    plt.ylim(-1.0*all_domain, all_domain)
    plt.text(all_domain/3.0, -1.0*all_domain*0.9, "%e s" % time_data)
    plt.tight_layout()
    plt.axes().set_aspect('equal')

    plt.savefig('./image/%d.png' % count,format = 'png', dpi=1000)
    count += 1

count = 0
print("input data >>>")
inputDir = input().strip()+"/"

print("vector plot on(1) / off(0) >>>")
flag_vector_plot = int(input())

if flag_vector_plot == 1:
    print("kind of vectors. 3:v, 5:B, 8:al >>>")
    output_val_num = int(input())

list1 = os.listdir(inputDir)
list2 = sort(list1)

list3 = [s for s in list2 if '.csv' in s]
length = len(list3)
print(length)

list4 = list(map(create_full_path, list3))
print(list4)

fig = plt.figure()
image_list = []

for i in range(length):
    create_f(list4[i])