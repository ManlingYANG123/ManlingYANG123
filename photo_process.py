# Compress photos dropped into assets/img/photo/unprocess/{digital,film}
# and copy the results into the live gallery folders.
import os
import shutil
import glob
from PIL import Image, ImageOps

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UNPROCESS_DIR = os.path.join(SCRIPT_DIR, "assets", "img", "photo", "unprocess")
LIVE_DIR = os.path.join(SCRIPT_DIR, "assets", "img", "photo")


def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)
    name = name.replace(" ", "_")
    return name + ext


def compress_image(input_path, output_path, quality=85, max_width=1920, max_height=1080):
    try:
        with Image.open(input_path) as img:
            img = ImageOps.exif_transpose(img)

            original_width, original_height = img.size
            width_ratio = max_width / original_width
            height_ratio = max_height / original_height
            ratio = min(width_ratio, height_ratio, 1.0)

            if ratio < 1.0:
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Bake orientation into pixels and drop EXIF so viewers do not rotate twice
            img.save(output_path, "JPEG", quality=quality, optimize=True)
            return True
    except Exception as e:
        print(f"  error processing {input_path}: {e}")
        return False


def process_photos():
    image_extensions = ["*.jpg", "*.jpeg", "*.JPG", "*.JPEG", "*.png", "*.PNG", "*.bmp", "*.BMP"]
    total_files = 0
    processed_files = 0
    failed_files = 0
    copied = []

    print("Processing photos from unprocess/")
    print("=" * 50)

    for subfolder in ["digital", "film"]:
        source_dir = os.path.join(UNPROCESS_DIR, subfolder)
        dest_dir = os.path.join(LIVE_DIR, subfolder)
        if not os.path.isdir(source_dir):
            continue

        os.makedirs(dest_dir, exist_ok=True)
        backup_dir = os.path.join(source_dir, "backup")
        os.makedirs(backup_dir, exist_ok=True)

        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(source_dir, ext)))
        image_files.sort()

        if not image_files:
            print(f"\n{subfolder}: no new files")
            continue

        print(f"\n{subfolder}:")
        print("-" * 30)
        total_files += len(image_files)

        for image_path in image_files:
            filename = os.path.basename(image_path)
            live_name = sanitize_filename(filename)
            backup_path = os.path.join(backup_dir, filename)
            dest_path = os.path.join(dest_dir, live_name)

            print(f"  {filename} -> {live_name}")

            if not os.path.exists(backup_path):
                shutil.copy2(image_path, backup_path)

            if compress_image(image_path, dest_path):
                processed_files += 1
                src_mb = os.path.getsize(image_path) / (1024 * 1024)
                dst_mb = os.path.getsize(dest_path) / (1024 * 1024)
                print(f"    ok  {src_mb:.1f} MB -> {dst_mb:.1f} MB")
                copied.append((subfolder, live_name))
                os.remove(image_path)
            else:
                failed_files += 1
                print("    failed")

    print("\n" + "=" * 50)
    print(f"done. {processed_files}/{total_files} processed, {failed_files} failed")
    if copied:
        print("\nlive files:")
        for subfolder, name in copied:
            print(f"  /assets/img/photo/{subfolder}/{name}")


if __name__ == "__main__":
    process_photos()
