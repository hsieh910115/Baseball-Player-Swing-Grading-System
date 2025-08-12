import numpy as np

# 讀取 .npz 檔案
data = np.load('/Users/zongyan/Desktop/EAI/finalproject/VideoPose3D/data/detectron2output/video.mp4.npz', allow_pickle=True)

# 查看第一幀的內容
first_frame_boxes = data['boxes'][0]  # 第一幀的邊界框
first_frame_keypoints = data['keypoints'][0]  # 第一幀的關鍵點
first_frame_segments = data['segments'][0]  # 第一幀的分割（如果有）

# 打印第一幀的結果
print("First Frame Boxes:", first_frame_boxes)
print("First Frame Keypoints:", first_frame_keypoints)
print("First Frame Segments:", first_frame_segments)

# 查看影片的元數據
metadata = data['metadata'].item()  # 將 dict 解壓為普通 Python 字典
print("Metadata:", metadata)