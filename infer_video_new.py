import detectron2
from detectron2.utils.logger import setup_logger
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor

import subprocess as sp
import numpy as np
import time
import argparse
import sys
import os
import glob
import torch

def parse_args():
    parser = argparse.ArgumentParser(description='End-to-end inference')
    parser.add_argument(
        '--cfg',
        dest='cfg',
        help='cfg model file (/path/to/model_config.yaml)',
        default=None,
        type=str
    )
    parser.add_argument(
        '--output-dir',
        dest='output_dir',
        help='directory for visualization pdfs (default: /tmp/infer_simple)',
        default='/tmp/infer_simple',
        type=str
    )
    parser.add_argument(
        '--image-ext',
        dest='image_ext',
        help='image file name extension (default: mp4)',
        default='mp4',
        type=str
    )
    parser.add_argument(
        'im_or_folder', help='image or folder of images', default=None
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

def get_resolution(filename):
    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
               '-show_entries', 'stream=width,height', '-of', 'csv=p=0', filename]
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=-1)
    for line in pipe.stdout:
        w, h = line.decode().strip().split(',')
        return int(w), int(h)

def read_video(filename):
    w, h = get_resolution(filename)

    command = ['ffmpeg',
            '-i', filename,
            '-f', 'image2pipe',
            '-pix_fmt', 'bgr24',
            '-vsync', '0',
            '-vcodec', 'rawvideo', '-']

    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=-1)
    while True:
        data = pipe.stdout.read(w*h*3)
        if not data:
            break
        yield np.frombuffer(data, dtype='uint8').reshape((h, w, 3))

def get_best_person(bbox_tensor, kps, scores):
    """選擇最佳的人物檢測結果"""
    if len(scores) == 0:
        return None, None
    
    # 使用分數選擇最佳檢測結果
    best_idx = np.argmax(scores)
    best_bbox = bbox_tensor[best_idx:best_idx+1]  # 保持2D形狀
    best_kps = kps[best_idx:best_idx+1]  # 保持3D形狀
    
    return best_bbox, best_kps

def create_empty_detection():
    """創建空的檢測結果，保持與真實檢測相同的形狀"""
    empty_bbox = np.zeros((1, 5))  # x1, y1, x2, y2, score
    empty_kps = np.zeros((1, 17, 3))  # 17個關鍵點，每個點有x, y, score
    return empty_bbox, empty_kps

def main(args):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(args.cfg))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(args.cfg)
    # 動態設定設備
    if torch.cuda.is_available():
        cfg.MODEL.DEVICE = "cuda"
        print("Using CUDA")
    else:
        cfg.MODEL.DEVICE = "cpu"
        print("Using CPU")
    
    predictor = DefaultPredictor(cfg)
    predictor = DefaultPredictor(cfg)

    if os.path.isdir(args.im_or_folder):
        im_list = glob.iglob(args.im_or_folder + '/*.' + args.image_ext)
    else:
        im_list = [args.im_or_folder]

    for video_name in im_list:
        out_name = os.path.join(args.output_dir, os.path.basename(video_name))
        print('Processing {}'.format(video_name))

        boxes = []
        segments = []
        keypoints = []

        for frame_i, im in enumerate(read_video(video_name)):
            t = time.time()
            outputs = predictor(im)['instances'].to('cpu')
            print('Frame {} processed in {:.3f}s'.format(frame_i, time.time() - t))

            # 獲取檢測結果
            if outputs.has('pred_boxes') and len(outputs.pred_boxes) > 0:
                bbox_tensor = outputs.pred_boxes.tensor.numpy()
                scores = outputs.scores.numpy()
                kps = outputs.pred_keypoints.numpy()
                
                # 選擇最佳檢測結果
                bbox_tensor, kps = get_best_person(bbox_tensor, kps, scores)
                
                if bbox_tensor is not None:
                    # 添加分數到bbox
                    score = scores[np.argmax(scores)].reshape(1, 1)
                    bbox_tensor = np.concatenate((bbox_tensor, score), axis=1)
                    
                    # 處理關鍵點格式
                    kps_xy = kps[:, :, :2]
                    kps_prob = kps[:, :, 2:3]
                    kps_logit = np.zeros_like(kps_prob)  # Dummy
                    kps = np.concatenate((kps_xy, kps_logit, kps_prob), axis=2)
                    kps = kps.transpose(0, 2, 1)
                else:
                    bbox_tensor, kps = create_empty_detection()
                    kps = kps.transpose(0, 2, 1)
            else:
                bbox_tensor, kps = create_empty_detection()
                kps = kps.transpose(0, 2, 1)

            # Mimic Detectron1 format
            cls_boxes = [[], bbox_tensor]
            cls_keyps = [[], kps]
            
            boxes.append(cls_boxes)
            segments.append(None)
            keypoints.append(cls_keyps)

        # Video resolution
        metadata = {
            'w': im.shape[1],
            'h': im.shape[0],
        }
        
        # 確保所有array具有一致的形狀
        boxes = np.array(boxes, dtype=object)
        keypoints = np.array(keypoints, dtype=object)
        segments = np.array(segments, dtype=object)
        
        np.savez_compressed(out_name, boxes=boxes, segments=segments, keypoints=keypoints, metadata=metadata)

if __name__ == '__main__':
    setup_logger()
    args = parse_args()
    main(args)
