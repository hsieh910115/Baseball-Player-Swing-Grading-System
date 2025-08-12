import numpy as np
import matplotlib.pyplot as plt
'''
0   hip
1   right hip
2   right knee
3   right foot 
4   left hip
5   left knee    
6   left foot
7   spine
8   thorax
9   neck
10  head
11  left shoulder
12  left elbow
13  left wrist
14  right shoulder
15  right elbow
16  right wrist
'''
#################################functions################################
def get_theta(i, j, k, frame_coordinates):
    A = frame_coordinates[i] 
    B = frame_coordinates[j] 
    C = frame_coordinates[k] 
    BA = A - B
    BC = C - B
    dot_product = np.dot(BA, BC)                    #BA dot BC
    norm_BA = np.linalg.norm(BA)                    #|BA|
    norm_BC = np.linalg.norm(BC)                    #|BC|
    cos_theta = dot_product / (norm_BA * norm_BC)   #cos theta = (BA dot BC) / |BA| * |BC|
    cos_theta = np.clip(cos_theta, -1.0, 1.0)       #確保範圍在-1到1之間
    theta_radians = np.arccos(cos_theta)            #得到弧度theta
    theta_degrees = np.degrees(theta_radians)       #得到角度theta
    return theta_degrees

def get_hip_rotation(frame_coordinates): #加入一個從右髖(1)畫出的水平yz平面的線的點來判斷髖轉正的角度
    A = frame_coordinates[4] 
    B = frame_coordinates[1] 
    C = (frame_coordinates[1][0], frame_coordinates[4][1], frame_coordinates[4][2])
    BA = A - B
    BC = C - B
    dot_product = np.dot(BA, BC)
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)
    cos_theta = dot_product / (norm_BA * norm_BC)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    theta_radians = np.arccos(cos_theta)
    theta_degrees = np.degrees(theta_radians)
    return theta_degrees

def get_body_side_angle(frame_coordinates):
    A = frame_coordinates[8] 
    B = frame_coordinates[0] 
    C = (frame_coordinates[8][0], frame_coordinates[8][1], frame_coordinates[0][2]) # y of hip(0), x and z of thorax
    BA = A - B
    BC = C - B
    dot_product = np.dot(BA, BC)
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)
    cos_theta = dot_product / (norm_BA * norm_BC)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    theta_radians = np.arccos(cos_theta)
    theta_degrees = np.degrees(theta_radians)
    return theta_degrees

def get_body_lean_angle(frame_coordinates):
    A = frame_coordinates[8] 
    B = frame_coordinates[0] 
    C = (frame_coordinates[0][0], frame_coordinates[8][1], frame_coordinates[8][2]) # x of hip(0), y and z of thorax
    BA = A - B
    BC = C - B
    dot_product = np.dot(BA, BC)
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)
    cos_theta = dot_product / (norm_BA * norm_BC)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    theta_radians = np.arccos(cos_theta)
    theta_degrees = np.degrees(theta_radians)
    return theta_degrees

def calculate_angle(frame_coordinates): #有輸出不同部位的角度
    theta_list = []
    theta_right_shoulder = get_theta(8, 14, 15, frame_coordinates) # thorax, right shoulder, right elbow
    print("theta right shoulder : ", theta_right_shoulder)
    theta_list.append(theta_right_shoulder)

    theta_right_elbow = get_theta(14, 15, 16, frame_coordinates) # right shoulder, right elbow, right wrist
    print("theta right elbow : ", theta_right_elbow)
    theta_list.append(theta_right_elbow)

    theta_left_shoulder = get_theta(8, 11, 12, frame_coordinates) # thorax, left shoulder, left elbow
    print("theta left shoulder : ", theta_left_shoulder)
    theta_list.append(theta_left_shoulder)

    theta_left_elbow = get_theta(11, 12, 13, frame_coordinates) # left shoulder, left elbow, left wrist
    print("theta left elbow : ", theta_left_elbow)
    theta_list.append(theta_left_elbow)

    theta_right_hip = get_theta(14, 1, 2, frame_coordinates) # right shoulder, right hip, right knee
    print("theta right hip : ", theta_right_hip)
    theta_list.append(theta_right_hip)

    theta_left_hip = get_theta(11, 4, 5, frame_coordinates) # left shoulder, left hip, left knee
    print("theta left hip : ", theta_left_hip)
    theta_list.append(theta_left_hip)

    theta_right_knee = get_theta(1, 2, 3, frame_coordinates) # right hip, right knee, right foot
    print("theta right knee : ", theta_right_knee)
    theta_list.append(theta_right_knee)

    theta_left_knee = get_theta(4, 5, 6, frame_coordinates) # left hip, left knee, left foot
    print("theta left knee : ", theta_left_knee)
    theta_list.append(theta_left_knee)

    theta_hip_rotation = get_hip_rotation(frame_coordinates)
    print("theta hip rotation : ", theta_hip_rotation)
    theta_list.append(theta_hip_rotation)

    theta_body_side = get_body_side_angle(frame_coordinates)
    print("theta body side angle : ", theta_body_side)
    theta_list.append(theta_body_side)

    theta_body_lean = get_body_lean_angle(frame_coordinates)
    print("theta body lean angle : ", theta_body_lean)
    theta_list.append(theta_body_lean)
    return theta_list


