import PIL
from PIL import Image
import random
import PIL.ImageDraw
import numpy
import time

class Rect():
    def __init__(self, width, height=None):
        if height == None: # Allows for easier squares
            height = width

        self.width = width
        self.height = height
        self.dim = (width, height)
        self.area = width*height
        self.colour = (
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255),
        )

def sort_by_area(rectangles):
    # QUICK SORT ALGORITHM
    if len(rectangles) <= 1: # Base case
        return rectangles
    
    pivot = rectangles[0]
    rectangles.pop(0)
    lesser = []
    greater = []

    for rect in rectangles:
        if rect.area < pivot.area:
            lesser.append(rect)
        else:
            greater.append(rect)

    return sort_by_area(greater) + [pivot] + sort_by_area(lesser)

def place_rect(rect:Rect, pos:tuple):
    print(f"placing {rect.dim} at {pos}")
    upleft = pos
    downright = (pos[0]+rect.width-1, pos[1]+rect.height-1)
    drawable.rectangle(
        [upleft, downright],
        fill=rect.colour
    )
    occupation[upleft[1]:downright[1]+1, upleft[0]:downright[0]+1] = True

def find_and_place(rect:Rect, occupation):
    for y in range(len(occupation)):
        for x in range(len(occupation[0])):

            if occupation[y,x] == True:
                continue

            # Potential place found, now needs to check if it will be on top of anything else
            fail = False
            downRight = (x+rect.width, y+rect.height)
            if downRight[0]-1>=len(occupation[0]) or downRight[1]-1>=len(occupation): # Rect hangs outside of the image in this pos
                fail = True
            for coverx in range(x, downRight[0]):
                if fail:
                    break
                for covery in range(y, downRight[1]):
                    if occupation[covery,coverx] == True:
                        fail = True
                        break
            if fail:
                #for i in range(rect.height):
                #    occupation = numpy.concatenate((occupation, numpy.full(shape=(1,SPACE[0]), fill_value=False)))
                #print(occupation)
                #find_and_place(rect, occupation)
                continue

            place_rect(rect, (x,y))
            return
    print(f"Failed to place {rect.dim}")

SPACE = (10,10)
rects = [
    Rect(2,1),
    Rect(1,1),
    Rect(5,3),
    Rect(6,1),
    Rect(1,5),
    Rect(5,5),
    Rect(2,2),
    Rect(2,2),
    Rect(2,2),
    Rect(4,4),
    Rect(1,2), # Seems to be overwriting the 1,1
    Rect(6,2)
]
occupation = numpy.full(shape=(SPACE[1], SPACE[0]), fill_value=False)
image = PIL.Image.new(mode="RGB", size=SPACE)
drawable = PIL.ImageDraw.ImageDraw(image)
rects = sort_by_area(rects) # Quick sort into descending order by area
i = 0
for rect in rects:
    find_and_place(rect, occupation)
    image.resize((SPACE[0]*100, SPACE[1]*100), resample=PIL.Image.NEAREST).save(f"{i}.png")
    i += 1
image.save("output.png")