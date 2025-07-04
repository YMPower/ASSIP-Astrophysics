# ==============================================================================
#   Functions
# ------------------------------------------------------------------------------
# defines a function that allows the user to reduce the image to look at the small box surrounding the loop
def smallbox(img):
    # img is the average intensity full image
    # it returns the array of the small image defined by the box you chose

    import matplotlib.pyplot as plt
    import numpy as np

    """
    Parameters
    ----------
    img : array
        Array of average intensity values to be plotted and pull up an image.

   # Returns
  # box in 2 formats
    #"""
    # pulls up the original image
    plt.imshow(img, origin="lower", cmap="gray")  # lower case l
    # initializes a list for the points to be recorded
    smpts = []
    # initializes a number of points variable
    n_pts = 0
    # prompts the user to select points
    print(
        "Please select the lower left and upper right corners of your small box."
    )

    # loop through getting mouse click until two clicks are made
    while n_pts < 2:
        # gets the mouse coordinate
        mouse_coord = plt.ginput(timeout=-1)
        # adds coordiantes to list
        smpts.append(mouse_coord)
        # iterates
        n_pts += 1

    # pulls up the cropped image based on the mouse coordinates selected
    plt.figure()
    plt.imshow(img, origin="lower", cmap="gray")
    plt.xlim(smpts[0][0][0], smpts[1][0][0])
    plt.ylim(smpts[0][0][1], smpts[1][0][1])
    box = [smpts[0][0][1], smpts[0][0][0], smpts[1][0][1], smpts[1][0][0]]
    # print(box)
    b1 = np.int32(box)
    # print(b1)
    return b1, box


# ------------------------------------------------------------------------------


# need a function for getting the points (could we automate this)
def man_getpts():
    import matplotlib.pyplot as plt
    import keyboard

    # selecting the points around the loop
    # need to have the user be able to exit selecting points whenever they would like
    print("You will select the points around the loop. Click to begin.")

    # Waits for the mouse to be clicked to move on
    while True:
        # boolean for the status of a click
        click = plt.waitforbuttonpress()

        # checks if the mouse was clicked
        if click == False:
            break

    # provides instructions
    print(
        "Select all of your points. Left CLick adds point, Right removes the most recently added. When done, click the 'Enter' key or Center Mouse button."
    )
    # allows user to slect points until the d key is pushed

    while True:
        if keyboard.is_pressed("Enter") == True:
            break

        # adds the mouse click to the points list
    pts = plt.ginput(n=-1, timeout=120)  # *************
    # returns the list of points
    return pts


# -------------------------------------------------------------------------------


# defines a funtion to separate the x and y pixel coordinates*****
def get_x_y(pts):
    # gets the number of points in the given array
    import numpy as np

    n = len(pts)
    # initializes an array for the x and ycoordinates
    x = np.zeros(n)
    y = np.zeros(n)

    # run through all of the different points
    for i in range(0, n):
        # storing the x and y points
        x[i] = pts[i][0]
        y[i] = pts[i][1]
        # need to an mmwrite and mmread for these points after selection

    # need to round these values, so that the pixel coordinate can actually be used
    x = np.round(x)
    y = np.round(y)

    # need to become an integer type for the velocity calculation
    x = x.astype(int)
    y = y.astype(int)

    # returns x and y
    return x, y


# ------------------------------------------------------------------------------
# function for saving the x and y array of points selected to the computer and the box coordinates
# not sure where it stores them  now puts them in path that you send xcoord.txt and ycoord.txt
# def save_coord(x, y, box): #,xfile,yfile,boxfile)
def save_coord(path, x, y):
    # path has the form path='c:/Users/artpo/Desktop/'
    import numpy as np

    # using numpy's built in txt saving, so that the coordinates are not lost for multiple spectral lines
    np.savetxt(path + "xcoord.txt", x, delimiter=",")
    np.savetxt(path + "ycoord.txt", y, delimiter=",")
    # np.savetxt('box.txt',box, delimiter=',')
    return
    # np.savetxt('xcoord.txt', x, delimiter = ',')
    # np.savetxt('ycoord.txt', y, delimiter = ',')
    # np.savetxt('box.txt',box,delimiter=',')
    # puts them in folder where program is
    return


# -----------------------------------------------------------------------------
# function to load the points selected in
# def load_coord(xfile, yfile, box):  you give patg and names of x and y files
def load_coord(path, xfile, yfile):
    # x,y=load_coord(pathname, xfilename,yfilename)
    # don't put path in file name
    import numpy as np

    # using numpy's built in load txt function, so the coordinates can be read back in
    x = np.loadtxt(path + xfile)
    y = np.loadtxt(path + yfile)
    # box=np.loadtxt(box)
    # need to become an integer type for the velocity calculation
    x = x.astype(int)
    y = y.astype(int)
    # box=box.astype(int)
    return x, y
    # using numpy's built in load txt function, so the coordinates can be read back in
    # x = np.loadtxt(xfile)
    # y = np.loadtxt(yfile)
    # box=np.loadtxt(boxfile)
    # need to become an integer type for the velocity calculation
    # x = x.astype(int)
    # y = y.astype(int)
    # box=box.astype(int)
    return x, y


