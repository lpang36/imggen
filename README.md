# Imggen #

## Version 0.1 ##

A Python module to automatically generate images by overlaying foreground images on background images. Intended to facilitate training for computer vision algorithms. 

## Installation ##

Coming soon: 

    $ sudo pip install imggen

This package has dependencies: numpy, cv2 (also known as opencv-python), and tqdm. 

## Usage ##

To generate 10 images using default parameters: 

```python
import imggen as ig
ig.make(10)
```

Currently, the make function is the only function in the module. By default, foreground images are located in a folder named foreground, background images are located in a folder named background, and output images are saved to a folder named images and named sequentially. All three folders have the same parent directory as the invoking file. The output csv file containing bounding boxes is also located in the images folder and named data.csv by default. Note that this will overwrite any documents already contained in the folder with the same name. To modify these defaults, consult the documentation.

For foreground images, the best effect is achieved with a transparent background. If rotation is permitted, bounding boxes may be inaccurate. 

## Documentation ##

The make function has the following parameters:

* n
  * The number of images to be generated. This parameter is mandatory.

* foreground
  * The name of the folder to find foreground images. No slash is required. Defaults to 'foreground'.

* background
  * The name of the folder to find background images. No slash is required. Defaults to 'background'.

* out
  * The name of the folder to output images and data. No slash is required. Defaults to 'images'.

* data
  * The name of the file where bounding boxes will be stored. Defaults to 'data.csv'.

* filetype
  * The type of output files. Defaults to 'png'. Using a format other than png may cause loss in transparency.

* parameters
  * A dictionary containing various parameters, described below.

These keys are recognized by the parameters dictionary: 

* reshape
  * Boolean value for whether the foreground image can be resized. Defaults to True.

* maintain\_aspect
  * Boolean value for whether the aspect ratio of the image should be kept constant. Defaults to False. If this value is True, reshape range is taken from reshape\_x\_limits, and reshape\_y\_limits is ignored.

* reshape\_mode
  * Defines behaviour of reshape\_x\_limits and reshape\_y\_limits. If set to 'foreground', reshape\_x\_limits and reshape\_y\_limits will be a ratio relative to the size of the foreground image. If set to 'background', they will be a ratio relative to the size of the background image. If set to 'absolute', they will be absolute pixel size values. Defaults to 'foreground'.

* reshape\_x\_limits
  * Tuple in the format (lower\_bound, upper\_bound). Resizing of x dimension will be randomly chosen from between these values. Defaults to (0.25, 4).

* reshape\_y\_limits
  * Tuple in the format (lower\_bound, upper\_bound). Resizing of y dimension will be randomly chosen from between these values. Defaults to (0.25, 4).

* rotate
  * Boolean value for whether the foreground image can be rotated. Defaults to True.

* rotate\_limits
  * Tuple in the format (lower\_bound, upper\_bound). Angle of rotation in degrees will be randomly chosen from between these values. Defaults to (0, 360).

* rotate\_increment
  * Degree of rotation will be a multiple of this amount. Defaults to 90.

* flip
  * Boolean value for whether the foreground image can be flipped. Defaults to True.

* max\_foregrounds
  * The maximum number of foregrounds to be overlaid on the background. Defaults to 1.

* min\_foregrounds
  * The minimum number of foregrounds to be overlaid on the background. Defaults to 1.

* brightness
  * Boolean value for whether the brightness can be changed. Defaults to True.

* contrast
  * Boolean value for whether the contrast can be changed. Defaults to True.

* gain\_limits
  * Tuple in the format (lower\_bound, upper\_bound). Gain (a measure of change in contrast) will be randomly chosen from between these values. Defaults to (0.75, 1.25). 

* bias\_limits
  * Tuple in the format (lower\_bound, upper\_bound). Bias (a measure of change in brightness) will be randomly chosen from between these values. Defaults to (-10, 10).

* blur
  * Boolean value for whether the image can be blurred. Defaults to True.

* blur\_both
  * Boolean value for whether both background and foreground can be blurred. Defaults to False.

* blur_max
  * Maximum filter size of the blur, as a ratio of image size. Uses OpenCV's blur function. Defaults to 0.05.

* noise
  * Boolean value for whether salt-and-pepper noise can be applied to the foreground. Defaults to True.

* noise\_both
  * Boolean value for whether both background and foreground can be noised. Defaults to False.

* prob
  * Probability of a pixel in the image being noised. Defaults to 0.1.

* target\_size
  * Tuple containing fixed output size of image, in the format (x, y), or None. If None, output image size will vary. Defaults to None.

The output csv file is in the following format (headers not actually present): 

| Index | Background image name | Foreground image 1 | Foreground image 2 | ... |
| --- | --- | --- | --- | --- |
| 0 | background1.jpg | \[person.png, 5, 10, 245, 238\] | \[goose.png, 23, 75, 57, 21\] | ... |

In general, a foreground image cell will contain a list in the format \[image\_name, x\_offset, y\_offset, width, height\].
