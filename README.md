# Augmented-Reality-With-OpenCV
This project demonstrates the implementation of Augmented Reality (AR) using OpenCV and ArUco markers for image transformation and overlay. The goal is to detect ArUco markers in a live image and apply a perspective transformation to overlay another image (such as a display or graphical content) onto the detected marker.
<br>
1. ArUco Marker Detection: Using OpenCV's ArUco library to identify and locate predefined markers in an image.
2. Perspective Transformation: Applying a homography transformation to overlay the display image onto the detected marker, making it appear as if it's part of the real-world scene.
3. Image Masking: Generating binary masks to isolate specific areas of the transformed image for blending with the source image.
4. Augmented Reality Visualization: Combining the original image with the transformed content to create a realistic AR effect.
