from matplotlib import pyplot as plt
import os
import numpy as np
import cv2

from PIL import Image
from donkeycar.parts.preprocessing import PreProcessor


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
    path = '/Users/mpaa/donkey-data/data/tammerforce-tub-2019-newcar/3752_cam-image_array_.jpg'

    test = Tester()
    #test.process_and_save(path, "./test2.jpg")
    test.process_and_plot(path)
    #test.process_and_save_batch('/Users/mpaa/donkey-data/data/tammerforce-newcar-train/', '/Users/mpaa/donkey-data/data/tammerforce-newcar-train-processed/')