#畫圖
def draw_frame(coordinates, frame_index):
    x = list(coordinates[frame_index, :, 0])
    y = list(coordinates[frame_index, :, 2])
    z = list(-coordinates[frame_index, :, 1])
    #加入一個從右髖(1)畫出的水平yz平面的線的點(17)來判斷髖轉正的角度
    x.append(coordinates[frame_index][1][0])  # x of right hip(1), y and z of left hip(4)
    y.append(coordinates[frame_index][4][2])
    z.append(-coordinates[frame_index][4][1])
    #加入一個從中髖(0)畫出的水平xz平面的線的點(18)來判斷身體向本壘倒的角度
    x.append(coordinates[frame_index][8][0])  # y of hip(0), x and z of thorax
    y.append(coordinates[frame_index][0][2])
    z.append(-coordinates[frame_index][8][1])
    #加入一個從中髖(0)畫出的水平yz平面的線的點(19)來判斷身體前後倒的角度
    x.append(coordinates[frame_index][0][0])  # x of hip(0), y and z of thorax
    y.append(coordinates[frame_index][8][2])
    z.append(-coordinates[frame_index][8][1])
    # 定義骨架連接關係
    skeleton = [
        (0, 1), (1, 2), (2, 3),          # hip to right foot
        (0, 4), (4, 5), (5, 6),          # hip to left foot
        (0, 7), (7, 8), (8, 9), (9, 10), # hip to head
        (8, 11), (11, 12), (12, 13),     # thorax to left wrist
        (8, 14), (14, 15), (15, 16),     # thorax to right wrist
        (1, 17),                         # hip rotation 輔助 line
        (0, 18), (0,19)                  # body angle 輔助 line     
    ]

    # 定義關節點的顏色(身體關節點黑色，輔助點金色)
    colors = [
        'black', 'black', 'black', 'black', 'black', 
        'black', 'black', 'black', 'black', 'black', 
        'black', 'black', 'black', 'black', 'black', 
        'black', 'black', 'gold', 'gold', 'gold'
    ]

    # 創建 3D 圖形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 設置坐標軸範圍
    ax.set_xlim([-0.5, 0.5])
    ax.set_ylim([-0.5, 0.5])
    ax.set_zlim([-0.5, 0.5])
    # 設置坐標軸名稱
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    # 繪製散點圖
    ax.scatter(x, y, z, c=colors, marker='o')

    # 在每個點旁邊標註 index
    for i in range(len(x)):
        ax.text(x[i], y[i], z[i], f'{i}', color='black')

    #繪製骨架連接
    for joint1, joint2 in skeleton:
        ax.plot([x[joint1], x[joint2]], [y[joint1], y[joint2]], [z[joint1], z[joint2]], c='b')

    # 顯示圖形
    plt.show()

