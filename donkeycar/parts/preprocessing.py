import numpy as np
import time
import cv2


class PreProcessor:
    def __init__(self, kernel_size=9, blend_colors=True, canny_min=100, canny_max=200, crop_area=None):
        #We could initialize some variables based on a single snapshot, fex size, thresholds, etc
        self.morph_kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.canny_min = canny_min
        self.canny_max = canny_max
        self.blend_colors = blend_colors
        self.crop_area = crop_area

    def run(self, img_arr):
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
        #print("Elapsed: ", (end - start)*1000, " ms")

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

