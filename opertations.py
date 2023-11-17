# functions for general operations including opening files

import pandas as pd
import numpy as np
import os
import pyedflib
import math
import warnings
warnings.filterwarnings('ignore')
from IPython.display import Image
import re

# 1  Event Code               Label   
# 2           0        button press  
# 3           1  introduction track  
# 4           2        pre-baseline  
# 5           3      instruction 1a 
# 6           4      instruction 1b  
# 7           5       instruction 2  
# 8           6               relax  
# 9           7       instruction 3  
# 10          8           'prepare'  
# 11          9                 awe  
# 12         10         frustration  
# 13         11                 joy  
# 14         12               anger  
# 15         13               happy  
# 16         14                 sad  
# 17         15                love  
# 18         16                fear  
# 19         17          compassion  
# 20         18            jealousy  
# 21         19             content  
# 22         20               grief  
# 23         21              relief  
# 24         22              excite  
# 25         23             disgust  
# 26         24            'return'  
# 27         25       post-baseline  
# 28         26              thanks 
# 29         30       stop baseline   

# names of channels
# AF7: F10
# AF8: D24
# TP9: G32
# TP10: B31


def bdf_to_df(file_path):
    #file_name = os.path.join('data', file_path)
    f = pyedflib.EdfReader(file_path)
    n = f.signals_in_file
    signal_labels = f.getSignalLabels()
    sigbufs = np.zeros((n, f.getNSamples()[0]))
    for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)
    rec = pd.DataFrame(sigbufs).T
    rec.columns = signal_labels
    return rec
#open bdf file and convert to data frame
rec1 = bdf_to_df('eeg_recording_1.bdf')

#remove all channeles except the ones we want, Status corresponds to the emotion labels
data = rec1.loc[:,['1F10','1D24','1G23','1B31','Status']]


def check_status(df):
    print(len(df.Status.unique()))
    print(sorted(df.Status.unique()))
    return (len(df.Status.unique()), sorted(df.Status.unique()))
# check_status(rec1)


import requests
import bs4 
url = 'http://headit.ucsd.edu/studies/3316f70e-35ff-11e3-a2a9-0050563f2612/description'
r = requests.get(url)
soup = bs4.BeautifulSoup(r.text, 'html.parser')
table = soup.find_all('table')[-2]
status = pd.read_html(str(table))[0]
status.columns = status.iloc[1]
status = status.iloc[2:]
#print(status)
#print(rec1.Status.value_counts())

# Create dictionary for lables
event_code = list(status['Event Code'])
python_event_code = check_status(rec1)[1]
Event_dictionary = {}
for i in range(len(event_code)):
    Event_dictionary[python_event_code[i]] = event_code[i]
#{3407872.0: '0', 3407873.0: '1', 3407874.0: '2', 3407876.0: '3', 3407877.0: '4', 3407878.0: '5', 3407879.0: '6', 3407880.0: '7', 3407881.0: '8', 3407882.0: '9', 3407883.0: '10', 3407884.0: '11', 3407885.0: '12', 3407886.0: '13', 3407887.0: '14', 3407888.0: '15', 3407889.0: '16', 3407890.0: '17', 3407891.0: '18', 3407893.0: '19', 3407894.0: '20', 3407895.0: '21', 3407896.0: '22', 3407897.0: '23', 3407898.0: '24', 3407902.0: '25', 3407972.0: '26', 3473408.0: '30'}
#print(Event_dictionary)
#rec = data[data.Status != 3407872]
data.Status = data.Status.apply(lambda x: Event_dictionary[x])

data.to_csv('eeg_recording_chopped', index=False)