def draw_frame_double(coordinates1, frame_index1, coordinates2, frame_index2, similarity_point, grade_point):
    #處理第一個骨架的輔助點
    x1 = list(coordinates1[frame_index1, :, 0])
    y1 = list(coordinates1[frame_index1, :, 2])
    z1 = list(-coordinates1[frame_index1, :, 1])
    #加入一個從右髖(1)畫出的水平yz平面的線的點(17)來判斷髖轉正的角度
    x1.append(coordinates1[frame_index1][1][0])  # x of right hip(1), y and z of left hip(4)
    y1.append(coordinates1[frame_index1][4][2])
    z1.append(-coordinates1[frame_index1][4][1])
    #加入一個從中髖(0)畫出的水平xz平面的線的點(18)來判斷身體向本壘倒的角度
    x1.append(coordinates1[frame_index1][8][0])  # y of hip(0), x and z of thorax
    y1.append(coordinates1[frame_index1][0][2])
    z1.append(-coordinates1[frame_index1][8][1])
    #加入一個從中髖(0)畫出的水平yz平面的線的點(19)來判斷身體前後倒的角度
    x1.append(coordinates1[frame_index1][0][0])  # x of hip(0), y and z of thorax
    y1.append(coordinates1[frame_index1][8][2])
    z1.append(-coordinates1[frame_index1][8][1])

    #處理第二個骨架的輔助點
    x2 = list(coordinates2[frame_index2, :, 0])
    y2 = list(coordinates2[frame_index2, :, 2])
    z2 = list(-coordinates2[frame_index2, :, 1])
    #加入一個從右髖(1)畫出的水平yz平面的線的點(17)來判斷髖轉正的角度
    x2.append(coordinates2[frame_index2][1][0])  # x of right hip(1), y and z of left hip(4)
    y2.append(coordinates2[frame_index2][4][2])
    z2.append(-coordinates2[frame_index2][4][1])
    #加入一個從中髖(0)畫出的水平xz平面的線的點(18)來判斷身體向本壘倒的角度
    x2.append(coordinates2[frame_index2][8][0])  # y of hip(0), x and z of thorax
    y2.append(coordinates2[frame_index2][0][2])
    z2.append(-coordinates2[frame_index2][8][1])
    #加入一個從中髖(0)畫出的水平yz平面的線的點(19)來判斷身體前後倒的角度
    x2.append(coordinates2[frame_index2][0][0])  # x of hip(0), y and z of thorax
    y2.append(coordinates2[frame_index2][8][2])
    z2.append(-coordinates2[frame_index2][8][1])
    
    # 定義骨架連接關係
    skeleton = [
        (0, 1), (1, 2), (2, 3),          # hip to right foot
        (0, 4), (4, 5), (5, 6),          # hip to left foot
        (0, 7), (7, 8), (8, 9), (9, 10), # hip to head
        (8, 11), (11, 12), (12, 13),     # thorax to left wrist
        (8, 14), (14, 15), (15, 16),     # thorax to right wrist
        (1, 17),                         # hip rotation 輔助 line
        (0, 18), (0,19)                  # body angle 輔助 line     
    ]

    # 定義關節點的顏色(身體關節點黑色，輔助點金色)
    colors = [
        'black', 'black', 'black', 'black', 'black', 
        'black', 'black', 'black', 'black', 'black', 
        'black', 'black', 'black', 'black', 'black', 
        'black', 'black', 'gold', 'gold', 'gold'
    ]

    # 創建 3D 圖形，包含兩個子圖
    fig = plt.figure(figsize=(14, 6))
    
    #第一個子圖
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_title("STANDARD")
    # 設置坐標軸範圍
    ax1.set_xlim([-0.5, 0.5])
    ax1.set_ylim([-0.5, 0.5])
    ax1.set_zlim([-0.5, 0.5])
    # 設置坐標軸名稱
    ax1.set_xlabel('X axis')
    ax1.set_ylabel('Y axis')
    ax1.set_zlabel('Z axis')

    # 繪製散點圖
    ax1.scatter(x1, y1, z1, c=colors, marker='o')

    # 在每個點旁邊標註 index
    #for i in range(len(x1)):
    #    ax1.text(x1[i], y1[i], z1[i], f'{i}', color='black')

    #繪製骨架連接
    for joint1, joint2 in skeleton:
        ax1.plot([x1[joint1], x1[joint2]], [y1[joint1], y1[joint2]], [z1[joint1], z1[joint2]], c='b')

    #第二個子圖
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_title("YOU")
    # 設置坐標軸範圍
    ax2.set_xlim([-0.5, 0.5])
    ax2.set_ylim([-0.5, 0.5])
    ax2.set_zlim([-0.5, 0.5])
    # 設置坐標軸名稱
    ax2.set_xlabel('X axis')
    ax2.set_ylabel('Y axis')
    ax2.set_zlabel('Z axis')

    # 繪製散點圖
    ax2.scatter(x2, y2, z2, c=colors, marker='o')

    # 在每個點旁邊標註 index
    #for i in range(len(x2)):
    #    ax2.text(x2[i], y2[i], z2[i], f'{i}', color='black')

    #繪製骨架連接
    for joint1, joint2 in skeleton:
        ax2.plot([x2[joint1], x2[joint2]], [y2[joint1], y2[joint2]], [z2[joint1], z2[joint2]], c='b')


    #ax1.text(1.2, 0, 0, "Skeleton 1: Judge61", fontsize=12, color='red')
    #ax2.text(1.2, 0, 0, "Skeleton 2: Shohei", fontsize=12, color='green')
    frame_num = frame_index1 + 1
    fig.text(0.35, 0.83, f"frame : {frame_num}", fontsize=12, color='black')
    frame_num = frame_index2 + 1
    fig.text(0.84, 0.83, f"frame : {frame_num}", fontsize=12, color='black')
    fig.suptitle("Comparison of Two Skeletons", fontsize=16)
    # 顯示圖形
    fig.text(0.43, 0.1, f"Similarity Point : {similarity_point:.3f}", fontsize=12, color='black')
    fig.text(0.4835, 0.05, f"Grade : {grade_point:.3f}", fontsize=12, color='black')
    plt.tight_layout()
    plt.show()

