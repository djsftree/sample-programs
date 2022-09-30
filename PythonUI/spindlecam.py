from tkinter import *
import cv2
import sys
import getopt
import PIL.Image as Image, PIL.ImageTk as ImageTk

# import numpy as np #Needed for HoughCircles circle detection

# args, sources = getopt.getopt(sys.argv[1:], '', 'shotdir=')
# args = dict(args)
# if len(sources) == 0:
# sources = [ 0 ]

root = Tk()

width = 320
height = 240

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

_, frame = cap.read()
frameo = frame.copy()  # save old frame initially
frameo = cv2.min(frameo, frame)

# height, width, channels = frameo.shape
# print height, width, channels

img = Image.fromarray(frame)
imgtk = ImageTk.PhotoImage(image=img)

w = Label(root)
w.pack()


def TrailsToggle():
    global TrailsFlag
    TrailsFlag = not TrailsFlag


TrailsButton = Button(root, text="Trails", command=TrailsToggle)
TrailsButton.pack()

quitButton = Button(root, text="Quit", command=root.quit)
quitButton.pack()

X = int(width / 2)
Y = int(height / 2)


def LeftKey(event):
    global X
    X -= 1
    if X < 0:
        X = 0


def RightKey(event):
    global X
    X += 1
    if X > 319:
        X = 319


def UpKey(event):
    global Y
    Y -= 1
    if Y < 0:
        Y = 0


def DownKey(event):
    global Y
    Y += 1
    if Y > 239:
        Y = 239


root.bind("<Left>", LeftKey)
root.bind("<Right>", RightKey)
root.bind("<Up>", UpKey)
root.bind("<Down>", DownKey)
root.title("Spindle Camera 0.1")

TrailsFlag = 1


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step


def show_frame():
    global frameo, frame
    global cap
    global crosshair
    global X, Y

    _, frame = cap.read()

    # Flip as necessary
    # frame = cv2.flip(frame, 0)

    if TrailsFlag == 1:
        # Make trails
        frameo = cv2.min(frameo, frame)
    else:
        # Show live video
        frameo = frame

    # Circle detection needs some major work because all dots are analyzed which slows down analysis as dotted trails are made.
    # circles = cv2.HoughCircles(cv2.cvtColor(frameo,cv2.COLOR_BGR2GRAY), cv2.cv.CV_HOUGH_GRADIENT, 1, 1,param1=50,param2=30,minRadius=45,maxRadius=300)
    # if circles is not None:
    # circles = np.uint16(np.around(circles))
    # for i in circles[0,:4]:
    ## draw the outer circle
    # cv2.circle(displayframe,(i[0],i[1]),i[2],(0,255,0),2)
    ## draw the center of the circle
    # cv2.circle(displayframe,(i[0],i[1]),2,(0,0,255),3)

    # save frame for final display modifications
    displayframe = frameo.copy()

    # Draw target circles
    for radius in my_range(25, 200, 25):
        cv2.circle(displayframe, (X, Y), radius, (0, 0, 255), 1)

    # draw vertical line
    cv2.line(displayframe, (X, 0), (X, height), (0, 0, 255), 1)
    # draw horizontal line
    cv2.line(displayframe, (0, Y), (width, Y), (0, 0, 255), 1)

    # Convert colors as necessary for display
    displayframe = cv2.cvtColor(displayframe, cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(displayframe)
    imgtk = ImageTk.PhotoImage(image=img)
    w.imgtk = imgtk
    w.configure(image=imgtk)

    w.after(1, show_frame)


show_frame()

root.mainloop()
