import numpy as np
import time
import cv2
#from matplotlib import pyplot as plt

from PIL import Image


class PreProcessor:
    def __init__(self, kernel_size=9, blend_colors=True, canny_min=100, canny_max=200):
        #We could initialize some variables based on a single snapshot, fex size, thresholds, etc
        self.morph_kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.canny_min = canny_min
        self.canny_max = canny_max
        self.blend_colors = blend_colors

    def run(self, img_arr):
        #TODO add cropping before edge detect

        # TODO try this also https://www.learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/
        start = time.time()

        edges = cv2.Canny(img_arr, self.canny_min, self.canny_max)
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, self.morph_kernel)

        ret, mask = cv2.threshold(closed, 10, 255, cv2.THRESH_BINARY)
        if self.blend_colors:
            output = cv2.bitwise_and(img_arr, img_arr, mask=mask)
        else:
            output = mask

        end = time.time()
        print("Elapsed: ", (end - start)*1000, " ms")

        return output

    def update(self):
        pass

    def shutdown(self):
        pass


class Tester:

    def __init__(self):
        self.processor = PreProcessor(blend_colors=True)

    def process_and_save(self, img_path, new_path):
        # load objects that were saved as separate files
        img = Image.open(img_path)
        width, height = img.size
        print("w: ", width, " h:", height)
        arr = np.array(img)
        processed = self.processor.run(arr)
        saveable = Image.fromarray(np.uint8(processed))
        saveable.save(new_path)

    '''
    def process_and_plot(self, img_path):
        img = Image.open(img_path)
        arr = np.array(img)
        processed = self.processor.run(arr)

        plt.subplot(2, 2, 1), plt.imshow(arr, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(2, 2, 2), plt.imshow(processed, cmap='gray')
        plt.title('Processed Image'), plt.xticks([]), plt.yticks([])

        plt.show()
    '''


if __name__ == '__main__':
    print("using opencv: ", cv2.__version__)

    #img_path = '/Users/mpaa/donkey-data/data/simulator/log/3404_cam-image_array_.jpg'
    img_path = '/Users/mpaa/donkey-data/data/data-7th/7th-set1/1164_cam-image_array_.jpg'

    test = Tester()
    test.process_and_save(img_path, "./test.jpg")
    #test.process_and_plot(img_path)
