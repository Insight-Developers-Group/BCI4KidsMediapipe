# Instructions for how to install and run InSight for the first time on a Windows machine.

1. Clone the Github repository to your local machine. 

2. Download [Python version 3.7.7](https://www.python.org/downloads/release/python-377/). When prompted during installation select "Add Python 3.7 to PATH".

3. Ensure that pip was installed by typing `$ pip --version` into your command prompt. Pip should have been installed with the Python 3.7.7 installation. 

4. Upgrade pip wheels by typing `$ pip install --upgrade pip setuptools wheels` into your command prompt (This is necessary for installing MediaPipe using pip). 

5. Install backend dependencies by typing the following commands into your command prompt:
* `$ pip install numpy==1.19.5`
* `$ pip install websockets==10.1`
* `$ pip install pandas==1.3.5`
* `$ pip install pillow==9.0.0`
* `$ pip install tensorflow==2.4.1`
* `$ pip install mediapipe==0.8.9.1`
* `$ pip install opencv-python==4.5.5.64`
* `$ pip install scikit-learn==0.20.3`

6. For the frontend, InSight makes use of the node package manager to install and maintain all necessary dependencies. Ensure that node.js has been downloaded on your local device by running the command `npm -v`. If it has not been installed, you can get node.js [here](https://nodejs.org/en/download/).

7. To install all required dependencies, navigate to the folder `BCI4KidsMediapipe/Frontend/insight` and execute the command `npm install`.

8. Run frontend by opening a command prompt to the folder `BCI4KidsMediapipe/Frontend/insight` and executing the command `npm start`. The website will now be running locally and can be found at `localhost:3000` in your web browser of choice.

9. Run backend by opening a command prompt in the `BCI4Kidz\Python_Backend` folder and typing `python MainRunner.py` into the command prompt. Note that you will see a TensorFlow dlerror, this error can be ignored as we have not set up TensorFlow to run using the GPU.


