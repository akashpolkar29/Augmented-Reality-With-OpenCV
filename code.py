import cv2
import matplotlib.pyplot as plt
import numpy as np
import cv2.aruco as aruco
s
### Read images ###
img_path = r"E:\Projects\CV\Task1\Images\20221115_113340.jpg" 
display_img_path = r"E:\Projects\CV\Task1\Images\cov.jpg" 
image = cv2.imread(img_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
display_image = cv2.imread(display_img_path)
display_image = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)  

### Detecting and reading ArUco markers ###
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters()
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)

### Only corner points are useful (getting them in readable format) ###
corner = np.reshape(corners,(-1))
corner = corner.astype(int)  

### Defining original image points and perspective transformation points ###
(x, y) = (850, 440)  
# Defining four corner coordinates of the display image for perspective transformation
(tr, tl, br, bl) = ([0+x, 0+y], [display_image.shape[1]-x, 0+y], 
                    [display_image.shape[1]-x, display_image.shape[0]-y], [0+x, display_image.shape[0]-y])

display_img_corner_pts = np.float32([tr, tl, br, bl])  
perspective_shifted_pts = np.float32([[corner[0], corner[1]], [corner[2], corner[3]], 
                                      [corner[4], corner[5]], [corner[6], corner[7]]])

### Perspective transform of display image ###
matrix = cv2.getPerspectiveTransform(display_img_corner_pts, perspective_shifted_pts)
print("Perspective Transform Matrix:\n", matrix)

# Apply the perspective transformation to the display image ###
transformed_image = cv2.warpPerspective(display_image, matrix, (image.shape[1], image.shape[0])) 
print("Transformed Image Shape:", transformed_image.shape)

### x Perspective transform of display image x ###
# ### Masking ###
''' 
Bitwise_and -> Retains white (mask) values from original image; fills the rest with (0,0,0)
Bitwise_or -> Retains everything except the white (mask); fills the rest with (255,255,255) 
'''

#### New mask ###
mask1 = np.zeros_like(image, dtype=np.uint8)
mask1[:,:] = (255,255,255)

# Split the transformed image into BGR channels
b, g, r = cv2.split(transformed_image)
# Create separate masks for each channel (red, green, blue)
mask_r = np.zeros_like(r)
mask_r[r != 0] = 255
mask_g = np.zeros_like(g)
mask_g[g != 0] = 255
mask_b = np.zeros_like(b)
mask_b[b != 0] = 255 

# Merge the individual masks back into a single mask
mask = cv2.merge((mask_b, mask_g, mask_r))
mask = np.ones_like(mask) * 255 - mask  # Invert the mask

# Define the vertices of the ArUco marker corners
vertices1 = np.int32([[corner[0], corner[1]], [corner[2], corner[3]], [corner[4], corner[5]], [corner[6], corner[7]]])
# Apply bitwise_and to retain only the regions of the original image where the mask has nonzero values
masked_image1 = cv2.bitwise_and(image, mask) 

# Add the masked original image and transformed image
add_image = cv2.add(masked_image1, transformed_image)

# Show the final result
plt.imshow(add_image)
plt.axis('off')  
plt.show()
