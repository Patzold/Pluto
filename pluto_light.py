# Pluto
# v0.1.0

import numpy as np
import matplotlib.pyplot as plt
import cv2

def read_image(path: str, no_BGR_correction=False):  # -> np.ndarray
    """Returns an image from a path as a numpy array
    
    Args:
        path: location of the image.
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
        image: The image to be displayed.
        BGR2RGB: When True, the color space is converted from BGR to RGB.
    """
    if BGR2RGB: image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()

def avg_of_row(img: np.ndarray, row: int, ovo=False):  # -> int | list
    """Calculates the average pixel value for one row of an image
    
    Args:
        img: The screenshot as np.ndarray
        row: which row of the image should be analysed?
        ovo: output as 'one value only' instead of list?
    
    Returns:
        The average value per row, ether one value only or per color channel value
    """
    all_values_added = 0
    if img.shape[2] == 3: all_values_added = [0, 0, 0]
    length = len(img)
    for pixl in img[row]: all_values_added += pixl
    out = all_values_added / length
    if ovo: out = sum(out) / 3
    return out

def avg_of_collum(img: np.ndarray, collum: int, ovo=False):  # -> int | list
    """Calculates the average pixel value for one collum of an image
    
    Args:
        img: The screenshot as np.ndarray
        collum: which collum of the image should be analysed?
        ovo: output as 'one value only' instead of list?
    
    Returns:
        The average value per collum, ether one value only or per color channel value
    """
    all_values_added = 0
    if img.shape[2] == 3: all_values_added = [0, 0, 0]
    length = len(img[0])
    for pixl in img[:, collum]: all_values_added += pixl
    out = all_values_added / length
    if ovo: out = sum(out) / 3
    return out

def trimm_and_blur(inpt: np.ndarray, less: bool, value: int, blurs, trimm, double_down=False, invert=None):
    for i in range(len(inpt)):
        for j in range(len(inpt[i])):
            if less:
                if inpt[i][j][0] > value or inpt[i][j][1] > value or inpt[i][j][2] > value:
                    inpt[i][j] = np.array(trimm)
                elif double_down:
                    inpt[i][j] = np.array(invert)
            else:
                if inpt[i][j][0] < value or inpt[i][j][1] < value or inpt[i][j][2] < value:
                    inpt[i][j] = np.array(trimm)
                elif double_down:
                    inpt[i][j] = np.array(invert)
    blur = cv2.blur(inpt, blurs)
    return blur

