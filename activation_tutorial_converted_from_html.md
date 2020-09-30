

<div class="WordSection1">

<div style="border-top-color: initial; border-top-style: none; border-top-width: initial; border-right-color: initial; border-right-style: none; border-right-width: initial; border-bottom-color: windowtext; border-bottom-style: solid; border-bottom-width: 1pt; border-left-color: initial; border-left-style: none; border-left-width: initial; padding-top: 0in; padding-right: 0in; padding-bottom: 1pt; padding-left: 0in;">

<p class="MsoNoSpacing" style="border-top-color: initial; border-top-style: none; border-top-width: initial; border-right-color: initial; border-right-style: none; border-right-width: initial; border-bottom-color: initial; border-bottom-style: none; border-bottom-width: initial; border-left-color: initial; border-left-style: none; border-left-width: initial; padding-top: 0in; padding-right: 0in; padding-bottom: 0in; padding-left: 0in;"><o:p>&nbsp;</o:p></p>

</div>

<p class="MsoNoSpacing"><o:p>&nbsp;</o:p></p>

<div style="border-top-color: initial; border-top-style: none; border-top-width: initial; border-right-color: initial; border-right-style: none; border-right-width: initial; border-bottom-color: windowtext; border-bottom-style: solid; border-bottom-width: 1pt; border-left-color: initial; border-left-style: none; border-left-width: initial; padding-top: 0in; padding-right: 0in; padding-bottom: 1pt; padding-left: 0in;">

<p class="MsoTitle" style="border-top-color: initial; border-top-style: none; border-top-width: initial; border-right-color: initial; border-right-style: none; border-right-width: initial; border-bottom-color: initial; border-bottom-style: none; border-bottom-width: initial; border-left-color: initial; border-left-style: none; border-left-width: initial; padding-top: 0in; padding-right: 0in; padding-bottom: 0in; padding-left: 0in;">Chip Production<span dir="RTL"></span><span dir="RTL" style="font-family: &quot;Times New Roman&quot;, serif;"><span dir="RTL"></span>
</span>activation tutorial</p>

</div>

<p class="MsoNormal"><o:p>&nbsp;</o:p></p>

<p class="MsoListParagraphCxSpFirst" style="text-indent: -0.25in;"><span style=""><span style="">1)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span>You need to run packaging.py
script (Located in ‘scripts’ directory) to get a new zip that pack all you need
to run the algorithm.</p>

<p class="MsoListParagraphCxSpMiddle">While running the script will ask you if
you want to upgrade version and you need to type ‘n’ for no or ‘y’ for yes (of
course without the apostrophes)<span dir="RTL"></span><span dir="RTL" style="font-family: &quot;Arial&quot;, sans-serif;"><span dir="RTL"></span> </span>if yes you will
ask to enter h/m/l for which </p>

<p class="MsoListParagraphCxSpMiddle">Place you want to change (h/m/l stands for
high/middle/low), and now you need to wait for roughly 4.5 minutes until the
zip will be prepared.</p>

<p class="MsoListParagraphCxSpMiddle">Now were the zip will created determined by
‘packaging_config.json’ file (which also located in ‘scripts’ directory), This
file determines for packaging.py where to find each file its needed and in
addition it also determines were to put the result zip,<br>
This configuration file look like this:</p>

<p class="MsoListParagraphCxSpMiddle"><span style=""><img width="608" height="244" src="activation_tutorial_files/image002.jpg" v:shapes="Picture_x0020_2"></span></p>

<p class="MsoListParagraphCxSpMiddle">When each row is of the form <span style="color: rgb(0, 176, 240);">“key”<span class="GramE">: ”value</span>” </span>when key
describes the relevant property, and value is the value we want the algorithm
to use.</p>

