from PIL import Image
from matrix_things import *

import numpy as np
import argparse


class Steganography:
    BLACK_PIXEL = (0, 0, 0)
    H = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                  [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]])

    def _merge_rgb(self, rgb1, rgb2, rgb3, rgb4, rgb_sm):

        r1, g1, b1 = int_to_bin(rgb1)
        r2, g2, b2 = int_to_bin(rgb2)
        r3, g3, b3 = int_to_bin(rgb3)
        r4, g4, b4 = int_to_bin(rgb4)
        r_sm, g_sm, b_sm = int_to_bin(rgb_sm)

        container_r = np.array(str_to_arr(r1[-3:] + r2[-4:] + r3[-4:] + r4[-4:]))
        container_g = np.array(str_to_arr(g1[-3:] + g2[-4:] + g3[-4:] + g4[-4:]))
        container_b = np.array(str_to_arr(b1[-3:] + b2[-4:] + b3[-4:] + b4[-4:]))

        m_r = np.array(str_to_arr(r_sm[:4]))
        m_g = np.array(str_to_arr(g_sm[:4]))
        m_b = np.array(str_to_arr(b_sm[:4]))

        mul_rh = matr_to_bin(np.dot(self.H, container_r))
        mul_gh = matr_to_bin(np.dot(self.H, container_g))
        mul_bh = matr_to_bin(np.dot(self.H, container_b))

        sub_r = matr_to_bin(m_r - mul_rh)
        sub_g = matr_to_bin(m_g - mul_gh)
        sub_b = matr_to_bin(m_b - mul_bh)

        cont_r = arr_to_str(set_bit(container_r, get_ind(sub_r)))
        cont_g = arr_to_str(set_bit(container_g, get_ind(sub_g)))
        cont_b = arr_to_str(set_bit(container_b, get_ind(sub_b)))

        nr1, nr2, nr3, nr4 = r1[:5] + cont_r[0:3], r2[:4] + cont_r[3:7], r3[:4] + cont_r[7:11], r4[:4] + cont_r[11:]
        ng1, ng2, ng3, ng4 = g1[:5] + cont_g[0:3], g2[:4] + cont_g[3:7], g3[:4] + cont_g[7:11], g4[:4] + cont_g[11:]
        nb1, nb2, nb3, nb4 = b1[:5] + cont_b[0:3], b2[:4] + cont_b[3:7], b3[:4] + cont_b[7:11], b4[:4] + cont_b[11:]

        rgb1 = nr1, ng1, nb1
        rgb2 = nr2, ng2, nb2
        rgb3 = nr3, ng3, nb3
        rgb4 = nr4, ng4, nb4

        res = [bin_to_int(rgb1), bin_to_int(rgb2), bin_to_int(rgb3), bin_to_int(rgb4)]

        return res

    def _unmerge_rgb(self, rgb1, rgb2, rgb3, rgb4):

        r1, g1, b1 = int_to_bin(rgb1)
        r2, g2, b2 = int_to_bin(rgb2)
        r3, g3, b3 = int_to_bin(rgb3)
        r4, g4, b4 = int_to_bin(rgb4)

        container_r = np.array(str_to_arr(r1[-3:] + r2[-4:] + r3[-4:] + r4[-4:]))
        container_g = np.array(str_to_arr(g1[-3:] + g2[-4:] + g3[-4:] + g4[-4:]))
        container_b = np.array(str_to_arr(b1[-3:] + b2[-4:] + b3[-4:] + b4[-4:]))

        mul_rh = arr_to_str(matr_to_bin(np.dot(self.H, container_r)))
        mul_gh = arr_to_str(matr_to_bin(np.dot(self.H, container_g)))
        mul_bh = arr_to_str(matr_to_bin(np.dot(self.H, container_b)))

        rgb = mul_rh + "0000", mul_gh + "0000", mul_bh + "0000"

        return bin_to_int(rgb)

    def merge(self, image1, image2):

        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')

        map1 = image1.load()
        map2 = image2.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        i_sm = 0
        j_sm = 0
        for i in range(image1.size[0]):
            for j in range(0, image1.size[1] - 4, 4):
                is_valid = lambda: i_sm < image2.size[0] and j_sm < image2.size[1]
                rgb1 = map1[i, j]
                rgb2 = map1[i, j + 1]
                rgb3 = map1[i, j + 2]
                rgb4 = map1[i, j + 3]
                rgb_sm = map2[i_sm, j_sm] if is_valid() else self.BLACK_PIXEL
                rgb_arr = self._merge_rgb(rgb1, rgb2, rgb3, rgb4, rgb_sm)
                new_map[i, j] = rgb_arr[0]
                new_map[i, j + 1] = rgb_arr[1]
                new_map[i, j + 2] = rgb_arr[2]
                new_map[i, j + 3] = rgb_arr[3]
                j_sm += 1
            j_sm = 0
            i_sm += 1

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()
        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()
        i_sm = 0
        j_sm = 0
        for i in range(image.size[0]):
            for j in range(0, image.size[1] - 4, 4):
                new_map[i_sm, j_sm] = self._unmerge_rgb(pixel_map[i, j], pixel_map[i, j + 1],
                                                        pixel_map[i, j + 2],
                                                        pixel_map[i, j + 3])
                j_sm += 1
            i_sm += 1
            j_sm = 0

        return new_image


