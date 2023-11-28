#Img Processing Practice
import matplotlib.pyplot as plt
from PIL import Image
path = 'C:\\Users\\RyanSatterfield\\OneDrive - Guayaki SRP\\Documents\\Code\\Robot arm code Master file\\Test.jpeg'
# Load the image
img = Image.open(path).convert('L')  # Convert to grayscale

# Get pixel data
pixels = img.load()

# Lists to store x and y coordinates of black pixels
x_coords = []
y_coords = []
n = 0 
# Iterate through each pixel
for i in range(img.width):
    for j in range(img.height):
        # If the pixel is black (or close to black)
        if pixels[i, j] < 150:  # You can adjust the threshold if needed
            x_coords.append(i)
            y_coords.append(j)
            #print(str(i) + " , "+ str(j) +"\n")
            
    

# Create scatter plot
print(len(x_coords))
plt.scatter(x_coords, y_coords, color='black', s=0.05)  # s=1 makes each point very small
plt.gca().invert_yaxis()  # Invert y-axis to match image orientation
plt.show()
