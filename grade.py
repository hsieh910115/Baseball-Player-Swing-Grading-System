import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.font_manager import FontProperties
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

def get_shoulder_rotation(frame_coordinates): #加入一個從右肩(14)畫出的水平yz平面的線的點來判斷髖轉正的角度
    A = frame_coordinates[11] 
    B = frame_coordinates[14] 
    C = (frame_coordinates[14][0], frame_coordinates[11][1], frame_coordinates[11][2])
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
    #print("theta right shoulder : ", theta_right_shoulder)
    theta_list.append(theta_right_shoulder)

    theta_right_elbow = get_theta(14, 15, 16, frame_coordinates) # right shoulder, right elbow, right wrist
    #print("theta right elbow : ", theta_right_elbow)
    theta_list.append(theta_right_elbow)

    theta_left_shoulder = get_theta(8, 11, 12, frame_coordinates) # thorax, left shoulder, left elbow
    #print("theta left shoulder : ", theta_left_shoulder)
    theta_list.append(theta_left_shoulder)

    theta_left_elbow = get_theta(11, 12, 13, frame_coordinates) # left shoulder, left elbow, left wrist
    #print("theta left elbow : ", theta_left_elbow)
    theta_list.append(theta_left_elbow)

    theta_right_hip = get_theta(14, 1, 2, frame_coordinates) # right shoulder, right hip, right knee
    #print("theta right hip : ", theta_right_hip)
    theta_list.append(theta_right_hip)

    theta_left_hip = get_theta(11, 4, 5, frame_coordinates) # left shoulder, left hip, left knee
    #print("theta left hip : ", theta_left_hip)
    theta_list.append(theta_left_hip)

    theta_right_knee = get_theta(1, 2, 3, frame_coordinates) # right hip, right knee, right foot
    #print("theta right knee : ", theta_right_knee)
    theta_list.append(theta_right_knee)

    theta_left_knee = get_theta(4, 5, 6, frame_coordinates) # left hip, left knee, left foot
    #print("theta left knee : ", theta_left_knee)
    theta_list.append(theta_left_knee)

    theta_hip_rotation = get_hip_rotation(frame_coordinates)
    #print("theta hip rotation : ", theta_hip_rotation)
    theta_list.append(theta_hip_rotation)

    theta_shoulder_rotation = get_shoulder_rotation(frame_coordinates)
    #print("theta shoulder rotation : ", theta_shoulder_rotation)
    theta_list.append(theta_shoulder_rotation)

    theta_body_side = get_body_side_angle(frame_coordinates)
    #print("theta body side angle : ", theta_body_side)
    theta_list.append(theta_body_side)

    theta_body_lean = get_body_lean_angle(frame_coordinates)
    #print("theta body lean angle : ", theta_body_lean)
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