#計算相似值
def similarity(thetas_1, thetas_2): #有輸出grade
    grades = [] #存所有角度的評分
    for theta_1, theta_2 in zip(thetas_1, thetas_2):
        #假設差距範圍是0~50度，分數為0~100分，50 / 100 = 0.5度，差0.5度扣一分
        delta_theta = np.abs(theta_1 - theta_2)
        grade = 100 - delta_theta / 0.9
        grades.append(grade)
    print("grade ", grades)    
    return np.sum(grades) / len(grades) #回傳所有角度平均的相似值

def grade(thetas_1, thetas_2):
    grades = []      # 存所有角度的評分
    grade = 0        # 評分加總
    similar = 0      # 相似度評分
    total_weight = 0 # 總共權重數
    for theta_1, theta_2 in zip(thetas_1, thetas_2):
        #假設差距範圍是0~50度，分數為0~100分，50 / 100 = 0.5度，差0.5度扣一分
        delta_theta = np.abs(theta_1 - theta_2)
        similar = 100 - delta_theta / 0.9
        grades.append(similar)
    #11個分數給11個權重:右肩、右肘、左肩、左肘、右髖、左髖、右膝、左膝、髖旋轉、側傾角度、後仰角度
    weights = [        1.5,   2,  1.5,  2,    1,   1,    1,   1,    2,       2,      1] 
    for i in range(len(weights)):
        grade_weight = grades[i] * weights[i]
        #print("grades[i] : ", grades[i], ",  weights[i] : ", weights[i])
        grade += grade_weight
        total_weight += weights[i]
    print("total weight : ", total_weight)
    return grade / total_weight
    
    
#######################################主程式##############################################
# 加載保存的 3D 坐標
# 能用檔案:                                                                                                                                                                                                                                                                                                                                                                                                                                           
# ohtani_1 : 90, ohtani_2 : 159, ohtani_3 : 257, ohtani_4 : 127, ohtani_5 : 251, ohtani_6 : 189, ohtani_7 : 135, ohtani_8 : 256, ohtani_9 : 149
# judge_1 : 139, judge_2 : 340, judge_3 : 76, judge_4 : 272, judge_5 : 116, judge_6 : 290, judge_7 : 80, judge_8 : 53, judge_9 : 34
coordinates_1 = np.load('/Users/zongyan/Desktop/EAI/finalproject/standard/judge_9.npy') 
print("coordinates_1 shape", coordinates_1.shape)
# 获取某帧的3D坐标
frame_num_1 = 34  # 實際偵數
frame_index_1 = frame_num_1 - 1   # 實際偵數的index
frame_coordinates_1 = coordinates_1[frame_index_1]
thetas_1 = calculate_angle(frame_coordinates_1)
#print("theta_1 ", thetas_1)

coordinates_2 = np.load('/Users/zongyan/Desktop/EAI/finalproject/tsai_9.npy') 
print("coordinates_2 shape", coordinates_2.shape)
# 获取某帧的3D坐标
frame_num_2 = 210  # 實際偵數
frame_index_2 = frame_num_2 - 1   # 實際偵數的index
frame_coordinates_2 = coordinates_2[frame_index_2]
thetas_2 = calculate_angle(frame_coordinates_2)
#print("theta_2 ", thetas_2)

similar_points = similarity(thetas_1, thetas_2)
print("similar_points : ", similar_points)
grade_points = grade(thetas_1, thetas_2)
print("grade points : ", grade_points)
#draw_frame(coordinates_1, frame_index_1)
#draw_frame(coordinates_2, frame_index_2)

draw_frame_double(coordinates_1, frame_index_1, coordinates_2, frame_index_2, similar_points, grade_points)