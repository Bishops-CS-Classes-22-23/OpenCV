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

    # apply mask (thick outli ne)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.dilate(canned, kernel, iterations = 1)
    # cv2.imshow("Mask real", mask)

    # find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    cv2.drawContours(mask, contours, -1, (255), -1)
    # cv2.imshow("crop mask", mask) 
    
    # draw original image onto white parts of the crop mask by first making crop img black, 
    # then making all contoured pixels white 
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

    # crop background to fit original image size
    backHeight, backWidth, backChannels = background.shape
    print("\nbackground dimensions:", backHeight, backWidth)

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

    # make copy of image and find dimensions of image
    finalImage = resizedCrop.copy()
    finalHeight, finalWidth, finalChannels = finalImage.shape
    # loop throgh each pixel
    for x in range(finalHeight):
        for y in range(finalWidth):
            b, g, r = finalImage[x,y]

            # check if pixel in crop img is on/off
            # if off: get pixel at exact location in background and draw onto black pixel
            # if on: don't change
            if b == 0 and g == 0 and r == 0:
                # get pixel values of background
                backPixel = cropBack[x,y]
                finalImage[x][y] = np.array(backPixel)
   
    return finalImage


def displayImages(imgName, thresh1, thresh2):
    """
    Purpose: Read in all the functions and display the final image with the subject and virtual background.
    Parameters: The subject image file name, and the two threshold numbers for canny.
    Returns: None, but displays the original and finished image.
    (Chapter 3)
    """
    image = cv2.imread(imgName)
    nameList = imgName.split(".")

    # man: 10, 60
    # boy: 100, 200
    # rice: 100, 200
    # hw: 20, 175
    # beach: 600, 150
    crop = processImage(image, thresh1, thresh2)
    # blurFinal = blurImgBackground(image, crop)
    cropBack, resizedCrop = resizeBackground("beachback.jpeg", crop)
    backFinal = combineImages(resizedCrop, cropBack)
    cv2.imshow("%s Original" % nameList[0], image)
    cv2.imshow("%s Background Final" % nameList[0], backFinal)
    cv2.waitKey(0)


def main():
    
    displayImages("Boy.jpeg", 100, 200)

    displayImages("Rice.jpeg", 100, 200)

    displayImages("HW.jpeg", 15, 175)

    displayImages("Beach.jpeg", 600, 165)

    displayImages("Man.jpeg", 0, 50)
 
main()

