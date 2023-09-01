# Error Analysis and Local Geoid modelling



## Project Description

This a code to analyse errors in an observation using observation equation least square adjustment. This project also handles local geoid modelling for extracting the orthometric heights of terrain from GNSS ellipsoidal heights.

## Table of Contents

- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Contribution](#contribution)


## Installation

Follow these steps to set up and run the project:

1. Clone this repository:

      git clone https://github.com/martinaborgeh/Least-Square-Adjustment.git



2. Download and install Python and an IDE (e.g Pycharm or VS Code).

3. Open the cloned folder as your project directory.

4. Install the required dependencies:

pip install numpy, PyQt6,Sympy,matplotlib



## Dependencies

The project relies on the following dependencies:

- numpy
- PyQt6
- Sympy
- matplotlib



## Usage
### For Local Geoid
1. Specify the train and test input data in the read_data() method. the train and test sampple is found in the cloned directory 
2. Running will generate the local geoid model for converting ellipsoidal height to corresponding orthometric heights
### For Levelling Least Square Adjustment Geoid
1. Run the MainUiConnect.py file to run the application
2. Enter or import data from excel
3. select appropriate output requirement and compute
4. Export the Error Assessment and the Most probable Height to Excel.



<!-- You can add screenshots or GIFs here to demonstrate the usage -->

## Contribution

We welcome contributions to this project! If you'd like to get involved, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Open a pull request to merge your changes into the main branch.
