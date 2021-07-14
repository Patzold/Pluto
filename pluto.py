# Pluto
# v0.0.3

import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

# from tensorflow.python.ops.gen_array_ops import reverse
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

IMG_SIZE = 256

use_tesseract = False
use_easyocr = False

tesseract_path = ""

def read_image(path: str, no_BGR_correction=False):  # -> np.ndarray
    """Returns an image from a path as a numpy array
    
    Args:
        path: location of the image
        no_BGR_correction: When True, the color space is not converted from BGR to RGB
    
    Returns:
        The read image as np.ndarray.
    
    Raises:
        AttributeError: if path is not valid, this causes image to be None
    """
    image = cv2.imread(path)
    if image is None: raise AttributeError("Pluto ERROR in read_image() function: Image path is not valid, read object is of type None!")
    if no_BGR_correction: return image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def show_image(image: np.ndarray, BGR2RGB=False):
    """Displays an image using matplotlib's pyplot.imshow()
    
    Args:
        image: the image to be displayed
        BGR2RGB: When True, the color space is converted from BGR to RGB
    """
    if BGR2RGB: image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()

def merge(aimg: np.ndarray, bimg: np.ndarray):  # -> np.ndarray
    """Merges two images, aimg being the foreground and bimg being the background.
    
    aimg.shape[0] < bimg.shape[0] and aimg.shape[1] < bimg.shape[1] and matching dimensions for the color channel(s)
    Only works with RGB and grayscale images.
    
    Raises:
        Exception when dimensions are not matching
    
    Returns:
        A np.ndarray with the dimensions of bimg.
    """
    color_channels = 1
    if len(aimg.shape) == len(bimg.shape):
        if aimg.shape[2] == 3: color_channels = 3
        else:
            print("Pluto WARNING - Input 1 shape: ", aimg.shape, " Input 2 shape: ", bimg.shape)
            raise Exception("Images must both be RGB or grayscale. Wrong ammount of color channels detected.")
    else:
        print("Pluto WARNING - Input 1 shape: ", aimg.shape, " Input 2 shape: ", bimg.shape)
        raise Exception("Images must have matching dimensions for the color channels.")
    out = np.zeros((bimg.shape[0], bimg.shape[1], color_channels), dtype=np.uint8)
    maxi = aimg.shape[0]
    maxj = aimg.shape[1]
    for i in range(bimg.shape[0]):
        for j in range(bimg.shape[1]):
            out[i][j] = bimg[i][j]
            if i < maxi and j < maxj:
                out[i][j] = aimg[i][j]
    return out

def input_image(path: str):  # -> np.ndarray
    """Reads image and prepares it for the segmentation models
    The correct dimension for the segmentation models is 256x256.

    Args:
        path: The location of the image.

    Returns:
        A np.ndarray of the image with correct dimensions.

    Raises:
        AttributeError: If path is not valid. (from read_image())
    """
    image = read_image(path)
    imshape = image.shape
    image_dimension = max(imshape[0], imshape[1])
    # The neural network input image size is 256x256.
    bg_dimension = 0
    if image_dimension < 256: bg_dimension = 256
    elif image_dimension < 512: bg_dimension = 512
    else:
        bg_dimension = 768
        scale_factor = 768 / image_dimension
        image = cv2.resize(image, (int(imshape[1] * scale_factor), int(imshape[0] * scale_factor)))
    bg_r = np.full((bg_dimension, bg_dimension), 22)
    bg_g = np.full((bg_dimension, bg_dimension), 32)
    bg_b = np.full((bg_dimension, bg_dimension), 42)
    background = cv2.merge((bg_r, bg_g, bg_b))
    out = merge(image, background)
    return out

def ocr(image, override=False, function_use_tesseract=False, function_use_easyocr=False):
    if use_tesseract:
        if tesseract_path == "": print("Pluto WARNING - Please check if tesseract_path has been set.")
        from pytesseract import pytesseract
        pytesseract.tesseract_cmd = tesseract_path
        text = pytesseract.image_to_string(image)
        return text
    if use_easyocr:
        import easyocr
        reader = easyocr.Reader(['en'])
        return reader.readtext(image, detail=0)
    
    print("Pluto WARNING - Check if use_tesseract and use_easyocr attributes are set.")
    return None

