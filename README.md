### Vertice
Quake III Map Boundary Analysis Tool
<br/>

Created by Jordy Veenstra (A Pixelated Point of View)<br/>
Licensed under MIT

<br/>

### Table of Contents

* [Background](#background)
* [Installation](#installation)
* [License](#license)

<br/>

### Background
*Vertice* is a Python algorithm that outputs `boundary data` found inside Quake III map files. It outputs the size of each map as X, Y, Z coordinates, finds every spawn point, and calculates the movement space the player/or the camera has before it enters the void. Furthermore, it outputs the coordinates of each spawn point inside a 3D plot for visual reference.

The algorithm was initially made as a helper tool to generate map and camera data for the *avant* algorithm, yet as a standalone application it might prove useful in certain situations as it can offer the following features:

* Calculate the size/scope of a map;
* Find out how many spawn points there are inside of a map;
* Tell you how close/far a spawn point is from the void;
* Present data as to how much the player (or in the case of `Q3MME`, the camera) can move before the void is entered;

<br/>

### Installation
Vertice can be installed in three different ways. The easiest way is to download the standalone `.exe` or `.app` files found inside the `Release` section of the repository.

Simply extract the files from the download, place your Quake III Arena maps inside the `input` folder and run the executable. Vertice is able to spot the difference between `.bsp` and `.pk3` files and can work with both of them. Vertice can also recognize multiple `.bsp` files inside a `.pk3` archive. Depending on the amount of maps and processing power of your computer, the time needed to generate the data may vary, but in most cases shouldn't take longer than a few seconds. Once completed, a pdf containing all of the data will be generated in the `output` folder for further use.

Another way to run vertice is by installing it as a PyPi package and run the algorithm by typing `vertice_run` in your terminal window.

The third and last way to use vertice is by cloning the repository and installing the dependencies. You need to make sure that you have a recent version of [Python](https://www.python.org/downloads/) installed (Preferably >= 3.8). You will need `pip` as well in order to download a number of required dependencies. If you download Python from the original Python Foundation Website, pip will automatically be installed. 

**If you are using the PyPi package, please follow this approach:**
* Verify your Python version and/or install/upgrade
* Install the PyPi package with `pip install vertice`
* Open a new terminal window, navigate to a directory of choice, for example your `Desktop` or `Documents`.
* Create two folders: `input` and `output` in that same directory.
* Plae your Quake III maps inside the input folder. Vertice supports 7zip, rar, and zip archives or bsp and pk3 files/archives. It does not matter if they are placed in the root of the input folder or in seperate folders, as long as they are within the `input` folder.
* Run the algorithm in your terminal by typing `vertice_run`.
* The algorithm should start and updates should be visible inside the terminal window.
* Once the message `...Done!` is visible, you can navigate to the `output` folder in order to find your PDF file.


**If you want to clone the repository, please follow this approach:**
* Verify your Python version and/or install/upgrade
* Open a new terminal window, navigate to a folder of choice
* Clone the repository with `git clone https://github.com/jiyorude/vertice.git` 
* (Optional) Switch to a virtual environment of choice with `venv` or other tool that has your personal preference
* Install all dependencies with `pip install -r requirements.txt`.
* Place your Quake III maps inside the `input` folder. Vertice supports 7zip, rar and zip archives, or .bsp and .pk3 files. It doesn't matter if they are placed in the root of the input folder or if the files are placed in seperate folders inside of the input folder.
* Inside your terminal window, navigate to the folder where you cloned the repository and navigate to `src/vertice`.
* Start the algorithm with `python vertice.py`.
* The algorithm should start and updates should be visible inside the terminal window.
* Once the message `...Done!` is visible, you can navigate to the `output` folder in order to find your PDF file.

<br/>

### License
Vertice is licensed under MIT. Please refer to `License.txt` for more information regarding usage.

&copy; Jordy Veenstra 2024<br/>
&copy; A Pixelated Point of View 2024