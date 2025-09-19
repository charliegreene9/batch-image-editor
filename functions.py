import glob

from PIL import Image


def rotater(
    file_path, theta: float, batch: bool, prefix: str = "", suffix: str = ""
):
    def img_rotate(path, angle):
        img = Image.open(path)
        img = img.rotate(angle)
        img.save(path)

    if batch:
        file_list = glob.glob(file_path + "\*.*")
        print("**********", file_list)
        for file in file_list:
            img_rotate(file, theta)
    else:
        img_rotate(file_path, theta)


# # Testing functions
# rotater(os.path.join(os.getcwd(), "test_images"), 90, True)
