# research_monitor
#### This is a python-based project designed for ISSD of KIT, in order to improve the automation and intelligence of the research monitor used inside ISSD.

This project needs to use the following third-party libraries of python:

```
import datetime
import pandas
import numpy
import re
import os
import requests
from bs4 import BeautifulSoup
import keras
import nltk
import plotly.graph_objects 
import networkx
import wordcloud
```


### REMINDER: After saving all the codes and data of this program locally, you only need to start main.py to run this program, and the program will automatically call other modules.


#### The following is the documentation for main.py:


The program will first check whether there is a folder that meets the preset naming rules in the local area. main.py will print on the console the name of the folder that is applicable to the day the program is run.

 > D:\py_research_monitor\data\2020-Q3u4\
 
 
search_string.main() will crawl the current list of the latest researchers from the ISSD website. After comparing with the past data, it will add the newly added researcher's name to the search string and save it to the local notepad file. After this step is successfully executed, the program will print the file save path on the console.

> Getting search string of ISSD ...
> 
> Successfully created file of search string under path: D:\py_research_monitor\researchers list\search string 2020-Q3u4.txt


search_string_im.main() will perform a similar process for the IM team’s list, but due to some differences in the web page structure of the two teams’ websites, the two modules have not been merged. After this step is successfully executed, the program will also print the file save path on the console.

> Getting search string of IM ...
> 
> Successfully created file of search string under path: D:\py_research_monitor\researchers list\search string_im 2020-Q3u4.txt


get_KITopen.main() will automatically send a request to KIT-Open based on the ISSD search string, and save the returned data to a local excel file. get_KITopen_im.main() will perform a similar process. After completing these steps, the program will also print the file save paths on the console.

> Getting data of ISSD from KIT-Open...
> 
> Successfully saved data of ISSD into Excel file under path: D:\py_research_monitor\data\2020-Q3u4\report_2020Q3u4.xlsx
> 
> Getting data of IM from KIT-Open...
> 
> Successfully saved data of IM into Excel file under path: D:\py_research_monitor\data\2020-Q3u4\report_im_2020Q3u4.xlsx


clean_report.main() will clean the data from KIT Open and integrate all the data that needs to be used into the new file. After this step is successfully executed, the program will also print the file save path on the console.

> Cleaning Excel file from KIT Open...
> 
> Successfully created cleaned report of ISSD under path: D:\py_research_monitor\data\2020-Q3u4\report_2020Q3u4_clean.xlsx
> 
> Successfully created cleaned report of IM under path: D:\py_research_monitor\data\2020-Q3u4\report_2020Q3u4_clean.xlsx


predict_tag.main() will predict the missing ‘KIT-tag’ in the report based on the trained model (ML-model training/tag_model.h5). (If you want to retrain this model, you can modify the relevant data in the'model training' folder and run train_model.py) After the prediction process is completed, the prediction results will be saved to a local excel file. After this step is successfully executed, the program will also print the file save path on the console.


> Predicting blank KIT-tags in the report...
> 
> Successfully saved predictions under path: D:\py_research_monitor\data\2020-Q3u4\tag_prediction_2020Q3u4.xlsx


Next, the program will first determine whether the previous PoPCites.csv exists, if it does not exist, the program will remind the user to add the previous PoPCites.csv to the corresponding folder, and will not continue to run until the file is added correctly. calc_cites_delta.main() will calculate the corresponding data based on the previous PoPCites.csv and current PoPCites.csv data, and save it to a local folder. After this step is successfully executed, the program will also print the file save path on the console.

> Calculating relative data of PoPCites.csv...
> 
> Successfully calculated data and saved under path: D:\py_research_monitor\data\2020-Q3u4\citation_delta.csv


get_data_network.main() and get_network.main() will count the cooperation relationship between researchers, generate a visual network and save it as a local html file. After this step is successfully executed, the program will also print the file save path on the console.

> Getting data of authors...
> 
> Successfully saved author data under path: D:\py_research_monitor\data\2020-Q3u4\data_network_2020Q3u4.xlsx
> 
> Generating cooperation network of authors...
> 
> Successfully generated cooperation network under path: D:\py_research_monitor\data\2020-Q3u4\network_author.html

get_wordcloud.main() will generate the corresponding word cloud according to the research paper titles of ISSD and IM and save it as a local png file.After this step is successfully executed, the program will also print the file save path on the console.

> Generating wordclouds of paper titles...
> Successfully generated wordclouds of paper titles


#### _Thanks to @SvenMichalczyk for his guidance and support throughout this project. Thanks to @MingjieZhang for his suggestions and help in the tag prediction module._
