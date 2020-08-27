import os
import numpy as np
import re

import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.animation as animation
import numpy as np; np.random.seed(0)
import pandas as pd
import time
from numba import jit
import functools

def create_full_path(file_name, inputDir):
    return inputDir + file_name

def isd(N):
    return bool(re.compile("^[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?$").match(N))

def sort(A):
    B=list(np.copy(A))
    B.sort(key = lambda x: float(x) if isd(x) else x)
    return B

def create_f(f_name, zoom_para, width_par_vec, output_val_num, flag_vector_plot, count):
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
        x_max = np.amax(np.absolute(data[:, int(output_val_num)]))
        y_max = np.amax(np.absolute(data[:, int(output_val_num + 1)]))

        base = x_max
        if x_max < y_max:
            base = y_max

        plt.quiver(data[:, 1],
                    data[:, 2],
                    data[:, int(output_val_num)],
                    data[:, int(output_val_num + 1)],
                    angles='xy',scale_units='width',scale=base*float(width_par_vec), width=0.01)

    # 界面描画
    for i in range(4*nc):
        if i == 4*nc - 1:
            plt.plot([data[int(i+interface_start), 1], data[int(interface_start), 1]], [data[int(i+interface_start), 2], data[int(interface_start), 2]],'m-.', lw=1.0, label = "Interface")
        else:
            plt.plot([data[int(i+interface_start), 1], data[int(i+1+interface_start), 1]], [data[int(i+interface_start), 2], data[int(i+1+interface_start), 2]],'m-.', lw=1.0)

    plt.xlabel('$\it{x}$'+' [m]')
    plt.ylabel('$\it{y}$'+' [m]')
    plt.xlim(-1.0*all_domain/float(zoom_para), all_domain/float(zoom_para))
    plt.ylim(-1.0*all_domain/float(zoom_para), all_domain/float(zoom_para))
    plt.text(all_domain/float(zoom_para)/3.0, -1.0*all_domain/float(zoom_para)*0.9, "%e s" % time_data, backgroundcolor='white')
    plt.tight_layout()
    plt.axes().set_aspect('equal')

    plt.savefig('./image/%d.png' % count,format = 'png', dpi=1000)

def main():
    count = 0
    zoom_para = 1
    width_par_vec = 20
    flag_vector_plot = 0
    output_val_num = 3
    skip_num = 1

    print("input data >>>")
    inputDir = input().strip()+"/"

    print("skip_num >>>")
    skip_num = int(input())

    print("zoom para (default is 1)>>>")
    zoom_para = input()

    print("vector plot on(1) / off(0) (default is 0)>>>")
    flag_vector_plot = int(input())

    if flag_vector_plot == 1:
        print("kind of vectors. 3:v, 5:B, 8:al (default is 3)>>>")
        output_val_num = int(input())

        print("width of plot / the largest vector (default is 20)>>>")
        width_par_vec = input()

    list1 = os.listdir(inputDir)
    list2 = sort(list1)

    list3 = [s for s in list2 if '.csv' in s]
    length = len(list3)
    print(length)

    list4 = list(map(functools.partial(create_full_path, inputDir=inputDir), list3))
    print(list4)

    fig = plt.figure()
    image_list = []

    for i in range(length):
        if int(i % skip_num) == 0: 
            create_f(list4[i], zoom_para, width_par_vec, output_val_num, flag_vector_plot, count)
            count += 1

main()