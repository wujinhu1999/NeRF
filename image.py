import argparse
import cv2
import matplotlib.pyplot as plt
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Batch process images using template matching.")
    parser.add_argument("--template", default="./process/template/template.jpg", help="Path to the template image.")
    parser.add_argument("--image_dir", default="./process/input", help="Directory containing images to be processed.")
    parser.add_argument("--output_dir", default="./process/output", help="Directory to save cropped images.")
    return parser.parse_args()

def main():
    args = parse_args()

    # 读取模板图片
    template = cv2.imread(args.template, 0)
    w, h = template.shape[::-1]

    # 确保输出目录存在
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # 获取所有图片路径
    image_paths = [os.path.join(args.image_dir, img) for img in os.listdir(args.image_dir) if img.endswith(('.jpg', '.png'))]

    # 遍历并处理所有图片
    for image_path in image_paths:
        # 读取原始图片
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 使用模板匹配
        result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 获取匹配区域的坐标
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # 裁剪出匹配区域
        roi = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # 在原始图片上画出匹配区域（可选）
        # cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)

        # 显示结果（可选）
        # plt.figure(figsize=(10, 5))
        # plt.subplot(1, 2, 1)
        # plt.title("Original Image with Matched Region")
        # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # plt.axis('off')
        #
        # plt.subplot(1, 2, 2)
        # plt.title("Cropped Image")
        # plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        # plt.axis('off')
        #
        # plt.show()

        # 保存裁剪后的图片
        filename = os.path.basename(image_path)
        cv2.imwrite(os.path.join(args.output_dir, filename), roi)

if __name__ == "__main__":
    main()
