# ⚾ Swing Analysis with VideoPose3D

This project evaluates baseball swing mechanics by comparing your swing against professional standards from **Aaron Judge** and **Shohei Ohtani**.  
You can select a swing position (**1–9**) to compare parameters such as **body angle, rotation, and joint alignment**. The system outputs both a **numerical score** and **short comments** for feedback.



## 🔹 Workflow

1. **Prepare your swing video**  
   - Save as `input.mp4`  

2. **Run VideoPose3D.ipynb**  
   - This will create three folders:  
     - `detectron2`  
     - `VideoPose3D`  
     - `videos`  
   - It will also generate `output.mp4` with 3D pose reconstruction.  

3. **Run grade.py**  
   - Produces `grade.png` containing:  
     - Comparison plots (your swing vs. Judge/Ohtani)  
     - Score and comments for each joint angle  


## 🔹 Demo

### 🎥 Swing Input & Reconstruction
![IMG_6936](https://github.com/user-attachments/assets/a2737e2f-93c9-47e2-a118-f7d8242dbaf3)

https://github.com/user-attachments/assets/a3d4776b-6838-4a94-9bb8-7b769d970e6d  



### 📊 Swing Comparison & Score
<img width="800" alt="grade" src="https://github.com/user-attachments/assets/25cddb55-67dc-4dbb-b76f-7c7a9535fadd" />

**Example Result:**  
- **Score:** 70.9 / 100  
- **Feedback:** Shoulder rotation slightly off, body lean angle needs improvement.  



## 🔹 Key Features
- ✅ Compare your swing with MLB standards (Aaron Judge & Shohei Ohtani)  
- ✅ 3D reconstruction using **VideoPose3D**  
- ✅ Automatic scoring and feedback comments  
- ✅ Visual comparison plots for detailed analysis  



