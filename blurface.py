import numpy as np
import argparse
import cv2


def getImage():
    """
    Purpose: Reads in the given image in the command line
    Parameters: None
    Returns: Returns the processed image
    (Chapter 3)
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True,
    help = "Path to the image")
    args = vars(ap.parse_args())
    image = cv2.imread(args["image"])
    return image

def processImage(image):
    """
    Purpose: Modifies the image by applying canny, dilation, and countours of the image to 
    identify the subject of the image and make the background black
    Parameters: Given image
    Returns: Cropped image
    (Chapters 6, 10, 11, & dilate)
    """
    # man: 10, 60
    # boy: 100, 200
    # rice: 100, 200
    # hw: 20, 175
    canned = cv2.Canny(image, 20, 175)
    # cv2.imshow("Canny", canned)

    # apply mask (thick outline)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.dilate(canned, kernel, iterations = 1)
    cv2.imshow("Mask real", mask)

    # find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    crop_mask = np.zeros_like(mask) 
    cv2.drawContours(crop_mask, contours, -1, (255), -1)
    # cv2.imshow("crop mask", crop_mask) 
    
    # crop image
    crop = np.zeros_like(image) 
    crop[crop_mask == 255] =  image[crop_mask == 255]

    return crop

def resizeBackground(imgName, crop):
    """
    Purpose: Find the dimensions of the cropped and background image, and make them both
    the same size, based on the dimensions of the cropped image
    Parameters: Background image and cropped image
    Returns: Returns the resized background and unchanged cropped image.
    (Chapter 3 & resizing)
    """
    background = cv2.imread("beachback.jpg")
    # crop pic to fit image size
    backHeight, backWidth, backChannels = background.shape
    print("background:", backHeight, backWidth)

    cropHeight, cropWidth, cropChannels = crop.shape
    print("image:", cropHeight, cropWidth)

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
    (Combining images by looping through each pixel; variation on masking)
    """
    finalImage = resizedCrop.copy()
    finalHeight, finalWidth, finalChannels = finalImage.shape
    print(finalHeight, finalWidth)
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

    image = getImage()

    crop = processImage(image)

    cropBack, resizedCrop = resizeBackground("beachback.jpg", crop)

    finalImage = combineImages(resizedCrop, cropBack)

    # show 
    cv2.imshow("cropped", crop)
    cv2.imshow("Final", finalImage)

main()



# cv2.imshow("cropBack", cropBack)
# cv2.imshow("resizedCrop", resizedCrop)


# cv2.imshow("Original", image) 
# blurred = cv2.blur(image, (15, 15))
# cv2.imshow("blurred", blurred)

# masked = cv2.bitwise_xor(crop, cropBack)
# cv2.imshow("original", image)
# cv2.imshow("Final", masked)

cv2.waitKey(0) 