<p class="MsoListParagraphCxSpMiddle"><span class="Heading4Char">In particular</span>:<br>
“artifacts_package_file_path” is <span class="SpellE">were</span> to put the <span class="GramE">result<span style="">&nbsp; </span>zip</span>, and which
name we want to give him,<span style="">&nbsp; </span><span style="font-size: 13.5pt; line-height: 107%; font-family: Consolas; color: rgb(106, 135, 89);">"../results/package_artifacts/DieCluster"
</span><span style="font-size: 12pt; line-height: 107%; font-family: Consolas; color: black;"><o:p></o:p></span></p>

<p class="MsoListParagraphCxSpMiddle"><span style="color: black;">Says that the zip would lie in folder ‘package_artifacts’ and its name
will be DieCluster<br>
[ In fact I add for the zip name a date and version].<o:p></o:p></span></p>

<p class="MsoListParagraphCxSpMiddle"><o:p>&nbsp;</o:p></p>

<p class="MsoListParagraphCxSpMiddle" style="text-indent: -0.25in;"><span style=""><span style="">2)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span>Now extract all the files
from the .zip into special directory (Its very important that all files will
lie in same directory so the code will know <span class="SpellE">were</span> to
find them),<br>
now your directory should look like this:<br>
<span style=""><img width="183" height="117" src="activation_tutorial_files/image004.jpg" v:shapes="Picture_x0020_3"></span></p>

<p class="MsoListParagraphCxSpMiddle" style="text-indent: -0.25in;"><span style=""><span style="">3)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span>A) version.txt file
contains the version of the package.</p>

<p class="MsoListParagraphCxSpMiddle"><span style="">B)
requirements.txt file contains all packages that aren’t python standard
packages, which<span style="">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </span>means, that
if you try to run the code via command line or code editor you will need to
install them, </span><b style="">But to run the .exe
file you shouldn’t install anything</b><span style="">,
In addition PyInstaller package, which we use in our code in the packaging
process, Have problems with specific versions of some packages, If this happen
you need to downgrade those packages, to know which packages <br>
cause this you can find all my environment (my packages versions) in GitHub in
issue 44<br>
Here </span><a href="https://github.com/Vayyar/ChipProduction/issues/44">https://github.com/Vayyar/ChipProduction/issues/44</a>
.<br>
And you can simply compare your environment to mine, to find packages that
cause the problem, and then simply downgrade them.<span style=""> <br>
C) README.md is the same to the README from GitHub and contains explanations on
the <br>
project, and its purpose.<br>
</span><b style="">D) ‘neighbors_table.json’
determines how many die neighbors need some chip to have so that the algorithm
will declare on him as die.<br>
And <span class="SpellE">its</span> looking like this:<br>
<span style="background-color: darkgray; background-image: initial;">{<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;"><span style="">&nbsp; </span>"0": 1,<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;"><span style="">&nbsp; </span>"1": 1,<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;"><span style="">&nbsp; </span>"2": 1,<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;"><span style="">&nbsp; </span>"3": 2,<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;"><span style="">&nbsp; </span>"4": 3,<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;"><span style="">&nbsp; </span>"5": 3,<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;"><span style="">&nbsp; </span>"6": 5,<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;"><span style="">&nbsp; </span>"7": 5,<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;"><span style="">&nbsp; </span>"8": 6<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="background-color: darkgray; background-image: initial;">}<span style="display: none;"> Hu</span></span><o:p></o:p></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><o:p>&nbsp;</o:p></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style="">When
each row is “a”: b when “a” is the number of neighbors, the chip have, and b is
the threshold<span style="">&nbsp; </span>of the minimal number of
die chips in it 8 neighbor, we need to mark him as die.<o:p></o:p></b></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="font-size: 14pt; line-height: 107%; color: red;">This file you must change
to whatever you want to before applying the algorithm</span></b><span style="color: red;">.<o:p></o:p></span></p>

<p class="MsoListParagraphCxSpMiddle"><span style="">E)
‘figures_union_template.html’ is skeleton file the algorithm uses for
generating the .html file.<o:p></o:p></span></p>

