Image Processing Overiew
------------------------
> ### Format
> 1. __Step Name__  
> 2. **Output**

### Steps
1. Take Picture
    - Image
2. Separate Green Colors
    - Image With Only Green Pixels
3. Threshold Itensity
    - Image With Only Bright Green Pixels
4. Edge Detect
    - Set of Points at Edges
5. Find Lines
    - Set of Acceptable Lines (Degrees and Position)
6. Create Shapes
    - Set of Corner Points of Acceptably Sied Rectangles
7. Find Pixels Then Angle Between Points of Interest
    - Distance
8. Output


Task and Corresponding Python Function
--------------------------------------
#### Python Libraries Used
> 1. OpenCV -> cv2
>  2. Numpy -> np  

Task | OpenCV/Python Function | What Function Returns
-----| ---------------------- | -----------------------
Open Image | `cv2.imread(filename)`   | Returns a value
Save Image | `cv2.imwrite(filename, image to be saved)` | Writes image to Image
Convert to Different Color Spaces | `cv2.cvtColor(input_image, output_image, colorSpace)` | Array of transformed Color Values
Display Image | `cv2.imshow(windowname, image)` | Window with displayed image ( *WaitKey() Necessary to actually display something* ) 
Tell Python to Display Image For Quantity of Time | `cv2.WaitKey(Number of milliseconds)` | Keeps window on screen
Color Upper Limit | np.array([value1, value2, value3]) | Array of color values
Color Lower Limit | np.array([value1, value2, value3]) | Array of color values
Color Filter "Mask" | `cv2.inRange(input_array, lower_limit, upper_limit)` | A new array with 1(ture) or 0(false) values determining if original color value lies within limits
Filter Original Image | `cv2.bitwise__and(input_array1, input_array2, mask=mask_array)` | Array of Color Values that are filtered and can be displayed to produce an image