def expand_to_rows(image: np.ndarray):
    """
    Args:
        image: An image as np.ndarray, which represents a mask
    """
    dimensions = image.shape
    for i in range(int(dimensions[0] / 2)):
        for j in range(dimensions[1]):
            if image[i][j] > 200:
                image[i] = [255 for k in range(dimensions[1])]
    for i in range(int(dimensions[0] / 2), dimensions[0]):
        for j in range(dimensions[1]):
            image[i][j] = 0
    return image

def sgmtn_stats(image, reverse_output=False, reverse_only=False):
    # Requires RGB image. Returns masked image in original dimensions.
    original_dimensions = image.shape
    
    try:
        import tensorflow as tf
    except ModuleNotFoundError as e:
        print("Please make shure to install Tensorflow dependency. Original error: ", e)
    
    new_array = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    image_reshape = new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3) 
    
    model = tf.keras.models.load_model("D:/Codeing/Twitter_Segmentation/model_1")
    prediction = model.predict(image_reshape)[0] * 255
    
    output_mask_blur = cv2.blur(prediction, (10, 10))
    output_mask_rough = (output_mask_blur > 0.9).astype(np.uint8) * 255
    output_mask_upscale = cv2.resize(output_mask_blur, (original_dimensions[0], original_dimensions[1]))
    
    output = np.zeros((original_dimensions[0], original_dimensions[1], 3)).astype(np.uint8)
    reverse = np.zeros((original_dimensions[0], original_dimensions[1], 3)).astype(np.uint8)
    
    for i in range(original_dimensions[0]):
        for j in range(original_dimensions[1]):
            if output_mask_upscale[i][j] > 0.5:
                for c in range(3):
                    output[i][j][c] = image[i][j][c]
                    reverse[i][j][c] = 0.0
            else:
                for c in range(3):
                    output[i][j][c] = 0.0
                    reverse[i][j][c] = image[i][j][c]
    
    if reverse_output:
        return output, reverse
    elif reverse_only:
        return reverse
    else:
        return output

def get_text(image, already_segmented=False):
    header_subtracted = image
    if not already_segmented:
        header_subtracted = sgmtn_header(image, False, True)
    show_image(header_subtracted)
    ocr_result = ocr(header_subtracted)
    lines = ocr_result.split("\n")
    print(lines)
    # show_image(header_subtracted)

def get_stats(image, already_segmented=False):
    stats_subtracted = image
    if not already_segmented:
        stats_subtracted = sgmtn_stats(image)
    show_image(stats_subtracted)
    ocr_result = ocr(stats_subtracted)
    lines = ocr_result.split("\n")
    print(lines)
    show_image(stats_subtracted)

def ocr_cleanup(text: str):  # -> str
    """Removes unwanted characters or symbols from a text
    
    This includes \n, \x0c, and multiple ' ' 
    
    Args:
        text: The String for cleanup.
    
    Returns:
        The cleaned text as String.
    """
    out = text.replace("\n", "")
    out = out.replace("\x0c", "")
    out = " ".join(out.split())
    
    splits = out.split(",")
    clean_splits = []
    
    for phrase in splits:
        arr = list(phrase)
        l = len(arr)
        start = 0
        end = l
        for i in range(0, l):
            if arr[i] == " ": start += 1
            else: break
        for i in range(l, 0, -1):
            if arr[i-1] == " ": end -= 1
            else: break
        clean_splits.append(phrase[start:end])
    
    out = ""
    for phrase in clean_splits:
        out += phrase
        out += ", "
    out = out[:-2]
    
    return out