<p class="MsoListParagraphCxSpMiddle"><b style=""><span style="font-size: 13pt; line-height: 107%; color: red;">F) DieCludter.exe this is
the application you simply need to double click on it to start the application,
this will open a window which manage the algorithm.<o:p></o:p></span></b></p>

<p class="MsoListParagraphCxSpLast"><b style=""><span style="font-size: 13pt; line-height: 107%; color: red;"><o:p>&nbsp;</o:p></span></b></p>

<h1 align="center" style="text-align: center;">: APPLYING THE ALGORITHM:</h1>

<p class="MsoNormal"><o:p>&nbsp;</o:p></p>

<p class="MsoListParagraphCxSpFirst" style="text-indent: -0.25in;"><span style=""><span style="">1)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span>Don’t forget to update
neighbors_table.json file with the real threshold (See explanation <span class="GramE">In</span> 3 D above).</p>

<p class="MsoListParagraphCxSpMiddle" style="text-indent: -0.25in;"><span style=""><span style="">2)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span>Now Double click on
DieCluster.exe file to open a window, it should look like this:</p>

<p class="MsoListParagraphCxSpMiddle"><o:p>&nbsp;</o:p></p>

<p class="MsoListParagraphCxSpMiddle"><span style=""><img border="0" width="506" height="418" src="activation_tutorial_files/image006.jpg" v:shapes="Picture_x0020_4"></span></p>

<p class="MsoListParagraphCxSpMiddle" style="text-indent: -0.25in;"><span style=""><span style="">3)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span><span style="">Now all you need is to fill the relevant boxes with correct values and
surprise <span class="SpellE">surprise</span> press on the “start” <span class="SpellE">botton</span>. <o:p></o:p></span></p>

<p class="MsoListParagraphCxSpLast" style="text-indent: -0.25in;"><span style=""><span style="">4)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span><span class="GramE"><span style="">So</span></span><span style=""> <span class="SpellE">lets</span> mark each box with identifier number just
for clarity of the below explanation<br>
<span style=""><img border="0" width="607" height="502" src="activation_tutorial_files/image008.jpg" v:shapes="Picture_x0020_12"></span><o:p></o:p></span></p>

<h3><b><span style="color: rgb(112, 48, 160);">Region 1: </span></b><b><span style="color: windowtext;">Here you should insert path for a directory were you
want the program will put its results<br>
(If the path currently not exist, the program will create it).<br>
</span></b><b><span style="color: rgb(112, 48, 160);">Region 2: </span></b><b><span style="color: windowtext;">Here you should insert path for the json file that
contains the threshold data<br>
as explained in 3 D above.<br>
If you rely on the json that attached with the zip, you don’t need to change
here anything<br>
the default path is correct, (you need change it only if you rely on another
json with different place or with different name).<o:p></o:p></span></b></h3>

<h3><b><span style="color: rgb(112, 48, 160);">Region 6: </span></b><b><span style="color: windowtext;">The input for the algorithm can be a single file, or a
directory of wafers, or even directory that contains directories that contains
wafers, and so on.<br>
(If the input is directory the algorithm will pass on all files in the
directory in one run <br>
<span style="">&nbsp; </span>and will create also a summary excel).<br>
So if the input is full directory of wafers you should check this box, else (if
it a single file)<br>
just remove it unchecked.<o:p></o:p></span></b></h3>

