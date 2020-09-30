1.  You need to run packaging.py script (Located in ‘scripts’ directory)
    to get a new zip that pack all you need to run the algorithm.

While running the script will ask you if you want to upgrade version and
you need to type ‘n’ for no or ‘y’ for yes (of course without the
apostrophes) <span dir="rtl"></span>if yes you will ask to enter h/m/l
for which

Place you want to change (h/m/l stands for high/middle/low), and now you
need to wait for roughly 4.5 minutes until the zip will be prepared.

Now were the zip will created determined by ‘packaging\_config.json’
file (which also located in ‘scripts’ directory), This file determines
for packaging.py where to find each file its needed and in addition it
also determines were to put the result zip,  
This configuration file look like this:

<img src="media/image1.png" style="width:6.33611in;height:2.54375in" />

When each row is of the form “key”: ”value” when key describes the
relevant property, and value is the value we want the algorithm to use.

*In particular*:  
“artifacts\_package\_file\_path” is were to put the result zip, and
which name we want to give him,
"../results/package\_artifacts/DieCluster"

Says that the zip would lie in folder ‘package\_artifacts’ and its name
will be DieCluster  
\[ In fact I add for the zip name a date and version\].

1.  Now extract all the files from the .zip into special directory (Its
    very important that all files will lie in same directory so the code
    will know were to find them),  
    now your directory should look like this:  
    <img src="media/image2.png" style="width:1.91181in;height:1.21597in" />

2.  A\) version.txt file contains the version of the package.

    B\) requirements.txt file contains all packages that aren’t python
    standard packages, which means, that if you try to run the code via
    command line or code editor you will need to install them, **But to run
    the .exe file you shouldn’t install anything**, In addition PyInstaller
    package, which we use in our code in the packaging process, Have
    problems with specific versions of some packages, If this happen you
    need to downgrade those packages, to know which packages  
    cause this you can find all my environment (my packages versions) in
    GitHub in issue 44  
    Here <https://github.com/Vayyar/ChipProduction/issues/44> .  
    And you can simply compare your environment to mine, to find packages
    that cause the problem, and then simply downgrade them.
      
    C) README.md is the same to the README from GitHub and contains
    explanations on the  
    project, and its purpose.
      
    **D) ‘neighbors\_table.json’ determines how many die neighbors need some
    chip to have so that the algorithm will declare on him as die.  
    And its looking like this:  
    {**
    
    **"0": 1,**

    **"1": 1,**
    
    **"2": 1,**
    
    **"3": 2,**
    
    **"4": 3,**
    
    **"5": 3,**
    
    **"6": 5,**
    
    **"7": 5,**
    
    **"8": 6**
    
    **}**

    **When each row is “a”: b when “a” is the number of neighbors, the chip
    have, and b is the threshold of the minimal number of die chips in it 8
    neighbor, we need to mark him as die.**
    
    **This file you must change to whatever you want to before applying the
    algorithm**.

    E\) ‘figures\_union\_template.html’ is skeleton file the algorithm uses
    for generating the .html file.
    
    **F) DieCludter.exe this is the application you simply need to double
    click on it to start the application, this will open a window which
    manage the algorithm.**

: APPLYING THE ALGORITHM:
=========================

1.  Don’t forget to update neighbors\_table.json file with the real
    threshold (See explanation In 3 D above).

2.  Now Double click on DieCluster.exe file to open a window, it should
    look like this:

<img src="media/image3.png" style="width:5.27906in;height:4.35139in" />

3.  Now all you need is to fill the relevant boxes with correct values
    and surprise surprise press on the “start” botton.

4.  So lets mark each box with identifier number just for clarity of the
    below explanation  
    <img src="media/image4.png" style="width:6.32778in;height:5.22431in" />

##### **Region 1: Here you should insert path for a directory were you want the program will put its results (If the path currently not exist, the program will create it).**

##### **Region 2: Here you should insert path for the json file that contains the threshold data as explained in 3 D above. If you rely on the json that attached with the zip, you don’t need to change here anything the default path is correct, (you need change it only if you rely on another json with different place or with different name).**

##### **Region 6: The input for the algorithm can be a single file, or a directory of wafers, or even directory that contains directories that contains wafers, and so on. (If the input is directory the algorithm will pass on all files in the directory in one run and will create also a summary excel). So if the input is full directory of wafers you should check this box, else (if it a single file) just remove it unchecked.**

##### **Region 4: If you leave box 6 unchecked, you may simply ignore this box (The program will ignore it), else just insert here the path of the directory that contains all the wafers Please pay attention that this directory should contains only wafers (or directories that contain directories that contain wafers and everything like that), and not anything else.**

##### **Region 3: If you leave box 6 checked you may ignore this box (The program will ignore it), else just insert here the path of the wafer file (it can be either .txt or .stdf file).**
 
##### **Region 5: For now it simply deed area (Historically It was responsible to rule if the screen will display only INFO or also DEBUG messages when running, but finally I change it so that always it will display also DEBUG messages, it very easy to change it back if you wish, or to delete this area, with small changes in main.py script).**

##### **Region 7: Finally, just click start to run.**

After successful run you need to see something like this:  
<img src="media/image5.png" style="width:6.49583in;height:3.44028in" />

The results lie where you told the program to put them in **region 1**

[**Here** example of how the program results should look
like](https://github.com/Vayyar/ChipProduction/tree/master/results_for_example/results_of_resources_Date_2020_09_29_20_51_09)

**And the html files should look likes**

<img src="media/image6.png" style="width:6.49583in;height:4.94375in" />

**Comments:**
-------------

1.  **Efficiency**: there are huge difference in running time between
    the program if we run it as .exe file, or as .py file by simply
    running main.py script, when the later is quicker in order of
    magnitude, so it may worth considering to run it through main.py
    (its also create a GUI window)  
    when there are huge amounts of wafers.

2.  **Efficiency**: The vast majority of the time (something like 97%)
    taken by the savefig method of matplotlib package (Used in
    HtmlViewer.py file in scripts directory), that saves the figures
    which latter I plant in the html file (I mean the wafer figures).

3.  When trying to make things parallel (In attempt to save time) the
    Gooey (which create the GUI window) get very crazy with problems
    that I find very hard to solve.

###
