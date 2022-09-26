import numpy as np
import cv2


def processImage(image, threshold1, threshold2):
    """
    Purpose: Modifies the image by applying canny, dilation, and countours of the image to 
    identify the subject of the image and make the background black
    Parameters: Given image
    Returns: Cropped image
    (Chapters 6, 10, 11, & dilate)
    """
  
    canned = cv2.Canny(image, threshold1, threshold2)
    # cv2.imshow("Canny", canned)

    # apply mask (thick outline)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.dilate(canned, kernel, iterations = 1)
    cv2.imshow("Mask real", mask)

    # find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    # crop_mask = np.zeros_like(mask) 
    cv2.drawContours(mask, contours, -1, (255), -1)
    cv2.imshow("crop mask", mask) 
    
    # crop image
    crop = np.zeros_like(image) 
    crop[mask == 255] = image[mask == 255]

    return crop


def resizeBackground(imgName, crop):
    """
    Purpose: Find the dimensions of the cropped and background image, and make them both
    the same size, based on the dimensions of the cropped image
    Parameters: Background image and cropped image
    Returns: Returns the resized background and unchanged cropped image.
    (Chapter 3 & resizing)
    """
    background = cv2.imread(imgName)
    # crop pic to fit image size
    backHeight, backWidth, backChannels = background.shape
    print("background dimensions:", backHeight, backWidth)

    cropHeight, cropWidth, cropChannels = crop.shape
    print("image dimensions:", cropHeight, cropWidth)

    cropBack = cv2.resize(background, (cropWidth, cropHeight))
    resizedCrop = cv2.resize(crop, (cropWidth, cropHeight))
 
    # cv2.imshow("cropBack", cropBack)
    # cv2.imshow("resizedCrop", resizedCrop)

    return cropBack, resizedCrop


def combineImages(resizedCrop, cropBack):
    """
    Purpose: Paste the cropped image onto the background by iterating through each pixel and
    drawing the background onto the black (off) pixels of the cropped image  
    Parameters: Cropped image and same dimension background
    Returns: Returns the finished image with the cropped image over the background
    (Chapter 4 & Combining images by looping through each pixel; variation on masking)
    """
    finalImage = resizedCrop.copy()
    finalHeight, finalWidth, finalChannels = finalImage.shape
    # print(finalHeight, finalWidth)
    for x in range(finalHeight):
        for y in range(finalWidth):
            # print(x,y)
            b, g, r = finalImage[x,y]
            # print(b, g, r)

            # check if pixel in crop img is on/off
            # if off: get pixel at exact location in background and draw onto black pixel
            # if on: don't change
            if b == 0 and g == 0 and r == 0:
                # get pixel values of background
                backPixel = cropBack[x,y]
                finalImage[x][y] = np.array(backPixel)
   
    return finalImage


def main():

    image = cv2.imread("boy.jpeg")
    # man: 10, 60
    # boy: 100, 200
    # rice: 100, 200
    # hw: 20, 175
    # beach: 600, 150
    crop = processImage(image, 100, 200)
    # blurFinal = blurImgBackground(image, crop)
    cropBack, resizedCrop = resizeBackground("beachback.jpeg", crop)
    boyBackFinal = combineImages(resizedCrop, cropBack)
    cv2.imshow("Boy Original", image)
    cv2.imshow("Boy Background Final", boyBackFinal)
    cv2.waitKey(0)

    image2 = cv2.imread("rice.jpeg")
    # man: 10, 60
    # boy: 100, 200
    # rice: 100, 200
    # hw: 20, 175
    # beach: 600, 150
    crop = processImage(image2, 100, 200)
    # blurFinal = blurImgBackground(image2, crop)
    cropBack, resizedCrop = resizeBackground("beachback.jpeg", crop)
    riceBackFinal = combineImages(resizedCrop, cropBack)
    cv2.imshow("Rice Original", image2)
    cv2.imshow("Rice Background Final", riceBackFinal)
    cv2.waitKey(0)

    image3 = cv2.imread("hw.jpeg")
    # man: 10, 60
    # boy: 100, 200
    # rice: 100, 200
    # hw: 20, 175
    # beach: 600, 150
    crop = processImage(image3, 20, 175)
    # blurFinal = blurImgBackground(image3, crop)
    cropBack, resizedCrop = resizeBackground("beachback.jpeg", crop)
    hwBackFinal = combineImages(resizedCrop, cropBack)
    cv2.imshow("HW Original", image3)
    cv2.imshow("HW Background Final", hwBackFinal)
    cv2.waitKey(0)

    image4 = cv2.imread("beach.jpeg")
    # man: 10, 60
    # boy: 100, 200
    # rice: 100, 200
    # hw: 20, 175
    # beach: 600, 150
    crop = processImage(image4, 600, 150)
    # blurFinal = blurImgBackground(image3, crop)
    cropBack, resizedCrop = resizeBackground("beachback.jpeg", crop)
    hwBackFinal = combineImages(resizedCrop, cropBack)
    cv2.imshow("Beach Original", image4)
    cv2.imshow("Beach Background Final", hwBackFinal)
    cv2.waitKey(0)

    # show 
    # cv2.imshow("cropped", crop)
    # cv2.imshow("Original", image)
    # cv2.imshow("Blurred Final", blurFinal)

main()

