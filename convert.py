import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

for (path, dir, files) in os.walk("./tracking_train_pcd"):
    for filename in files:
        ext = os.path.splitext(filename)[-1]
        if ext == '.bin':            
            path = path.replace("\\", "/")
            folder = (path.split("/"))[2]
            print(path, filename)

            raw = np.fromfile(path + "/" + filename, dtype='float32', sep="")
            raw = raw.reshape([raw.shape[0] // 4, 4])
            pc = raw[:, 0:3]

            total_points = []

            for i in range(pc.shape[0]):
                xyz = [float(pc[i][0]), float(pc[i][1]), float(pc[i][2])]
                total_points.append(xyz)

            total_points = np.array(total_points)
            label_path = path.replace("tracking_train_pcd", "tracking_train_label").replace("result_", "").replace("_frame", "") + "/" + filename.replace(".bin", ".txt")

            label = open(label_path, 'r')

            while True:
                line = label.readline()
                line = line.replace("\n", "")

                if not line: 
                    break

                line = line.split(" ")

                center = np.array([float(line[2]), float(line[3]), float(line[4])])

                theta = -float(line[8])
                ob_center_pc = total_points - center

                z_rotation_M = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
                rotated_pc = np.dot(ob_center_pc, z_rotation_M)
                rotated_pc = ob_center_pc

                crop_pc = []

                for i in range(len(rotated_pc)):
                    new_x = rotated_pc[i][0]
                    new_y = rotated_pc[i][1]
                    new_z = rotated_pc[i][2]

                    if new_x < float(line[5]) / 2 and new_x > -float(line[5]) / 2:
                        if new_y < float(line[6]) / 2 and new_y > -float(line[6]) / 2:
                            if new_y < float(line[7]) / 2 and new_y > -float(line[7]) / 2:
                                crop_pc.append([new_x, new_y, new_z])
                
                crop_pc = np.array(crop_pc)

                if crop_pc.shape[0] > 100:
                    label_txt = open("./result/{0}/{1}_{2}_{3}.txt".format(str(line[1]), folder, filename.replace(".bin", ""), str(line[0])), 'w')
                    for i in range(crop_pc.shape[0]):
                        label_txt.write(str(crop_pc[i][0]) + " " + str(crop_pc[i][1]) + " " + str(crop_pc[i][2]) + "\n")

                    label_txt.close()
                    
                    # X = crop_pc[:, 0]
                    # Y = crop_pc[:, 1]
                    # Z = crop_pc[:, 2]

                    # fig = plt.figure()
                    # ax = fig.gca(projection='3d')

                    # ax.scatter(X, Y, Z, s=1, c=Z)

                    # ax.set_xlabel('X')
                    # ax.set_ylabel('Y')
                    # ax.set_zlabel('Z')
                    # plt.savefig("./result/{0}/{1}_{2}_{3}.png".format(str(line[1]), folder, filename.replace(".bin", ""), str(line[0])), dpi=300)
                    # plt.close('all')
            label.close()