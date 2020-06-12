import urllib.request as request
import os
import pandas as pd
from scipy import stats

def get_coursedata_125(url_files):
  '''
  takes list of file names, mostly .csv
  retrieves files from github, converts to dataframe
  returns list of dataframes
  '''
  
  url_root = 'https://raw.githubusercontent.com/'
  url_repo = 'bsheese/CSDS125ExampleData/master/'
    
  for f_name in url_files:
    filedata = request.urlopen(url_root + url_repo + f_name).read().decode()
    f = open(f_name, "w+")
    f.write(filedata)
    f.close()

  if os.path.exists('/content/' + url_files[0]):
    print('Files successfully downloaded')
  else:
    print('Something went wrong. Please ask for assistance.')

  dataframe_list = []
  for f_name in url_files:
    dataframe_list.append(pd.read_csv(f_name))

  return dataframe_list

def createSkewDist(mean, sd, skew, size):
  '''
  creates data with specific skew
  takes mean, sd, skew, and size
  returns data as numpy array
  # from https://stackoverflow.com/a/58111859
  '''

  # calculate the degrees of freedom 1 required to obtain the specific skewness statistic, derived from simulations
  loglog_slope=-2.211897875506251 
  loglog_intercept=1.002555437670879 
  df2=500
  df1 = 10**(loglog_slope*np.log10(abs(skew)) + loglog_intercept)

  # sample from F distribution
  fsample = np.sort(stats.f(df1, df2).rvs(size=size))

  # adjust the variance by scaling the distance from each point to the distribution mean by a constant, derived from simulations
  k1_slope = 0.5670830069364579
  k1_intercept = -0.09239985798819927
  k2_slope = 0.5823114978219056
  k2_intercept = -0.11748300123471256

  scaling_slope = abs(skew)*k1_slope + k1_intercept
  scaling_intercept = abs(skew)*k2_slope + k2_intercept

  scale_factor = (sd - scaling_intercept)/scaling_slope    
  new_dist = (fsample - np.mean(fsample))*scale_factor + fsample

  # flip the distribution if specified skew is negative
  if skew < 0:
      new_dist = np.mean(new_dist) - new_dist

  # adjust the distribution mean to the specified value
  final_dist = new_dist + (mean - np.mean(new_dist))

  return final_dist
