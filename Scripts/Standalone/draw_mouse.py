import pyautogui
import time
import cv2
import numpy as np
import keyboard

# --- WARNING ---
# This code is a
# CONCEPT. It will be
# VERY SLOW and
# JUMPY.
# --- WARNING ---

# --- Failsafe ---
pyautogui.PAUSE = 0.001 # Make it fast, but risky
pyautogui.FAILSAFE = True

# --- Get Coordinates (Steps 1 & 2) ---
image = cv2.imread('image.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
canny_edges = cv2.Canny(blurred, 50, 150)
coordinates = np.column_stack(np.where(canny_edges > 0))

# Give yourself 5 seconds to switch to MS Paint
print("Switch to your drawing program (e.g., MS Paint)...")
time.sleep(5)

# --- Draw (Step 3) ---
print("Drawing...")

# Offset: Where on the screen to start drawing
start_x = 300
start_y = 300

# Go to the first point
# Note: OpenCV's (y, x) is (row, col)
# PyAutoGUI's (x, y) is (col, row)
first_point = coordinates[0]
pyautogui.moveTo(first_point[1] + start_x, first_point[0] + start_y)

# Loop through all other points
for point in coordinates:

    if keyboard.is_pressed('q'):
        print("Stop key pressed! Exiting.")
        break # Exit the loop

    # `point[1]` is X (column)
    # `point[0]` is Y (row)
    x = point[1] + start_x
    y = point[0] + start_y
    
    # Drag to the next point
    pyautogui.dragTo(x, y, duration=0.0)

    # Check again in case it's a long loop
    if keyboard.is_pressed('q'):
        print("Stop key pressed! Exiting.")
        break

print("Done!")