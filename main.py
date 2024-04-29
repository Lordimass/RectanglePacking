import PIL
from PIL import Image
import random
import PIL.ImageDraw
import numpy

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
    print(occupation)

def find_and_place(rect:Rect, occupation):
    temp_occupation = occupation.copy()
    numpy.append(temp_occupation, numpy.full(shape=len(occupation[0]), fill_value=False)) # Dynamic image height
    extra_used = False

    placed = False
    for y in range(len(temp_occupation)):
        if y > len(temp_occupation[0])-1:
            extra_used = True
        if placed:
            break
        for x in range(len(temp_occupation)):
            if temp_occupation[y,x] == True:
                continue

            fail = False
            downRight = (x+rect.width+1, y+rect.height+1)
            if downRight[0] > len(temp_occupation[0]) or downRight[1]>len(temp_occupation): # Rect hangs outside of the image in this pos
                continue
            for coverx in range(x, downRight[0]):
                if fail:
                    continue
                for covery in range(y, downRight[1]):
                    if temp_occupation[covery,coverx] == True:
                        fail = True
                        continue
            place_rect(rect, (x,y))
            placed = True
            break

    if not extra_used:
        occupation = temp_occupation[:len(occupation)]
        return
    
    rows = numpy.array()
    for row in temp_occupation:
        keep = False
        for value in row:
            if value == True:
                keep = True
                numpy.append(rows, row)
                continue
        if not keep:
            break
    occupation = numpy.concatenate(occupation, rows) 
    return
 
SPACE = (10,10)
rects = [
    Rect(2,1),
    Rect(1,1),
    Rect(5,3),
    Rect(6,1),
    Rect(1,5),
    Rect(5,5),
    Rect(2,2),
    Rect(6,5),
    Rect(5,7)
]
occupation = numpy.full(shape=SPACE, fill_value=False)
image = PIL.Image.new(mode="RGB", size=SPACE)
drawable = PIL.ImageDraw.ImageDraw(image)
rects = sort_by_area(rects) # Quick sort into descending order by area
for rect in rects:
    find_and_place(rect, occupation)
image.save("output.png")