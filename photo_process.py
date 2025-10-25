# 读取/Users/manlingy/Desktop/Person/homepage/ManlingYANG123/assets/img/photo里面所有的图片文件，并且图片文件大小但保留比例和像素之类的，保证加载速度和质量
import os
import cv2
import numpy as np
from PIL import Image
import glob

def compress_image(input_path, output_path, quality=85, max_width=1920, max_height=1080):
    """
    压缩图片，保持比例和质量
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        quality: JPEG质量 (1-100)
        max_width: 最大宽度
        max_height: 最大高度
    """
    try:
        # 使用PIL打开图片
        with Image.open(input_path) as img:
            # 获取原始尺寸
            original_width, original_height = img.size
            
            # 计算缩放比例
            width_ratio = max_width / original_width
            height_ratio = max_height / original_height
            ratio = min(width_ratio, height_ratio, 1.0)  # 不放大图片
            
            # 如果图片已经小于目标尺寸，不进行缩放
            if ratio < 1.0:
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 保存图片
            if img.mode in ('RGBA', 'LA'):
                # 处理透明通道
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存为JPEG格式
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            return True
    except Exception as e:
        print(f"处理图片 {input_path} 时出错: {e}")
        return False

def process_photos():
    """
    处理photo文件夹中的所有图片
    """
    photo_dir = '/Users/manlingy/Desktop/Person/homepage/ManlingYANG123/assets/img/photo'
    
    # 支持的图片格式
    image_extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG', '*.bmp', '*.BMP']
    
    # 统计信息
    total_files = 0
    processed_files = 0
    failed_files = 0
    
    print("开始处理图片...")
    print("=" * 50)
    
    # 遍历digital和film子文件夹
    for subfolder in ['digital', 'film']:
        subfolder_path = os.path.join(photo_dir, subfolder)
        if not os.path.exists(subfolder_path):
            continue
            
        print(f"\n处理 {subfolder} 文件夹:")
        print("-" * 30)
        
        # 获取所有图片文件
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(subfolder_path, ext)))
        
        total_files += len(image_files)
        
        for image_path in image_files:
            filename = os.path.basename(image_path)
            print(f"处理: {filename}")
            
            # 创建备份文件夹
            backup_dir = os.path.join(subfolder_path, 'backup')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # 备份原文件
            backup_path = os.path.join(backup_dir, filename)
            if not os.path.exists(backup_path):
                import shutil
                shutil.copy2(image_path, backup_path)
            
            # 压缩图片
            if compress_image(image_path, image_path, quality=85, max_width=1920, max_height=1080):
                processed_files += 1
                print(f"  ✓ 成功处理")
            else:
                failed_files += 1
                print(f"  ✗ 处理失败")
    
    print("\n" + "=" * 50)
    print("处理完成!")
    print(f"总文件数: {total_files}")
    print(f"成功处理: {processed_files}")
    print(f"处理失败: {failed_files}")
    
    # 显示文件大小统计
    print("\n文件大小统计:")
    print("-" * 30)
    for subfolder in ['digital', 'film']:
        subfolder_path = os.path.join(photo_dir, subfolder)
        if os.path.exists(subfolder_path):
            total_size = 0
            file_count = 0
            for root, dirs, files in os.walk(subfolder_path):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                        file_count += 1
            
            size_mb = total_size / (1024 * 1024)
            print(f"{subfolder}: {file_count} 个文件, {size_mb:.2f} MB")

if __name__ == "__main__":
    process_photos()