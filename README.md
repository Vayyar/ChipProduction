# Chip Production<br/>
The Project classify chips as pass or fail based on their neighbors rersults in test.<br/><br/>

For mark chip as fail the algorithm look at all its 8 neighbors, <br/>
   And mark the chip as failed if and only if the number of failed neighbors is <br/>
   bigger than or equals to some threshold when the threshold is function f:{0,...,8} -> {0,...,8}.<br/><br/>
   
Input Parameters:<br/> 
  1) Path for The wafer as text file or .stdf file.<br/>
  2) Path of directory to put the results in it.<br/>
  3) Path of .json file that contains dict of number of neighbors to threshold.<br/>
     the json would look like this : <br/>
     {"0": 1, "1": 1, "2": 1, "3": 2, "4": 3, "5": 3, "6": 4, "7": 5, "8": 6}<br/>    here for example in "0": 1  "0" means 0 neighbors        case and 1 is the threshold.<br/><br/>
      
Running example: <br/>
   From command line:<br/>
      'python main.py --ignore-gooey ../resources/N6W014.0V-24.txt ../results ../resources/neighbors_table.json'<br/>
   From gooey:
       Double click on DieCluster.exe file, now you see this window:
       
   
Program steps:<br/>
   1) Validate the input parameters.<br/>
   2) Read the input wafer file.<br/>
   3) Parse it and store the wafer map into memory as ChipsGrid object.<br/>
   4) apply the algorithm for predict who chips are failed and make new ChipsGrid object that represents the new state.<br/>
   5) Generate .jpg file with images of input output and a summary.<br/>
   6) Save result wafer as text file.<br/>
   
   

 