<h3><b><span style="color: rgb(112, 48, 160);">Region 4:</span></b><b><span style="color: windowtext;"> If you leave box </span></b><b><span style="color: rgb(112, 48, 160);">6</span></b><b><span style="color: windowtext;"> unchecked,
you may simply ignore this box (The program will ignore it), else just insert
here the path of the directory that contains all the wafers<br>
Please pay attention that this directory should contains only wafers (or
directories that contain directories that contain wafers and everything like
that), and not anything else.<br>
</span></b><b><span style="color: rgb(112, 48, 160);">Region 3: </span></b><b><span style="color: windowtext;">If you leave box </span></b><b><span style="color: rgb(112, 48, 160);">6</span></b><b><span style="color: windowtext;"> checked you may ignore
this box (The program will ignore it), else just insert here the path of the
wafer file (it can be either .txt or .<span class="SpellE">stdf</span> file).<br>
</span></b><b><span style="color: rgb(112, 48, 160);">Region 5: </span></b><b><span style="color: windowtext;">For now it simply deed area (Historically It was
responsible to rule if the screen will display only INFO or also DEBUG messages
when running, but finally I change it so that always it will display also DEBUG
messages, it very easy to change it back if you wish, or to delete this area,
with small changes in main.py script).<o:p></o:p></span></b></h3>

<h3><b><span style="color: rgb(112, 48, 160);">Region 7: </span></b><b><span style="color: windowtext;">Finally, just click start to run.<o:p></o:p></span></b></h3>

<p class="MsoNormal"><o:p>&nbsp;</o:p></p>

<p class="MsoNormal">After successful run you need to see something like this:<br>
<span style=""><img border="0" width="624" height="330" src="activation_tutorial_files/image010.jpg" v:shapes="Picture_x0020_9"></span></p>

<p class="MsoNormal">The results lie where you told the program to put them in <b><span style="color: rgb(112, 48, 160);">region 1<o:p></o:p></span></b></p>

<p class="MsoNormal"><a href="https://github.com/Vayyar/ChipProduction/tree/master/how_the_results_should_look_like_after_sucessful_run/results_of_resources_Date_2020_09_29_20_51_09"><b>Here
</b>example of how the program results should look like</a><b><o:p></o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b><o:p>&nbsp;</o:p></b></p>

<p class="MsoNormal"><b>And the html files should look likes <o:p></o:p></b></p>

<p class="MsoNormal"><span style=""><img border="0" width="624" height="474" src="activation_tutorial_files/image012.jpg" v:shapes="Picture_x0020_10"></span></p>

<p class="MsoNormal"><o:p>&nbsp;</o:p></p>

<h2><b><span style="color: rgb(112, 48, 160);">Comments:<o:p></o:p></span></b></h2>

<p class="MsoListParagraphCxSpFirst" style="text-indent: -0.25in;"><span style=""><span style="">1)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span><b>Efficiency</b>: there
are huge difference in running time between the program if we run it as .exe
file, or as .<span class="SpellE">py</span> file by simply running main.py
script, when the <span class="SpellE">later</span> is quicker in order of
magnitude, so it may worth considering to run it through main.py (its also
create a GUI window)<br>
when there are huge amounts of wafers.<br style="">
<br style="">
</p>

<p class="MsoListParagraphCxSpMiddle" style="text-indent: -0.25in;"><span style=""><span style="">2)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span><b>Efficiency</b>: The vast
majority of the time (something like 97%) taken by the <span class="SpellE">savefig</span>
method of matplotlib package (Used in HtmlViewer.py file in scripts directory),
that saves the figures which latter I plant in the html file (I mean the wafer
figures).</p>

<p class="MsoListParagraphCxSpMiddle"><o:p>&nbsp;</o:p></p>

<p class="MsoListParagraphCxSpLast" style="text-indent: -0.25in;"><span style=""><span style="">3)<span style="font-weight: normal; font-size: 7pt; font-family: &quot;Times New Roman&quot;;">&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><span dir="LTR"></span>When trying to make things
parallel (In attempt to save time) the Gooey (which create the GUI window) get
very crazy with problems that I find very hard to solve.</p>

<h3><b><span style="color: windowtext;"><br style="">
<br style="">
</span></b><b><span style="color: rgb(112, 48, 160);"><o:p></o:p></span></b></h3>

<p class="MsoNormal"><o:p>&nbsp;</o:p></p>

</div>