class Steganography2:
    BLACK_PIXEL = (0, 0, 0)

    def _merge_rgb(self, rgb1, rgb2):
        r1, g1, b1 = int_to_bin(rgb1)
        r2, g2, b2 = int_to_bin(rgb2)
        rgb = r1[:4] + r2[:4], g1[:4] + g2[:4], b1[:4] + b2[:4]
        return bin_to_int(rgb)

    def _unmerge_rgb(self, rgb):
        r, g, b = int_to_bin(rgb)
        new_rgb = r[4:] + '0000', g[4:] + '0000', b[4:] + '0000'
        return bin_to_int(new_rgb)

    def merge(self, image1, image2):
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')

        map1 = image1.load()
        map2 = image2.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                is_valid = lambda: i < image2.size[0] and j < image2.size[1]
                rgb1 = map1[i, j]
                rgb2 = map2[i, j] if is_valid() else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2)

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()

        # Create the new image and load the pixel map
        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                new_map[i, j] = self._unmerge_rgb(pixel_map[i, j])

        return new_image


def main():
    print("Hi! This program will hide or find one of your images in another! What do you want to do?")
    print("1. Encrypt one image in another\r\n2. Decode a picture from another")
    wh = input("I want to: ")

    if wh == '1':
        image1 = input("Path to image#1: ")
        image2 = input("Path to image#2: ")
        try:
            image1s = Image.open(image1)
        except:
            print("First picture was not found")
            exit()
        try:
            image2s = Image.open(image2)
        except:
            print("Second picture was not found")
            exit()
        print(
            "Great! Choose the algorithm you want to use.\r\n1. Hamming (slow, but doesn't spoil the original picture, "
            "the second one should be 4 times smaller than the first one).\r\n2. Simple Steganography(fast, messes up "
            "the original image)")
        tp = input("My choice is: ")

        print("Ok, what will be the name of the encrypted file?")
        s_image = input("Name: ")

        if tp == '1':
            print("The encryption process has started")
            Steganography().merge(image1s, image2s).save('output/' + s_image + '.png')
        elif tp == '2':
            print("The encryption process has started")
            Steganography2().merge(image1s, image2s).save('output/' + s_image + '.png')
        else:
            print("Wrong input")
        print("Process is complete, enjoy the result")
    elif wh == '2':
        images = input("Path to image: ")
        try:
            image = Image.open(images)
        except:
            print("Picture was not found")
            exit()

        print("What algorithm to use for decoding?\r\n1. Hemming.\r\n2. Simple")
        tp = input("My choice is: ")
        print("Ok, what will be the name of the decrypted file?")
        s_image = input("Name: ")

        if tp == '1':
            print("The decryption process has started")
            Steganography().unmerge(image).save('output/' + s_image + '.png')
        elif tp == '2':
            print("The decryption process has started")
            Steganography2().unmerge(image).save('output/' + s_image + '.png')
        else:
            print("Wrong input")
        print("Process is complete, enjoy the result")
    else:
        print("Incorrect input")


if __name__ == '__main__':
    main()
    input()