def draw_frame_double(coordinates1, frame_index1, coordinates2, frame_index2, grade_point, for_comments, standard, position):
    #處理第一個骨架的輔助點
    x1 = list(coordinates1[frame_index1, :, 0])
    y1 = list(coordinates1[frame_index1, :, 2])
    z1 = list(-coordinates1[frame_index1, :, 1])
    #加入一個從右髖(1)畫出的水平yz平面的線的點(17)來判斷髖轉正的角度
    x1.append(coordinates1[frame_index1][1][0])  # x of right hip(1), y and z of left hip(4)
    y1.append(coordinates1[frame_index1][4][2])
    z1.append(-coordinates1[frame_index1][4][1])
    #加入一個從右肩(14)畫出的水平yz平面的線的點(18)來判斷髖轉正的角度
    x1.append(coordinates1[frame_index1][14][0])  # x of right shoulder(14), y and z of left shoulder(11)
    y1.append(coordinates1[frame_index1][11][2])
    z1.append(-coordinates1[frame_index1][11][1])
    #加入一個從中髖(0)畫出的水平xz平面的線的點(19)來判斷身體向本壘倒的角度
    x1.append(coordinates1[frame_index1][8][0])  # y of hip(0), x and z of thorax
    y1.append(coordinates1[frame_index1][0][2])
    z1.append(-coordinates1[frame_index1][8][1])
    #加入一個從中髖(0)畫出的水平yz平面的線的點(20)來判斷身體前後倒的角度
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
    #加入一個從右肩(14)畫出的水平yz平面的線的點(18)來判斷髖轉正的角度
    x2.append(coordinates2[frame_index2][14][0])  # x of right shoulder(14), y and z of left shoulder(11)
    y2.append(coordinates2[frame_index2][11][2])
    z2.append(-coordinates2[frame_index2][11][1])
    #加入一個從中髖(0)畫出的水平xz平面的線的點(19)來判斷身體向本壘倒的角度
    x2.append(coordinates2[frame_index2][8][0])  # y of hip(0), x and z of thorax
    y2.append(coordinates2[frame_index2][0][2])
    z2.append(-coordinates2[frame_index2][8][1])
    #加入一個從中髖(0)畫出的水平yz平面的線的點(20)來判斷身體前後倒的角度
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
        (1, 17), (14, 18),               # hip rotation and shoulder rotation 輔助 line
        (0, 19), (0,20)                  # body angle 輔助 line     
    ]

    # 定義關節點的顏色(身體關節點黑色，輔助點金色)
    colors = [
        'black', 'black', 'black', 'black', 'black', 
        'black', 'black', 'black', 'black', 'black', 
        'black', 'black', 'black', 'black', 'black', 
        'black', 'black', 'gold', 'gold', 'gold', 'gold'
    ]

    # 創建 3D 圖形，包含兩個子圖
    fig = plt.figure(figsize=(14.5, 7.3))
    # 使用 GridSpec 調整佈局
    gs = GridSpec(3, 2, figure=fig)
    #第一個子圖
    ax1 = fig.add_subplot(gs[0:2, 0], projection='3d')
    ax1.set_title("STANDARD")
    # 設置坐標軸範圍
    ax1.set_xlim([-0.5, 0.5])
    ax1.set_ylim([-0.5, 0.5])
    ax1.set_zlim([-0.5, 0.5])
    # 設置坐標軸名稱
    ax1.set_xlabel('X axis')
    ax1.set_ylabel('Y axis')
    ax1.set_zlabel('Z axis')
    # 調整 X、Y、Z 的比例
    ax1.set_box_aspect([1, 1, 1])  
    # 繪製散點圖
    ax1.scatter(x1, y1, z1, c=colors, marker='o')
    #繪製骨架連接
    for joint1, joint2 in skeleton:
        ax1.plot([x1[joint1], x1[joint2]], [y1[joint1], y1[joint2]], [z1[joint1], z1[joint2]], c='b')

    #第二個子圖
    ax2 = fig.add_subplot(gs[0:2, 1], projection='3d')
    ax2.set_title("YOU")
    # 設置坐標軸範圍
    ax2.set_xlim([-0.5, 0.5])
    ax2.set_ylim([-0.5, 0.5])
    ax2.set_zlim([-0.5, 0.5])
    # 設置坐標軸名稱
    ax2.set_xlabel('X axis')
    ax2.set_ylabel('Y axis')
    ax2.set_zlabel('Z axis')
    # 調整 X、Y、Z 的比例
    ax2.set_box_aspect([1, 1, 1])  
    # 繪製散點圖
    ax2.scatter(x2, y2, z2, c=colors, marker='o')
    #繪製骨架連接
    for joint1, joint2 in skeleton:
        ax2.plot([x2[joint1], x2[joint2]], [y2[joint1], y2[joint2]], [z2[joint1], z2[joint2]], c='b')


    #骨架偵數
    frame_num = frame_index1 + 1
    fig.text(0.38, 0.85, f"frame : {frame_num}", fontsize=12, color='black')
    frame_num = frame_index2 + 1
    fig.text(0.82, 0.85, f"frame : {frame_num}", fontsize=12, color='black')
    # 標題
    if standard == 1: fig.suptitle(f"Swing Comparison: Your Swing vs. Shohei Ohtani at position {position}", fontsize=16)
    if standard == 2: fig.suptitle(f"Swing Comparison: Your Swing vs. Aaron Judge at position {position}", fontsize=16)
    
    # 相似度
    #fig.text(0.379, 0.35, f"Similarity : {similarity_point:.3f}", fontsize=16, color='black')
    # 使用字型屬性
    font = FontProperties(fname='/Users/zongyan/Desktop/EAI/finalproject/123.ttc', size=16)
    # 成績
    if grade_point >= 90:
        fig.text(0.405, 0.35, f"Grade : {grade_point:.3f}", fontsize=16, color='green')
        fig.text(0.385, 0.31, "Why not consider joining the professional baseball draft?", fontsize=16, color='green')
    elif grade_point >= 75:
        fig.text(0.405, 0.35, f"Grade : {grade_point:.3f}", fontsize=10, color='black')
        fig.text(0.385, 0.31, "I think there’s still room for improvement.", fontsize=10, color='black')
    elif grade_point >= 60:
        fig.text(0.405, 0.35, f"Grade : {grade_point:.3f}", fontsize=16, color='orange')
        fig.text(0.385, 0.31, "It doesn’t seem to be that great.", fontsize=16, color='orange')
    else:
        fig.text(0.405, 0.35, f"Grade : {grade_point:.3f}", fontsize=16, color='red')
        fig.text(0.385, 0.31, "You might not be suited for playing baseball…", fontsize=16, color='red')                               
    # 評語區
    text_ax = fig.add_subplot(gs[2, :])
    text_ax.axis('off')
    #        x從左開始,y從下開始
    # 評語區
    text_ax.text(0.0, 0.9, "Comment", fontsize=16)
    # 右肩、右肘、左肩、左肘、右髖、左髖、右膝、左膝、髖旋轉、肩旋轉、側傾角度、後仰角度
    # 右肩
    if for_comments[0]["delta_theta"] > 0: text_ax.text(0.0, 0.75, f"right shoulder : {for_comments[0]['comment']}  ==>  {for_comments[0]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[0]['color'])
    elif for_comments[0]["delta_theta"] == 0: text_ax.text(0.0, 0.75, f"right shoulder : Perfect.", color = 'green') 
    else: text_ax.text(0.0, 0.75, f"right shoulder : {for_comments[0]['comment']}  ==>  {-for_comments[0]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[0]['color'])
    # 右肘
    if for_comments[1]["delta_theta"] > 0: text_ax.text(0.0, 0.75 - 0.14, f"right elbow     : {for_comments[1]['comment']}  ==>  {for_comments[1]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[1]['color'])
    elif for_comments[1]["delta_theta"] == 0: text_ax.text(0.0, 0.75 - 0.14, f"right elbow     : Perfect.", color = 'green') 
    else: text_ax.text(0.0, 0.75 - 0.14, f"right elbow     : {for_comments[1]['comment']}  ==>  {-for_comments[1]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[1]['color'])
    # 左肩
    if for_comments[2]["delta_theta"] > 0: text_ax.text(0.0, 0.75 - 0.14 * 2, f"left shoulder   : {for_comments[2]['comment']}  ==>  {for_comments[2]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[2]['color'])
    elif for_comments[2]["delta_theta"] == 0: text_ax.text(0.0, 0.75 - 0.14 * 2, f"left shoulder   : Perfect.", color = 'green') 
    else: text_ax.text(0.0, 0.75 - 0.14 * 2, f"left shoulder   : {for_comments[2]['comment']}  ==>  {-for_comments[2]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[2]['color'])
    # 左肘
    if for_comments[3]["delta_theta"] > 0: text_ax.text(0.0, 0.75 - 0.14 * 3, f"left elbow       : {for_comments[3]['comment']}  ==>  {for_comments[3]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[3]['color'])
    elif for_comments[3]["delta_theta"] == 0: text_ax.text(0.0, 0.75 - 0.14 * 3, f"left elbow       : Perfect.", color = 'green') 
    else: text_ax.text(0.0, 0.75 - 0.14 * 3, f"left elbow       : {for_comments[3]['comment']}  ==>  {-for_comments[3]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[3]['color'])
    # 右髖
    if for_comments[4]["delta_theta"] > 0: text_ax.text(0.0, 0.75 - 0.14 * 4, f"right hip         : {for_comments[4]['comment']}  ==>  {for_comments[4]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[4]['color'])
    elif for_comments[4]["delta_theta"] == 0: text_ax.text(0.0, 0.75 - 0.14 * 4, f"right hip         : Perfect.", color = 'green') 
    else: text_ax.text(0.0, 0.75 - 0.14 * 4, f"right hip         : {for_comments[4]['comment']}  ==>  {-for_comments[4]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[4]['color'])
    # 左髖
    if for_comments[5]["delta_theta"] > 0: text_ax.text(0.0, 0.75 - 0.14 * 5, f"left hip           : {for_comments[5]['comment']}  ==>  {for_comments[5]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[5]['color'])
    elif for_comments[5]["delta_theta"] == 0: text_ax.text(0.0, 0.75 - 0.14 * 5, f"left hip           : Perfect.", color = 'green') 
    else: text_ax.text(0.0, 0.75 - 0.14 * 5, f"left hip           : {for_comments[5]['comment']}  ==>  {-for_comments[5]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[5]['color'])
    # 右膝
    if for_comments[6]["delta_theta"] > 0: text_ax.text(0.56, 0.75, f"right knee            : {for_comments[6]['comment']}  ==>  {for_comments[6]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[6]['color'])
    elif for_comments[6]["delta_theta"] == 0: text_ax.text(0.56, 0.75, f"right knee            : Perfect.", color = 'green') 
    else: text_ax.text(0.56, 0.75, f"right knee            : {for_comments[6]['comment']}  ==>  {-for_comments[6]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[6]['color'])
    # 左膝
    if for_comments[7]["delta_theta"] > 0: text_ax.text(0.56, 0.75 - 0.14, f"left knee              : {for_comments[7]['comment']}  ==>  {for_comments[7]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[7]['color'])
    elif for_comments[7]["delta_theta"] == 0: text_ax.text(0.56, 0.75 - 0.14, f"left knee              : Perfect.", color = 'green') 
    else: text_ax.text(0.56, 0.75 - 0.14, f"left knee              : {for_comments[7]['comment']}  ==>  {-for_comments[7]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[7]['color'])
    # 髖旋轉
    if for_comments[8]["delta_theta"] > 0: text_ax.text(0.56, 0.75 - 0.14 * 2, f"hip rotation          : {for_comments[8]['comment']}  ==>  {for_comments[8]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[8]['color'])
    elif for_comments[8]["delta_theta"] == 0: text_ax.text(0.56, 0.75 - 0.14 * 2, f"hip rotation          : Perfect.", color = 'green') 
    else: text_ax.text(0.56, 0.75 - 0.14 * 2, f"hip rotation          : {for_comments[8]['comment']}  ==>  {-for_comments[8]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[8]['color'])
    # 肩旋轉
    if for_comments[9]["delta_theta"] > 0: text_ax.text(0.56, 0.75 - 0.14 * 3, f"shoulder rotation : {for_comments[9]['comment']}  ==>  {for_comments[9]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[9]['color'])
    elif for_comments[9]["delta_theta"] == 0: text_ax.text(0.56, 0.75 - 0.14 * 3, f"shoulder rotation : Perfect.", color = 'green') 
    else: text_ax.text(0.56, 0.75 - 0.14 * 3, f"shoulder rotation : {for_comments[9]['comment']}  ==>  {-for_comments[9]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[9]['color'])
    # 側傾角度
    if for_comments[10]["delta_theta"] > 0: text_ax.text(0.56, 0.75 - 0.14 * 4, f"body side angle   : {for_comments[10]['comment']}  ==>  {for_comments[10]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[10]['color'])
    elif for_comments[10]["delta_theta"] == 0: text_ax.text(0.56, 0.75 - 0.14 * 4, f"body side angle   : Perfect.", color = 'green') 
    else: text_ax.text(0.56, 0.75 - 0.14 * 4, f"body side angle   : {for_comments[10]['comment']}  ==>  {-for_comments[10]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[10]['color'])
    # 後仰角度
    if for_comments[11]["delta_theta"] > 0: text_ax.text(0.56, 0.75 - 0.14 * 5, f"body lean angle   : {for_comments[11]['comment']}  ==>  {for_comments[11]['delta_theta']:.1f} degree smaller than Standard.", fontsize=13, color = for_comments[11]['color'])
    elif for_comments[11]["delta_theta"] == 0: text_ax.text(0.56, 0.75 - 0.14 * 5, f"body lean angle   : Perfect.", color = 'green') 
    else: text_ax.text(0.56, 0.75 - 0.14 * 5, f"body lean angle   : {for_comments[11]['comment']}  ==>  {-for_comments[11]['delta_theta']:.1f} degree bigger than Standard.", fontsize=13, color = for_comments[11]['color'])
    
    plt.tight_layout()
    plt.show()

def grade(thetas_1, thetas_2):
    similarity = 0            # 相似度評分
    similarities = []         # 存所有角度的評分
    final_similarity = 0      # 所有角度平均的相似值
    grade = 0                 # 最終評分
    total_weight = 0          # 總共權重數
    for_comments = []           # [word, delta_theta], 給draw_frame_double寫評語用
    for i, (theta_1, theta_2) in enumerate(zip(thetas_1, thetas_2)):
        #假設差距範圍是0~90度，分數為0~100分，90 / 100 = 0.9度，差0.9度扣一分
        delta_theta = np.abs(theta_1 - theta_2) # 計算相似度要絕對值
        similarity = 100 * np.exp(-(delta_theta / 20) ** 2)
        similarities.append(similarity)
        delta_theta = theta_1 - theta_2         # 要放入評語中，必須看誰比較高或低，不用絕對值
        if i < 4: # 上半身，角度容易較大，給定較寬鬆的標準
            if similarity > 92 : for_comments.append({"comment": "VERY GOOD ", "delta_theta": delta_theta, "color": 'green'})
            elif similarity > 82 : for_comments.append({"comment": "GOOD          ", "delta_theta": delta_theta, "color": 'black'})
            elif similarity > 72 : for_comments.append({"comment": "OK               ", "delta_theta": delta_theta, "color": 'black'})
            elif similarity > 60 : for_comments.append({"comment": "NOT GOOD  ", "delta_theta": delta_theta, "color": 'orange'})
            else: for_comments.append({"comment": "BAD             ", "delta_theta": delta_theta, "color": 'red'})
        else:     # 下半身以及旋轉，角度通常較小，給定較嚴格的標準
            if similarity > 95 : for_comments.append({"comment": "VERY GOOD ", "delta_theta": delta_theta, "color": 'green'})
            if similarity > 90 : for_comments.append({"comment": "GOOD          ", "delta_theta": delta_theta, "color": 'black'})
            elif similarity > 85 : for_comments.append({"comment": "OK               ", "delta_theta": delta_theta, "color": 'black'})
            elif similarity > 75 : for_comments.append({"comment": "NOT GOOD  ", "delta_theta": delta_theta, "color": 'orange'})
            else: for_comments.append({"comment": "BAD             ", "delta_theta": delta_theta, "color": 'red'})
    final_similarity = np.sum(similarities) / len(similarities) 
    print("similarities : ", similarities)
    #11個分數給11個權重:右肩、右肘、左肩、左肘、右髖、左髖、右膝、左膝、髖旋轉、肩旋轉、側傾角度、後仰角度
    weights = [         6,   10,   6,   10,   3,   3,    6,   6,    7,      7,      8,       8] 
    for i in range(len(weights)):
        grade_weight = similarities[i] * weights[i]
        #print("grades[i] : ", grades[i], ",  weights[i] : ", weights[i])
        grade += grade_weight
        total_weight += weights[i]
    #print("total weight : ", total_weight)
    grade = grade / total_weight
    return final_similarity, grade, for_comments
    
    
#######################################主程式##############################################
# 加載保存的 3D 坐標
# 能用檔案:                                                                                                                                                                                                                                                                                                                                                                                                                                           
# ohtani_1 : 90, ohtani_2 : 159, ohtani_3 : 257, ohtani_4 : 127, ohtani_5 : 251, ohtani_6 : 189, ohtani_7 : 135, ohtani_8 : 256, ohtani_9 : 149
# judge_1 : 139, judge_2 : 340, judge_3 : 76, judge_4 : 272, judge_5 : 116, judge_6 : 290, judge_7 : 80, judge_8 : 53, judge_9 : 35
while True:
    standard = int(input("請輸入你想要做為標準的骨架(1:大谷Shohei Ohtani、2:法官Aaron Judge) : "))
    if standard == 1 or standard == 2: break        
    else: print("請輸入正確的值")
while True:
    position = int(input("請輸入你想要比較的九宮格位置(以捕手視角左上為1、上為2、右上為3、左為4、中為5、右為6、左下為7、下為8、右下為9) : "))
    if position >= 1 and position <= 9: break        
    else: print("請輸入正確的值")
if standard == 1:
    if position == 1: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\ohtani_1.npy")
        frame_num_1 = 90
    elif position == 2: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\ohtani_2.npy")
        frame_num_1 = 159
    elif position == 3: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\ohtani_3.npy")
        frame_num_1 = 257
    elif position == 4: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\ohtani_4.npy")
        frame_num_1 = 127
    elif position == 5: 
        coordinates_1 = np.load('/Users/zongyan/Desktop/EAI/finalproject/standard/ohtani_5.npy')
        frame_num_1 = 251
    elif position == 6: 
        coordinates_1 = np.load('/Users/zongyan/Desktop/EAI/finalproject/standard/ohtani_6.npy')
        frame_num_1 = 189
    elif position == 7: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\ohtani_7.npy")
        frame_num_1 = 135
    elif position == 8: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\ohtani_8.npy")
        frame_num_1 = 256
    elif position == 9: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\ohtani_9.npy")
        frame_num_1 = 149
elif standard == 2:
    if position == 1: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\judge_1.npy")
        frame_num_1 = 139
    elif position == 2: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\judge_2.npy")
        frame_num_1 = 340
    elif position == 3: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\judge_3.npy")
        frame_num_1 = 76
    elif position == 4: 
        coordinates_1 = np.load('/Users/zongyan/Desktop/EAI/finalproject/standard/judge_4.npy')
        frame_num_1 = 272
    elif position == 5: 
        coordinates_1 = np.load('/Users/zongyan/Desktop/EAI/finalproject/standard/judge_5.npy')
        frame_num_1 = 116
    elif position == 6: 
        coordinates_1 = np.load('/Users/zongyan/Desktop/EAI/finalproject/standard/judge_6.npy')
        frame_num_1 = 290
    elif position == 7: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\judge_7.npy")
        frame_num_1 = 80
    elif position == 8: 
        coordinates_1 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\judge_8.npy")
        frame_num_1 = 53
    elif position == 9: 
        coordinates_1 = np.load('/Users/zongyan/Desktop/EAI/finalproject/standard/judge_9.npy')
        frame_num_1 = 35
print("coordinates_1 shape", coordinates_1.shape)
# 获取某帧的3D坐标
frame_index_1 = frame_num_1 - 1   # 實際偵數的index
frame_coordinates_1 = coordinates_1[frame_index_1]
thetas_1 = calculate_angle(frame_coordinates_1)
#print("theta_1 ", thetas_1)

# tsai_1 : 212, tsai_2 : 253, tsai_3 : 226, tsai_4 : 189, tsai_5 : 181, tsai_6 : 142, tsai_7 : 129, tsai_8 : 119, tsai_9 : 212
if position == 1: 
    coordinates_2 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\tsai_1.npy")
    frame_num_2 = 212
elif position == 2: 
    coordinates_2 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\tsai_2.npy")
    frame_num_2 = 253
elif position == 3: 
    coordinates_2 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\tsai_3.npy")
    frame_num_2 = 226
elif position == 4: 
    coordinates_2 = np.load('/Users/zongyan/Desktop/EAI/finalproject/willy.npy')
    frame_num_2 = 50
elif position == 5: 
    coordinates_2 = np.load('/Users/zongyan/Desktop/EAI/finalproject/willy.npy')
    frame_num_2 = 47
elif position == 6: 
    coordinates_2 = np.load('/Users/zongyan/Desktop/EAI/finalproject/willy.npy')
    frame_num_2 = 50
elif position == 7: 
    coordinates_2 = np.load('/Users/zongyan/Desktop/EAI/finalproject/willy.npy')
    frame_num_2 = 48
elif position == 8: 
    coordinates_2 = np.load('/Users/zongyan/Desktop/EAI/finalproject/willy.npy')
    frame_num_2 = 48
elif position == 9: 
    coordinates_2 = np.load('/Users/zongyan/Desktop/EAI/finalproject/willy.npy')
    frame_num_2 = 48
#coordinates_2 = np.load(r"C:\NCKU\113_1\EAI\correct_3d_coordinate\judge_5.npy") 
print("coordinates_2 shape", coordinates_2.shape)
# 获取某帧的3D坐标
#frame_num_2 = 116  # 實際偵數
frame_index_2 = frame_num_2 - 1   # 實際偵數的index
frame_coordinates_2 = coordinates_2[frame_index_2]
thetas_2 = calculate_angle(frame_coordinates_2)
#print("theta_2 ", thetas_2)

similar_point, grade_point, comments = grade(thetas_1, thetas_2)
print("similar point : ", similar_point)
print("grade point : ", grade_point)

draw_frame_double(coordinates_1, frame_index_1, coordinates_2, frame_index_2, grade_point, comments, standard, position)