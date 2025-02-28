import os

dyrectory = '/Users/arkadij/PycharmProjects/PygameProject/data/Meteors'
images = os.listdir(dyrectory)
for image in images:
    print(image)