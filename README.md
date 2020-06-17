# ChipProduction<br/>
1) The project get a wafer and apply a algorithm on it that aim for finding failed chips <br/>
that pass the tests.<br/><br/>

2) For mark chip as fail we look at all its 8 neighbors, <br/>
   And mark the chip as failed iff the number of failed neighbors is <br/>
   bigger than or equals to some threshold when the threshold is function f:{0,...,8} -> {0,...,8}.<br/><br/>
   
3) Input Parameters:<br/> 
  a) Path for The wafer as text file or .stdf file.<br/>
  b) Path of directory to put the results in it.<br/>
  c) Path of .json file that contains dict of number of neighbors to threshold.<br/>
     the json would look like this : <br/>
     {"0": 1, "1": 1, "2": 1, "3": 2, "4": 3, "5": 3, "6": 4, "7": 5, "8": 6}<br/>    here for example in "0": 1  "0" means 0 neighbors        case and 1 is the threshold.<br/><br/>
      
4) Running example: <br/>
   a) from command line:<br/>
      'python main.py --ignore-gooey ../resources/N6W014.0V-24.txt ../results ../resources/neighbors_table.json'<br/>
   b) 
   
5) Program steps:<br/>
   a) Validate the input parameters.<br/>
   b) Read the input wafer file.<br/>
   c) Parse it and store only the wafer map into memory as ChipsGrid object.<br/>
   d) apply the algorithm for predict who chips are failed and make new ChipsGrid object that represents the new state.<br/>
   e) Generate .jpg file with iamges of input output and a summary in the middle.<br/>
   f) Save result wafer as text file.<br/>
   
   

 
