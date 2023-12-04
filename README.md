# LAT - Leverage Analysis Tool

LAT is an analyzing tool for gaining understanding if and how leveraged instruments
can be used to build an investment portfolio that matches ones preferences. The tool is still under construction.

![Screenshot sample of the application](/images/sample-Kivy.png)

### Background

Development of this application was started after a series increasingly more realistic models. Experiment with the previous model resulted in a whitepaper, concluding that leveraged instruments could increase the expected returns of a portfolio. This application will enable non-programmes to experiment with leveraged certificates, and allow for different strategies of buying and selling the certificates in order to minimize risk or to increase returns.

<kbd>
<img src="/images/Leveraged_Certificates.png" alt="Whitepaper first page" width="50%"/>
</kbd>

### How to run

Run the application by executing the Makefile

```
make
```

This compiles the C++ files, and then runs the program.

*NOTE*: The program does not work with Windows currently, and Mac only can run with C++ version 11.

### Required libraries

Beyond Python3 standard libraries this program also requires:

* numpy
* matplotlib
* kivy
* kivymd
* simplejson

and c++ compilator

* g++

run `sudo make install` all needed requirements,
or `pip install -r requirements.txt` to install all pip requirements without sudo. 

### Project structure
For getting an undestanding of this code you are recomended to start with leverage_analysis_tool.py, and then Model.py and View.py.

### Walkthrough

To get started select a market by clicking on a row with a market in the bottom left table. The leverage is selected by the column number of your click.

To the top left are widgits to change input parameters and strategy. And in the middle is a histogram which displays the distribution of outcomes of the portfolio when investing for a selected amount of years (default is one year). There is also a graph showing the performance from the start date to the end date, which can be specefied benath the graph.

Metrics of the portfolios performance is displayed on the righten side of the application.

### Data

Data files are not included due to copyright uncertainties but can be downloaded online, for example at

* https://www.kaggle.com/

The data should be stored as csv files and need to have a specific format, this is checked in the beginning of the program.

Filename: *Index* *Country*.csv \
First row: Date, Close, Open \
Following rows: *Date value*, *Close value*, *Open value*

e.g.

SP500 USA.csv

```
Date,Close,Open
20220103,3,2
20220102,2,1
20220101,1,0
```

The file path is set in *src/model/common/constants_model.py*

### Disclaimer

Historical returns are no guarantee of future returns. An investment in securities or funds can both increase and decrease in value, and you may not get the invested capital back.

### Goal & Journey

The project started out buy geting the logic in place and making a proof of consept, by using Tkinter as the GUI toolkit. But the goal was all along to change graphical toolkit to something more pleasing, if I managed to get that far without dropping the project.

![Image of the applicatioin when using Tkinter](/images/sample-Tkinter.png)

This phase is now past and the program is now built by using Kivy (https://kivy.org/). At the start of the project I wanted to achieve something in the following style. And it is still my northern star, though Kivy adds a few struggels in dark mode.

![Image of design goal](/images/Goal.jpeg)


The aim is to make a tool for both beginner and experts where there are two display options. One simplistic with only the most important features and values viewable. And one with all controls and all statistical performance meters.