def to_grayscale(img: np.ndarray): # -> np.ndarray
    """Converts a color image to grayscale.
    Note: If the input image has dimensions of 200x200x3, the output image will have dimensions of 200x200.
    
    Args:
        img: color image with BGR channel order
    
    Returns:
        The input image as grayscale.
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def iso_grayscale(img: np.ndarray, less_than, value, convert_grayscale=False, blur=(1, 1)): # -> np.ndarray
    """Isolates image areas with a specific value
    
    Args:
        img: input image as np.ndarray
        less_than: Sets filter technique to less than / bigger than
        value: Value to filter by
        convert_to:grayscale: True if the input image is color and needs to be converted to grayscale first
        blur: optional blur kernal size
    
    Returns:
        modified input image as np.ndarray
    """
    if convert_grayscale: img = to_grayscale(img)

    if less_than:
        for i in range(len(img)):
            for j in range(len(img[i])):
                if img[i][j] < value: img[i][j] = 255
                else: img[i][j] = 0
    else:
        for i in range(len(img)):
            for j in range(len(img[i])):
                if img[i][j] > value: img[i][j] = 255
                else: img[i][j] = 0
    
    if blur != (1, 1):
        img = cv2.blur(img, blur)
    
    return img

def expand_to_rows(image: np.ndarray, full=False, value=200):  # -> np.ndarray
        """
        Args:
            image: An grayscale image as np.ndarray, which represents a mask.
        
        Returns:
            A np.ndarray of the edited image.
        """
        dimensions = image.shape
        imglen = dimensions[0]
        
        white_row = np.array([255 for k in range(dimensions[1])])
        black_row = np.array([0 for k in range(dimensions[1])])
        
        if not full: imglen = dimensions[0] / 2
        for i in range(int(imglen)):
            for j in range(dimensions[1]):
                if image[i][j] > value:
                    image[i] = white_row
        for i in range(int(imglen), dimensions[0]):
            for j in range(dimensions[1]):
                image[i] = black_row
        return image

def expand_to_columns(image: np.ndarray, full=False, value=200):  # -> np.ndarray
        """
        Args:
            image: An grayscale image as np.ndarray, which represents a mask.
        
        Returns:
            A np.ndarray of the edited image.
        """
        dimensions = image.shape
        imglen = dimensions[1]
        if not full: imglen = dimensions[1] / 2
        for i in range(int(imglen)):
            for j in range(dimensions[0]):
                if image[j][i] > value:
                    image[:,i] = [255 for k in range(dimensions[1])]
        for i in range(int(imglen), dimensions[1]):
            for j in range(dimensions[1]):
                image[j][i] = 0
        return image

class PlutoObject:
    def __init__(self, img: np.ndarray):
        self.img = img
        self.tesseract_path = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    
    def ocr(self, image=None):  # -> str
        """Preforms OCR on a given image, using ether Tesseract or EasyOCR
        
        Args:
            image: np.ndarray of the to be treated image.
        
        Returns:
            String with the raw result of the OCR library.
        
        """
        if image is None: image = self.img
        if self.tesseract_path == "": print("Pluto WARNING - Please check if tesseract_path has been set.")
        from pytesseract import pytesseract
        try:
            pytesseract.tesseract_cmd = self.tesseract_path
            text = pytesseract.image_to_string(image)
        except Exception as e:
            print("Pluto WARNING - Error while performing OCR: ", e)
            text = ""
        return text

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

    def extr_mask_img(self, mask: np.ndarray, img: np.ndarray, inverted=False):
        """Performs extend_to_rows() on the mask and returns the masked out parts of the original image.
        
        Args:
            mask: grayscale mask
            img: Original image
            inverted: if True, an inverted version of the output will also be returned
        
        Returns:
            A np.ndarray of the masked out part
        """
        mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
        
        extr = self.expand_to_rows(mask)
        
        # show_image(extr)
        
        out = []
        invout = []
        for i in range(len(extr)):
            if extr[i][0] > 200: out.append(img[i])
            elif inverted: invout.append(img[i])
        
        if inverted: return np.array(out), np.array(invout)
        return np.array(out)

class Twitter(PlutoObject):
    def __init__(self, img: np.ndarray):
        super().__init__(img)
    
    def dark_mode(self, img=None):  # -> bool
        """Checks if the screenshot has dark mode enabled
        
        Args:
            img: if the checked image should be different from the self.img, pass it here
        
        Returns:
            Is the screenshot in dark mode? True / False
        """
        testimg = self.img
        if img is not None: testimg = img.copy()
        top_row = avg_of_row(testimg, 0, True)
        bottom_row = avg_of_row(testimg, -1, True)
        left_collum = avg_of_collum(testimg, 0, True)
        right_collum = avg_of_collum(testimg, -1, True)
        final_value = sum([top_row, bottom_row, left_collum, right_collum]) / 4
        return final_value < 125
    
    def analyse(self):
        result = None
        if self.dark_mode(): result = self.dark()
        else: result = self.std()
        header, body = result
        # show_image(header)
        # show_image(body)
        return self.ocr_cleanup(self.ocr(header)), self.ocr_cleanup(self.ocr(body))
    
    def std(self, img=None, display=False):
        input_img = None
        if img is not None: input_img = img.copy()
        else: input_img = self.img.copy()
        if img is not None: self.img = img.copy()
        
        blur = trimm_and_blur(input_img, True, 30, (20, 20), [255, 255, 255])
        out = trimm_and_blur(blur, False, 250, (5, 5), [0, 0, 0])

        msk_inv = (255 - out[:,:,0])

        out_exptr = self.expand_to_rows(msk_inv, True)

        header_info = []
        continue_please = True
        cnt = 0
        for i in range(len(out_exptr)):
            if continue_please:
                if out_exptr[i][0] < 250: continue
            else:
                if out_exptr[i][0] < 250: break
            header_info.append(self.img[i])
            continue_please = False
            # print("hey!")
        cnt = i

        bottom = []
        lastone = False
        for i in range(cnt+1, len(out_exptr), 1):
            if out_exptr[i][0] < 250:
                if lastone:
                    bottom.append(self.img[3])
                    lastone = False
                continue
            bottom.append(self.img[i])
            lastone = True
        
        header_info = np.array(header_info)
        bottom = np.array(bottom)
        
        if display:
            show_image(header_info)
            show_image(bottom)
        
        return header_info, bottom
    
    def dark(self, img=None, display=False):
        """Segmentates the input screenshot (dark mode enabled) into header and body.
        
        Args:
            img: if the screenshot should be different from self.img, pass it here.
            display: True if output should be displayed before return
        
        Returns:
            The two segmentated areas.
        """
        input_img = None
        if img is not None: input_img = img.copy()
        else: input_img = self.img.copy()
        if img is not None: self.img = img.copy()
        
        blur = trimm_and_blur(input_img, False, 230, (20, 20),[0, 0, 0])
        out = trimm_and_blur(blur, True, 10, (5, 5),[255, 255, 255])

        msk = out[:,:,0]

        out_exptr = self.expand_to_rows(msk, True)

        header_info = []
        continue_please = True
        cnt = 0
        for i in range(len(out_exptr)):
            if continue_please < 3:
                if out_exptr[i][0] < 250:
                    if continue_please == 1: continue_please += 1
                    if continue_please == 2: header_info.append(self.img[i])
                    continue
            else:
                if out_exptr[i][0] < 250: break
            
            if continue_please == 0: continue_please += 1
            if continue_please == 2: break
            header_info.append(self.img[i])
        cnt = i

        bottom = []
        lastone = False
        for i in range(cnt+1, len(out_exptr), 1):
            if out_exptr[i][0] < 250:
                if lastone:
                    bottom.append(self.img[3])
                    lastone = False
                continue
            bottom.append(self.img[i])
            lastone = True
        
        header_info = np.array(header_info)
        bottom = np.array(bottom)
        
        if display:
            show_image(header_info)
            show_image(bottom)
        
        return header_info, bottom
    
    def black(self):
        pass

class FoxNews(PlutoObject):
    def __init__(self, img: np.ndarray):
        super().__init__(img)
    
    def analyse(self, display=False):
        og_shape = self.img.shape
        img = cv2.resize(self.img, (512, 512))
        black = np.zeros((512, 512))

        for i in range(len(black)):
            for j in range(len(black[0])):
                temp = img[i][j]
                if (temp == [34, 34, 34]).all(): black[i][j] = 255
        blured = cv2.blur(black, (20, 20))

        for i in range(len(blured)):
            for j in range(len(blured[0])):
                if blured[i][j] < 40: blured[i][j] = 0
                else: blured[i][j] = 255

        msk = self.expand_to_rows(blured)

        og_size_msk = cv2.resize(msk, (og_shape[1], og_shape[0]))
        
        top = []
        heading = []
        bottom = []

        top_part = True
        bottom_part = False

        for i in range(len(self.img)):
            if og_size_msk[i][0] > 1:
                heading.append(self.img[i])
                if top_part:
                    top_part = False
                    bottom_part = True
            elif top_part: top.append(self.img[i])
            else: bottom.append(self.img[i])

        heading = np.array(heading)
        bottom = np.array(bottom)
        top = np.array(top)
        
        if display:
            show_image(heading)
            show_image(bottom)
            show_image(top)

        ocr_result = self.ocr(heading)
        headline = self.ocr_cleanup(ocr_result)

        cat_info_img = []
        top_len = len(top)
        for i in range(top_len, 0, -1):
            if top[i-1][0][0] > 250: cat_info_img.insert(0, top[i-1])
            else: break

        cat_info_img = np.array(cat_info_img)
        print(cat_info_img.shape)
        if display: show_image(cat_info_img)

        ocr_result = self.ocr(cat_info_img)
        clean_ocr = self.ocr_cleanup(ocr_result)

        dotsplit = clean_ocr.split("-")[0][:-1].lstrip(" ")
        pubsplit = clean_ocr.split("Published")[1].lstrip(" ")
        
        subinfo_bottom = []

        stoper = False
        for row in bottom:
            subinfo_bottom.append(row)
            for pix in row:
                if pix[0] > 200 and pix[0] < 240 and pix[2] < 50 and pix[1] < 50:
                    stoper = True
                    break
            if stoper: break

        subinfo_bottom = np.array(subinfo_bottom[:-3])
        if display: show_image(subinfo_bottom)
        subinfo = self.ocr_cleanup(self.ocr(subinfo_bottom))

        subsplit = subinfo.split()

        author_list = []
        subtitle_list = []
        subinfo_switcher = True

        for w in reversed(subsplit):
            if w == "By" and subinfo_switcher:
                subinfo_switcher = False
                continue
            if w == "News" or w == "Fox" or w == "|": continue
            if subinfo_switcher: author_list.insert(0, w)
            else: subtitle_list.insert(0, w)

        author = " ".join(author_list)
        subtitle = " ".join(subtitle_list)
        
        jasoon = {  "source": "News Article",
                    "article": {
                        "created": "[Published] " + pubsplit,
                        "organisation": "Fox News",
                        "headline": headline,
                        "subtitle": subtitle,
                        "author": author,
                        "category": dotsplit
                    }
                }
        
        return self.to_json(jasoon)

class NYT(PlutoObject):
    def __init__(self, img: np.ndarray):
        super().__init__(img)
        self.header_img = None
    
    def header(self, img=None, non_header=False):
        """Isolates the headline from an article, based on color
        
        Args:
            img: if the used screenshot should differ from self.img, pass it here
            non_header: True if all other parts of the screenshot, that don't belong to the headline, \
                        should also be returned seperatly (basicly a inverted return of this method)
        
        Returns:
            An isolated part of the original screenshot, which only contains the headline\
            (optional also an inverted version, when non_header is True)
        """
        if img is None: img = self.img.copy()
        img_og = img.copy()
        
        img = cv2.resize(img, (255, 255))
        img = trimm_and_blur(img, False, 30, (15, 15), [255, 255, 255], True, [0, 0, 0])
        
        extr = expand_to_rows(img[:,:,0], True, 10)
        extr = cv2.resize(extr[:,:10], (10, img_og.shape[0]))
        
        out = []
        inverse_out = []
        
        for i in range(len(extr)):
            if extr[i][0] > 200: out.append(img_og[i])
            elif non_header: inverse_out.append(img_og[i])
        
        out = np.array(out)
        
        if non_header: return out, inverse_out
        return out

    def images(self, img=None, non_images=False): # -> np.ndarary | None
        """Isolates images of an article, based on color
        
        Args:
            img: if the used screenshot should differ from self.img, pass it here
            non_images: True if all other parts of the screenshot, that aren't partof an image, \
                        should also be returned seperatly (basicly a inverted return of this method)
        
        Returns:
            An isolated part of the original screenshot, which only contains the headline\
            (optional an inverted version as well, when non_images is True)
            If no images can be found, the return is None
        
        Please make sure that img is not scaled down and *not* grayscale
        """
        if img is None: img = self.img.copy()
        
        img_og = img.copy()
        img = cv2.resize(img, (50, img_og.shape[0]))
        
        image = []
        non_image = []
        
        j = 0
        stop = False
        
        for i in range(len(img)):
            stop = False
            while j < len(img[i]) and not stop:
                pix = img[i][j]
                minpix, maxpix = np.min(pix), np.max(pix)
                difference = maxpix - minpix
                if difference > 0:
                    image.append(img_og[i])
                    stop = True
                
                j += 1
            
            if not stop and non_images: non_image.append(img_og[i])
            j = 0
        
        image = np.array(image)
        if non_images: non_image = np.array(non_image)

        if len(image) < 1:
            image = None
            print("Pluto WARNING - At least one return from images() is empty.")
        
        if non_images: return image, non_image
        return image
    
    def suber(self, img=None):
        """Isolates the headline from an article, based on color
        
        Args:
            img: if the used screenshot should differ from self.img, pass it here
            non_header: True if all other parts of the screenshot, that don't belong to the headline, \
                        should also be returned seperatly (basicly a inverted return of this method)
        
        Returns:
            An isolated part of the original screenshot, which only contains the headline\
            (optional also an inverted version, when non_header is True)
        """
        if img is None: img = self.img.copy()
        img_og = img.copy()
        
        img = cv2.resize(img, (255, 255))
        img = trimm_and_blur(img, False, 55, (15, 15), [255, 255, 255], True, [0, 0, 0])
        
        extr = expand_to_rows(img[:,:,0], True, 10)
        extr = cv2.resize(extr[:,:10], (10, img_og.shape[0]))
        # show_image(extr)
        out = []
        
        for i in range(len(extr)):
            if extr[i][0] > 200: out.append(img_og[i])
        
        out = np.array(out)
        return out
    
    def analyse(self, img=None):
        analyse_img = img
        if analyse_img is None: analyse_img = self.img
        color_images, non_color = self.images(None, True)
        
        head, body = self.header(non_color, True)
        
        headline = self.ocr_cleanup(self.ocr(head))
        # print(headline)
        
        # show_image(head)
        # show_image(body)
        
        # print(type(body))
        subt = self.suber(np.array(body))
        subtitle = self.ocr_cleanup(self.ocr(subt))
        
        return headline, subtitle

class Facebook(PlutoObject):
    def __init__(self, img: np.ndarray):
        super().__init__(img)
        self.top = None
        self.body = None
        self.engagement = None
    
    def analyse(self, img=None, display=False): # -> tuple [str, str, str, str]
        """Main method for extracting information from a screenshot of a Facebook post.
        
        Args:
            img: If the used screenshot should differ from self.img, pass it here
            display: True for showing in-between steps
        
        Returns:
            The extracted information as a tuple of Strings
        """
        if img is None: img = self.img
        
        self.split(img)
        
        # t1 = time.time()
        top = to_grayscale(self.top)

        topname = top[:52,:]
        topdate = top[52:,:]
        
        if display:
            show_image(topname)
            show_image(topdate)
            show_image(self.middle)
        # t2 = time.time()
        # print("top name, date:", t2 - t1)
        # print(self.ocr(topname, True))
        # print(self.ocr(topdate, True))
        # show_image(self.middle)
        # show_image(self.bottom)
        # print(self.ocr(self.middle, True))
        # print("-------")
        # t1 = time.time()
        name = self.ocr_cleanup(self.ocr(topname))
        date = self.ocr_cleanup(self.ocr(topdate))
        
        body_text = self.ocr_cleanup(self.ocr(self.body))
        engagement_text = self.ocr_cleanup(self.ocr(self.engagement))
        # t2 = time.time()
        # print("ocr time:", t2 - t1)
        # bottomsting = self.ocr_cleanup(self.ocr(bottom))

        # print(name, date)
        # print(bottomsting)

        # print(self.characters_filter_strict(name, False), "|", self.characters_filter_strict(date))
        # print(self.characters_filter_strict(bottomsting))
        
        return name, date, body_text, engagement_text
    
    def dark_mode(self, img=None):
        if img is None: img = self.img
        dim = img.shape
        img = img[:int(dim[0]*0.1),:int(dim[0]*0.02),:]
        avg = np.average(img)
        return avg < 240

    def split(self, img=None, darkmode=None): # -> np.ndarray
        """Splits a Facebook Screenshot into a top part (thst's where the header is) and a 'bottom' part.
        
        Args:
            img: Alternative to the default self.img
        
        Returns:
            The top part and the bottom part, both as np.ndarray
        """
        if img is None: img = self.img
        og = img.copy()
        
        if darkmode is None: darkmode = self.dark_mode(img)
        # print(darkmode)
        
        if darkmode: gry = iso_grayscale(img, False, 50, True)
        else: gry = iso_grayscale(img, True, 250, True)

        gry_extr = expand_to_rows(gry, False, 100)
        
        top = []
        middle = []

        c = 0
        for i in range(len(gry_extr)):
            if gry_extr[i][0] > 100 and c < 2:
                if c == 0: c += 1
                top.append(og[i])
            elif c == 1: c += 1
            elif c == 2: middle.append(og[i])
        
        top = np.array(top)
        middle = np.array(middle)
        
        non_color = []
        for i in range(len(middle)):
            pix = middle[i][5] 
            if pix[0] > 250 or pix[1] > 250 or pix[2] > 250:
                non_color.append(middle[i])

        non_color = np.array(non_color)

        rgh = to_grayscale(non_color)

        rgh = rgh[:, int(non_color.shape[1] / 2):]
        rgh = iso_grayscale(rgh, True, 10, False, (25, 25))
        rgh = expand_to_rows(rgh, True, 5)
        
        body = []
        engagement = []
        for i in range(len(rgh)):
            if rgh[i][0] > 200: body.append(non_color[i])
            else: engagement.append(non_color[i])

        body = np.array(body)
        engagement = np.array(engagement)
        
        self.top = top
        self.body = body
        self.engagement = engagement
        
        return top, body, engagement