# -----------------------------------------------------------------------------
# defines a function to extract wavelengths and then calculate the velocity
def wave_vel(x, y, fitdata, wvl_lit, dwl):
    import numpy as np

    # x y are coordinates of points chosen
    # fitdata is result from eispac.fit_spectra(raster,tmplt,ncpu='max')
    # need to have applied the y shift before calling
    # dwl is the absolute wl shift calculated from Fe VIII

    # speed of light
    c = 3e5
    # the number of points selected to be used for extracting velocity at specific points
    nx = len(x)

    # gets the wavelength
    centroid = fitdata.fit["params"][:, :, 1]

    # initializes a correction arrays
    centroid_corr1 = np.zeros(centroid.shape)
    # loop to run through all of the wavelengths
    for n in range(centroid.shape[1]):
        # applies the correction
        centroid_corr1[:, n] = centroid[:, n] - dwl

    # calculates the velocity
    velocity = c * ((centroid - wvl_lit) / wvl_lit)

    # 26.520246725457337

    # reducing the velocity to the points selected
    vel_pts = []
    for i in range(0, nx):
        # gets the wavelength
        vel_pts.append(velocity[y[i], x[i]])

    return vel_pts


# ------------------------------------------------------------------------------
# defines a function the plots the velocity with the preset specifications
def plot_vel(vel, line_color, labelp):
    # color options r,g,b,c,m,y,k in quotes
    import matplotlib.pyplot as plt

    plt.figure(0)
    plt.grid(True)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.plot(
        vel,
        label=labelp,
        marker="o",
        markersize=10,
        color=line_color,
        linewidth=1,
    )
    plt.xlabel("Position", fontsize=50)
    plt.ylabel("Velocity (km/s)", fontsize=50)
    plt.legend(fontsize=40)
    return


# ------------------------------------------------------------------------------
# need a function for applying the yshift on to the second spectrometer
def yshift(wl, wl0, y0=0):
    # the result needs to be subtracted from previous measured y
    """
        Parameters
        ----------
        wl : FLOAT
            the wavelegnth of the current line where the shift should be applied
    x,y=    wl0 : FLOAT
            the base wavelength
        y0 : FLOAT
            the initial position

        Returns
        -------
        y : FLOAT
            the shift due to the spectrometer
    """

    # slope of the first(1) and second(2) detector
    m1 = 0.08718
    m2 = 0.076586
    # the wavelength that the jump occurs at
    wls = 220.0
    # the size of the jump between spectrometers
    ys = 11.649

    # the different cases that can exist for the yshift and the shirt to apply depending on the case
    if wl <= wls and wl0 < wls:
        y = m1 * (wl - wl0)
    elif wl >= wls and wl0 >= wls:
        y = m2 * (wl - wl0)
    elif wl >= wls and wl0 < wls:
        y = (m1 * (wls - wl0)) + (m2 * (wl - wls)) + ys
    elif wl <= wls and wl0 >= wls:
        y = (m1 * (wl - wls)) + (m2 * (wls - wl0)) - ys

    return y


# ------------------------------------------------------------------------------
# defines a function to test the conservation of mass equation
def com(v, p, a, x, y):
    import numpy as np

    """
    Parameters
    ----------
    v : array
        array of velocities going around the loop
    p : array
        array of densities going around the loop
    a : array
        array of cross-sectional area around the loop
    x: array
        x-coordinates along the loop
    y: array
        y-coordinates along the loop

    Returns
    -------
    c : float
        the value of the conservation of mass equation
    """

    # gets the length of all of the arrays
    n = len(v)

    c = np.zeros(n)
    # for loop to run through for the central difference method
    for i in range(1, n - 1):

        # calculates the ds based on the coordinates
        ds = np.sqrt((x[i + 1] - x[i - 1]) ** 2 + (y[i + 1] - y[i - 1]) ** 2)

        # calculates each step of the conservation of mass equation
        c1 = a[i] * p[i] * ((v[i + 1] - v[i - 1]) / (2 * ds))
        c2 = v[i] * p[i] * ((a[i + 1] - a[i - 1]) / (2 * ds))
        c3 = a[i] * v[i] * ((p[i + 1] - p[i - 1]) / (2 * ds))

        c[i] = c1 + c2 + c3

    return c


# ==============================================================================
def show1(intav, x_scale):
    # def show1(intav,x_scale):
    import matplotlib.pyplot as plt

    plt.imshow(intav, origin="lower", aspect=1.0 / x_scale)
    return


def show2(intav, x_scale):
    import matplotlib.pyplot as plt

    plt.imshow(intav, origin="lower", aspect=1.0 / x_scale, cmap="seismic")
    plt.colorbar(label="Velocity (km/s)")
    plt.title("Velocity Map")
    plt.xlabel("X Pixels")
    plt.ylabel("Y Pixels")
    plt.show()
    # =========