def mask_overlay(base: np.ndarray, mask1: np.ndarray, mask2=None, display=False):  # -> np.ndarray
    """Shows up to two mask by overlaying them on the original image.
    
    Mask images must be 255x255, base 3 color channels and both masks 1 color channel!
    
    Raises:
        AttributeError: When base or mask1 are None
        Exception when wrong dimensions.
    
    Returns:
        np.ndarray with the dimensions of bimg
    """
    print(base.shape)
    if base is None: raise AttributeError("Pluto ERROR in mask_overlay() function: 'base' parameter is of type None!")
    if mask1 is None: raise AttributeError("Pluto ERROR in mask_overlay() function: 'mask1' parameter is of type None!")
    print(base.shape)
    if base.shape != (256, 256, 3):
        print("Pluto WARNING - mask_overlay() - 'base' shape: ", base.base)
        raise Exception("The dimension of the 'base' image must be 256x256x3!")
    if mask1.shape != (256, 256):
        print("Pluto WARNING - mask_overlay() - mask1 shape: ", mask1.shape)
        raise Exception("mask1 must be 256x256!")
    black_img = np.zeros([256, 256]).astype(np.uint8)
    over_img = (mask1).astype(np.uint8)
    cor_overlay_image = cv2.merge((over_img, black_img, black_img))
    out = cv2.addWeighted(base, 0.5, cor_overlay_image, 1.0, 0)
    if mask2 is not None:
        if mask2.shape != (256, 256):
            print("Pluto WARNING - mask_overlay() - mask2 shape: ", mask2.shape)
            raise Exception("mask2 must be 256x256!")
        over_img = (mask2).astype(np.uint8)
        cor_overlay_image = cv2.merge((black_img, black_img, over_img))
        out = cv2.addWeighted(out, 0.5, cor_overlay_image, 1.0, 0)
    if display: show_image(out)
    print(type(out))
    return out

