import numpy as np
import time
import cv2
from matplotlib import pyplot as plt
import os

from PIL import Image


class PreProcessor:
    def __init__(self, kernel_size=9, blend_colors=True, canny_min=100, canny_max=200, crop_area=None):
        #We could initialize some variables based on a single snapshot, fex size, thresholds, etc
        self.morph_kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.canny_min = canny_min
        self.canny_max = canny_max
        self.blend_colors = blend_colors
        self.crop_area = crop_area

    def run(self, img_arr):
        #TODO add cropping before edge detect

        # TODO try this also https://www.learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/
        start = time.time()

        input = img_arr
        if self.crop_area:
            top = self.crop_area[0][0]
            bottom = self.crop_area[0][1]
            left = self.crop_area[1][0]
            right = self.crop_area[1][1]

            input = input[top:bottom, left:right]

        edges = cv2.Canny(input, self.canny_min, self.canny_max)
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, self.morph_kernel)

        ret, mask = cv2.threshold(closed, 10, 255, cv2.THRESH_BINARY)
        if self.blend_colors:
            output = cv2.bitwise_and(input, input, mask=mask)
        else:
            output = mask


        end = time.time()
        print("Elapsed: ", (end - start)*1000, " ms")

        return output

    def update(self):
        pass

    def shutdown(self):
        pass

    def set_crop_area(self, crop_area):
        self.crop_area = crop_area

    # Let's use the same convention as in Keras.Cropping2D
    def crop_area(top_crop, bottom_crop, left_crop, right_crop, width, height):
        return ((top_crop, height - bottom_crop), (left_crop, width - right_crop))

class Tester:

    def __init__(self):
        self.processor = PreProcessor(blend_colors=True)

    def process(self, input_path):
        input_img = Image.open(input_path)
        orig = np.array(input_img)

        width, height = input_img.size
        print("w: ", width, " h:", height)
        crop_area = PreProcessor.crop_area(30, 25, 0, 0, width, height)
        self.processor.set_crop_area(crop_area)

        processed = self.processor.run(orig)
        return orig, processed

    def process_and_save(self, img_path, new_path):

        orig, processed = self.process(img_path)
        saveable = Image.fromarray(np.uint8(processed))
        saveable.save(new_path)

    def process_and_save_batch(self, input_folder, output_folder):
        input_images = self.find_images(input_folder)

        if not os.path.exists(output_folder):
            print("creating folder", output_folder)
            os.makedirs(output_folder)

        for in_img in input_images:
            output_path = os.path.join(output_folder, in_img)
            print(output_path)
            input_full_path = os.path.join(input_folder, in_img)
            self.process_and_save(input_full_path, output_path)

    def find_images(self, input_folder):
        from os import listdir
        from os.path import isfile, join
        onlyfiles = [f for f in listdir(input_folder) if isfile(join(input_folder, f))]
        only_images = list(filter(lambda name: name.lower().endswith(('.jpg', '.jpeg')), onlyfiles))
        only_images.sort()  # TODO sort on file timestamp rather than name.
        print(only_images)
        return only_images

    def process_and_plot(self, img_path):
        orig, processed = self.process(img_path)

        plt.subplot(2, 2, 1), plt.imshow(orig, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(2, 2, 2), plt.imshow(processed, cmap='gray')
        plt.title('Processed Image'), plt.xticks([]), plt.yticks([])

        plt.show()


if __name__ == '__main__':
    print("using opencv: ", cv2.__version__)

    #img_path = '/Users/mpaa/donkey-data/data/simulator/log/3404_cam-image_array_.jpg'
    path = '/Users/mpaa/donkey-data/data/tammerforce-tub-2019-newcar/1114_cam-image_array_.jpg'

    test = Tester()
    #test.process_and_save(path, "./test2.jpg")
    test.process_and_plot(path)
    #test.process_and_save_batch('/Users/mpaa/donkey-data/data/tammerforce-tub-2019-newcar/', '/Users/mpaa/donkey-data/data/tammerforce-processing-test/')