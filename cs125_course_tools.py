import warnings

with warnings.catch_warnings():
    # filter sklearn\externals\joblib\parallel.py:268:
    # DeprecationWarning: check_pickle is deprecated
    warnings.simplefilter("ignore", category=FutureWarning)
    import pandas as pd
    import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import Markdown as md

def column_report(categories, df, series_name):
  '''
  takes category labels, df, and series name as string
  returns value counts with all categories properly ordered and filled
  '''
  counts = df[series_name].value_counts(normalize = True)
  base = pd.DataFrame(categories, columns = [series_name]).set_index(series_name)
  merged = pd.merge(base, counts, left_index=True, right_index=True, how='left')
  merged.index.name = None
  merged.loc[merged[series_name].isna(),series_name] = 0  
  return merged

def exercise_time_difficulty_report(exercise_name):
  # web address of published google sheet
  url_exercise_td = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSUa5PfAqioAzKa0ZUowuLMGm8s3TwvsfN9nqqwxQb0C5RQqzQEdvbHlYdZfEVSPLOgjL_XXrev3Vmx/pub?gid=153373153&single=true&output=csv'
  df = pd.read_csv(url_exercise_td)

  # restrict to current exercise
  df_exercise = df[df['Exercise'] == exercise_name] 

  # category labelled, used for filling out empty category responses
  difficult_categories = ['Very Easy', 'Somewhat Easy', 'Neutral', 'Somewhat Difficult', 'Very Difficult']
  time_categories = ['30 min or less', '31-60 min', '61-90 min', '91-120 min', 'More than 2 hours']

  #generate reports
  time_report = column_report(time_categories, df_exercise, 'Time')
  difficulty_report = column_report(difficult_categories, df_exercise, 'Difficulty')

  #display reports
  display(md(exercise_name))
  display(difficulty_report)
  print()
  display(time_report)