def display_masks(mask1, mask1_pp=None, mask2=None, mask2_pp=None):
    try:
        cv2.imshow("pred", mask1)
    except Exception as e:
        print("Pluto ERROR - In display_masks(), origininal error message: ", e)
        quit()
    cv2.imshow("mask", mask1_pp)
    cv2.waitKey(0)
    cv2.imshow("mask2", mask2)
    cv2.imshow("mask", mask2_pp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def nyt_sgmt(input_image: np.ndarray, verbose=1):  # -> np.ndarray
    """Uses a neural network to segmentate a screenshot of a NYT article
    
    Args:
        input_image: The screenshot for segmentation, color and ideally 256x256x3
        verbose: log level. 1 for prints, 0 for keeping the output clean
    
    Returns:
        output_mask_rough0: np.ndarray with post-processed result of nyt_model_0 (isolates title)
        output_mask_rough1: np.ndarray with post-processed result of nyt_model_1 (isolates text body)
    """
    if verbose == 1: print("Pluto NYT --- Loading models...")
    import tensorflow as tf
    model_input = cv2.resize(input_image, (IMG_SIZE, IMG_SIZE)) # The model expects an image of size 256x256x3
    model_input = model_input.reshape(-1, IMG_SIZE, IMG_SIZE, 3) # Tensorflow requires the dimensions to be (1, 256, 256, 3)
    model0 = tf.keras.models.load_model("models/nyt_model_0") # load both models from the "models" folder
    model1 = tf.keras.models.load_model("models/nyt_model_1")
    
    if verbose == 1: print("Pluto NYT --- Segmentation & post-processing...")
    prediction0 = model0.predict(model_input)[0] * 255  # The model returns its predictions in the dimension (1, 256, 256, 1) with values ranging from 0-1
    prediction1 = model1.predict(model_input)[0] * 255  # But the desired output is (256, 256, 1) with values ranging from 0-255

    output_mask_blur0 = cv2.blur(prediction0, (2, 2)) # Some post-processing on the segmentation mask
    output_mask_rough0 = (output_mask_blur0 > 0.999).astype(np.uint8) * 255

    output_mask_blur1 = cv2.blur(prediction1, (2, 2))
    output_mask_rough1 = (output_mask_blur1 > 0.999).astype(np.uint8) * 255
    
    # display_masks(None)
    
    # mask_overlay(input_image, output_mask_rough0, output_mask_rough1, True)
    
    return output_mask_rough0, output_mask_rough1

def mask_color(img: np.ndarray, mask: np.ndarray, reverse2=False):  # -> np.ndarray
    """Applies a mask oto an image, isolating the area of interest
    
    Args:
        img: The image the mask should be applied to.
        mask: The mask as a grayscale image.
        reverse2: If True, an additional image with an inverted mask applied.
    
    Returns:
        One or two image(s) as np.ndarray with an applied mask.
    """
    dimensions_img = img.shape
    dimensions_mask = mask.shape
    if dimensions_img != dimensions_mask:
        if dimensions_img < dimensions_mask: img = cv2.resize(img, (dimensions_mask[0], dimensions_mask[1]))
        else: mask = cv2.resize(mask, (dimensions_img[0], dimensions_img[1]))
    output = np.zeros((dimensions_img[0], dimensions_img[1], 3)).astype(np.uint8)
    if reverse2: reverse = np.zeros((dimensions_img[0], dimensions_img[1], 3)).astype(np.uint8)
    for i in range(dimensions_img[0]):
        for j in range(dimensions_img[1]):
            if mask[i][j] > 0.5:
                for c in range(3):
                    output[i][j][c] = img[i][j][c]
                    if reverse2: reverse[i][j][c] = 0.0
            else:
                for c in range(3):
                    output[i][j][c] = 0.0
                    if reverse2: reverse[i][j][c] = img[i][j][c]
    if reverse2: return output, reverse
    return output

def nyt_extract(img: np.ndarray, title_mask: np.ndarray, body_mask: np.ndarray, verbose=1):  # -> str
    """Applies the OCR on isolated parts of an image
    
    Args:
        img: The original screenshot
        title_mask: Mask that isolates the title, must be grayscale
        body_mask: Mask that isolates the text body, must be grayscale
        verbose: log level. 1 for prints, 0 for keeping the output clean
    
    Returns:
        title_raw_ocr: String with raw result of the OCR library applied to the title
        body_raw_ocr: String with raw result of the OCR library applied to the text body
    """
    title_insight = mask_color(img, title_mask)
    body_insight = mask_color(img, body_mask)
    # use_tesseract = False
    # use_easyocr = True
    show_image(title_insight)
    if verbose == 1: print("Pluto NYT --- Performing OCR...")
    title_ocr_result = ocr_cleanup(ocr(title_insight))
    show_image(body_insight)
    body_ocr_result = ocr_cleanup(ocr(body_insight))
    return title_ocr_result, body_ocr_result

def nyt(img: np.ndarray, verbose=1):
    """High-level function
    Extracts information from screenshots of New York Times articles.
    
    Args:
        img: The screenshot
        verbose: log level. 1 for prints, 0 for keeping the output clean
    """
    title_mask, body_mask = nyt_sgmt(img, verbose)
    extracted_data = nyt_extract(img, title_mask, body_mask, verbose)
    print(extracted_data)

class PlutoObject:
    def __init__(self, img: np.ndarray):
        self.img = img
        self.use_tesseract = True
        self.tesseract_path = ""
        self.use_easyocr = False
    
    def ocr(self, image=None, override=False, function_use_tesseract=False, function_use_easyocr=False):  # -> str
        """Preforms OCR on a given image, using ether Tesseract or EasyOCR
        
        Args:
            image: np.ndarray of the to be treated image.
        
        Returns:
            String with the raw result of the OCR library.
        
        """
        if self.use_tesseract:
            if self.tesseract_path == "": print("Pluto WARNING - Please check if tesseract_path has been set.")
            from pytesseract import pytesseract
            pytesseract.tesseract_cmd = self.tesseract_path
            text = pytesseract.image_to_string(image)
            return text
        if self.use_easyocr:
            import easyocr
            reader = easyocr.Reader(['en'])
            return reader.readtext(image, detail=0)

        print("Pluto WARNING - Check if use_tesseract and use_easyocr attributes are set.")
        return None

    def expand_to_rows(self, image: np.ndarray, full=False, value=200):  # -> np.ndarray
        """
        Args:
            image: An grayscale image as np.ndarray, which represents a mask.
        
        Returns:
            A np.ndarray of the edited image.
        """
        dimensions = image.shape
        imglen = dimensions[0]
        if not full: imglen = dimensions[0] / 2
        for i in range(int(imglen)):
            for j in range(dimensions[1]):
                if image[i][j] > value:
                    image[i] = [255 for k in range(dimensions[1])]
        for i in range(int(imglen), dimensions[0]):
            for j in range(dimensions[1]):
                image[i][j] = 0
        return image
    
    def ocr_cleanup(self, text: str):  # -> str
        """Removes unwanted characters or symbols from a text
        
        This includes \n, \x0c, and multiple ' ' 
        
        Args:
            text: The String for cleanup.
        
        Returns:
            The cleaned text as String.
        """
        out = text.replace("\n", " ")
        out = out.replace("\x0c", "")
        out = " ".join(out.split())
        
        splits = out.split(",")
        clean_splits = []
        
        for phrase in splits:
            arr = list(phrase)
            l = len(arr)
            start = 0
            end = l
            for i in range(0, l):
                if arr[i] == " ": start += 1
                else: break
            for i in range(l, 0, -1):
                if arr[i-1] == " ": end -= 1
                else: break
            clean_splits.append(phrase[start:end])
        
        out = ""
        for phrase in clean_splits:
            out += phrase
            out += ", "
        out = out[:-2]
        
        return out

    def to_json(self, data: dict):
        import json
        out = json.dumps(data)
        return out

    def __init__(self, image, handle=None):
        self.image = image
        self.handle = handle
    
    def sgmtn_header(self, image=None, reverse_output=False, reverse_only=False):  # -> np.ndarray
        """Applies the header segmentation model to an image
        
        Args:
            image: An image as np.ndarray for the segmentation model
            reverse_output: True, if a second image with an inverted mask should be output.
            reverse_only: True, if only an image with an inverted mask should be output.
        
        Returns:
            An np.ndarray with the masked image in original dimensions.
        """
        # Requires RGB image. Returns masked image in original dimensions.
        if image is None: image = self.image
        original_dimensions = image.shape
        
        try:
            import tensorflow as tf
            from tensorflow.compat.v1.keras.backend import set_session
            config = tf.compat.v1.ConfigProto()
            config.gpu_options.allow_growth = True
            config.log_device_placement = True
            sess = tf.compat.v1.Session(config=config)
            set_session(sess)
        except ModuleNotFoundError as e:
            print("Please make shure to install Tensorflow dependency. Original error: ", e)
        
        new_array = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        image_reshape = new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3) 
        
        model = tf.keras.models.load_model("D:/Codeing/Twitter_Segmentation/model_2")
        prediction = model.predict(image_reshape)[0] * 255
        
        output_mask_blur = cv2.blur(prediction, (10, 10))
        output_mask_rough = (output_mask_blur > 0.9).astype(np.uint8) * 255
        output_mask_upscale = cv2.resize(output_mask_blur, (original_dimensions[0], original_dimensions[1]))
        output_mask = expand_to_rows(output_mask_upscale)
        show_image(output_mask)
        output = np.zeros((original_dimensions[0], original_dimensions[1], 3)).astype(np.uint8)
        reverse = np.zeros((original_dimensions[0], original_dimensions[1], 3)).astype(np.uint8)
        
        for i in range(original_dimensions[0]):
            for j in range(original_dimensions[1]):
                if output_mask_upscale[i][j] > 0.5:
                    for c in range(3):
                        output[i][j][c] = image[i][j][c]
                        reverse[i][j][c] = 0.0
                else:
                    for c in range(3):
                        output[i][j][c] = 0.0
                        reverse[i][j][c] = image[i][j][c]
        
        if reverse_output:
            return output, reverse
        elif reverse_only:
            return reverse
        else:
            return output
    
    def get_header(self, image=None, already_segmented=False):  # -> str
        """Extracts the Username and Handle from the image
        
        Args:
            image: The screenshot as np.ndarray, by default the self.image
            already_segmentated = When the image is already correctly segmentated, choose True.
        
        Returns:
        """
        if image is None:
            image = self.image
        text_subtracted = image
        if not already_segmented:
            text_subtracted, header_subtracted = self.sgmtn_header(image, True)
        
        show_image(text_subtracted)
        show_image(header_subtracted)
        # print(ocr(text_subtracted))
        ocr_result = ocr_cleanup(ocr(text_subtracted))
        print("OCR clean: ", ocr_result)
        print(ocr(header_subtracted))
        data = ocr_result.split("@")
        self.handle = data[1]
        return data[0], data[1]
    
    def open_account(self, handle=None):
        """Opens the URL to the account with given handle
        
        Args:
            handle: The handle of the account (without '@' in the beginning)
        """
        if handle is None: handle = self.handle
        import webbrowser
        webbrowser.open(("https://twitter.com/" + handle), new=2)