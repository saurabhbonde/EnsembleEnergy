# Importing Libraries

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Creating Variable with filenames

filename = ["Device1_2020_07_01_00_00_02.969_2020_07_31_23_59_58.110.csv","Device2_2020_07_01_00_00_02.962_2020_07_31_23_59_55.106.csv","Device3_2020_07_01_00_00_02.961_2020_07_31_23_59_56.601.csv",
            "Device4_2020_07_01_00_00_02.967_2020_07_31_23_59_58.103.csv","Device5_2020_07_01_00_00_05.962_2020_07_31_23_59_58.103.csv","Device6_2020_07_01_00_00_01.461_2020_07_31_23_59_56.606.csv"]

# Reading datasets using for loop & concatenate them into one file.

data = pd.DataFrame()     #defining variable type dataframe

for filenames in filename:          # for loop start here
    
    df = pd.read_csv(filenames)
    data = pd.concat([data, df], ignore_index=True)         #for loop end here

# We have the final dataset containing all 6 files data   
    
data.head()   #taking glims of final dataset

data.shape    #size of data

data.tail()   # last 5 rows of the data

df1.count()

#Checking for missing values

data.isnull().sum()

# visualising dataset to understand the data.

sns.heatmap(data.isnull(),yticklabels=False,cbar=False)

# Understanding Categorical variable


print(data['variable'].unique())   # checking for distinct variables in each dataframe

len(data['variable'].unique())     # total number of variables in each dataframe

data["variable"].describe()        # info about variables

data["variable"].value_counts()    # Number of respective variable in the data

# Changing data type of the TimeStamp variable to datetime 

data["TimeStamp"] = pd.to_datetime(data["TimeStamp"])  # Converting column data type into date time format

data["TimeStamp"].dtype     #Checking datatype of the TimeSTamp column

# Sorting  the data by timestamp for futher processing

data = data.sort_values(by=['TimeStamp'])

data.head(100)   # checking top 100 rows of data

agg_data = pd.DataFrame()     #defining variable type dataframe

#Aggregating dataset as per 10 minute timeframe using TimeStamp Column 

agg_data = data.groupby([pd.Grouper(key="TimeStamp",freq='10Min'), "variable", "device"]).last() # last value of the value column is taken
agg_data.rename({'value':'last_value'},axis=1,inplace=True)  #converting label of value column to last_value

# Calculating & adding average column

agg_data['average'] = data.groupby([pd.Grouper(key="TimeStamp",freq='10Min'), "variable", "device"]).agg('mean')  

# Calculating & adding Minimum column

agg_data['minimum'] = data.groupby([pd.Grouper(key="TimeStamp",freq='10Min'), "variable", "device"]).agg('min')

# Calculating & adding Maximum column

agg_data['maximum'] = data.groupby([pd.Grouper(key="TimeStamp",freq='10Min'), "variable", "device"]).agg('max')

# Calculating & adding Standard Deviation column

agg_data['std_dev'] = data.groupby([pd.Grouper(key="TimeStamp",freq='10Min'), "variable", "device"]).agg('std')

# After processimg data for 10 minute aggregate convert TimeStamp index to Column

agg_data = agg_data.reset_index()

# Adding us timestamp to the aggregated data

agg_data["TimeStamp_us"] = agg_data.TimeStamp.dt.tz_localize('UTC').dt.tz_convert('America/Los_Angeles')

#Taking care of NaN Values by filling "0"

agg_data = agg_data.fillna(0)

#Checking processed dataset

agg_data.head()
agg_data.tail()

# Variable for retriving points for scatterd plot

var1 = ['WTUR1_W']        # variable of "WTUR1_W"

var2 = ['WNAC1_WdSpd']    # variable of "WNAC1_SdSpd"   

# Selecting require data

WTUR1_W_data = agg_data[agg_data['variable'].isin(var1)]      # dataframe of "WTUR1_W"
    
WNAC1_WdSpd_data = agg_data[agg_data['variable'].isin(var2)]  # dataframe of "WNAC1_SdSpd"

x = WNAC1_WdSpd_data["average"]  # WNAC1_SdSpd_AVG data values

y = WTUR1_W_data["average"]      # WTUR1_W_AVG data values

#SCATTERED plot of WNAC1_SdSpd_AVG on x axia & WTUR1_W_AVG axis

plt.scatter(x, y, c ="blue")     # Plotting Scattered plot

plt.xlabel("WNAC1_WdSpd_AVG")    # X - lable given to scattered plot

plt.ylabel("WTUR1_W_AVG")        # Y - lable given to scattered plot

plt.show()       # Visualise the scattered plot


