"""
This example loads the tetra3 default database and solves for every image in the
tetra3/examples/data directory.
"""

import sys
sys.path.append('..')

from PIL import Image
from pathlib import Path
EXAMPLES_DIR = Path(__file__).parent

import tetra3
from tabulate import tabulate

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def plot_centroids_on_png(image_path, centroids, radius=5):
    """
    Plots circles highlighting detected centroids over the original PNG image,
    adjusting coordinates from top-left origin to bottom-left origin.

    Parameters:
    - image_path: str, path to the PNG image file
    - centroids: list of tuples, each tuple is (x, y) coordinate of a centroid
    - radius: int, radius of the circle to draw around each centroid
    """
    # Load the PNG image
    image = mpimg.imread(image_path)
    height = image.shape[0]

    # Create a plot
    fig, ax = plt.subplots()
    ax.imshow(image)

    # Transform and plot each centroid
    for idx, (y,x) in enumerate(centroids):
        circle = plt.Circle((x, y), radius, color='red', fill=False, linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, y, str(idx), color='yellow', fontsize=8, weight='bold')

    ax.set_title("Centroids Highlighted")
    plt.axis('off')
    plt.show()


# Create instance and load the default database, built for 30 to 10 degree field of view.
# Pass `load_database=None` to not load a database, or to load your own.
t3 = tetra3.Tetra3()

file_path = f"output_tetra3.txt"
# Clear output file
f = open(file_path, "w")
f.close()

# Path where images are
path = EXAMPLES_DIR / 'data'
for impath in path.glob('*'):
    print('Solving for image at: ' + str(impath))
    with Image.open(str(impath)) as img:
        # Here you can add e.g. `fov_estimate`/`fov_max_error` to improve speed or a
        # `distortion` range to search (default assumes undistorted image). There
        # are many optional returns, e.g. `return_matches` or `return_visual`. A core
        # aspect of the solution is centroiding (detecting the stars in the image).
        # You can use `return_images` to get a second return value to check the
        # centroiding process, the key `final_centroids` is especially useful.
        centroids = tetra3.get_centroids_from_image(img)
        # print("\n" + "=" * 60)
        # print(centroids)
        plot_centroids_on_png(impath, centroids, radius=5)

        solution = t3.solve_from_image(img, distortion=[-.2, .1])

    data = []
    for key, value in solution.items():
        # print(f"{key}: {value}")
        data.append([key, value])

    # print(tabulate(data, headers=['Variable', 'Result']))
    imgname = str(impath).split('\\')[-1]
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f'>>> Results for: {imgname} <<<\n\n')
        f.write(tabulate(data, headers=['Variable', 'Result']))
        f.write("\n\n" + "=" * 60)
        f.write("\n\n")
