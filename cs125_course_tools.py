import warnings

with warnings.catch_warnings():
    # filter sklearn\externals\joblib\parallel.py:268:
    # DeprecationWarning: check_pickle is deprecated
    warnings.simplefilter("ignore", category=FutureWarning)
    import pandas as pd
    import seaborn as sns
import matplotlib.pyplot as plt

import ipywidgets as widgets
from IPython.display import Markdown as md
from IPython.display import display
import requests

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


'''
response form functions start here
'''

def widget_slider(min1,max1,step1,value1,description1):
  w1 = widgets.IntSlider(
    min=min1,
    max=max1,
    step=step1,
    description=description1,
    value=value1)
  return w1 

def widget_text_shortresponse(box_text,box_description):
  w1 = widgets.Text(
      value='',
      placeholder= box_text,
      description=box_description,
      disabled=False)
  return w1

def widget_text_bigresponse(box_text,box_description):
  w1 = widgets.Textarea(
      value='',
      placeholder= box_text,
      description=box_description,
      disabled=False)
  return w1

def widget_toggle_buttons(option_list, start_value, qdescription):
  w1 = widgets.ToggleButtons(
      options=option_list,
      description=qdescription,
      disabled=False,
      value=start_value,
      button_style='warning') # 'success', 'info', 'warning', 'danger' or ''      
  return w1

def submit_exercise_response(title, er_question_list):
  '''
  takes exercise title and list of widgets
  submits to google form
  crazy hodgepodge of new and old code
  refactor this
  '''
  
  while True:
    
    if er_question_list[0][2].value == '' or er_question_list[1][2].value == '':
      print('Please enter your first and last name in the form above and then rerun this cell.')
      break
    
    else:
      response_list = []
      for r in er_question_list:
        response_list.append(r[2].value)
      
      url_base = 'https://docs.google.com/forms/d/e/'
      form_url = '1FAIpQLSeDkLEgVpEBQG-8abkLjpYeYWm2j-_afsUHu7vVq9FCHdHwSg/'
      form_url2 = 'formResponse?usp=pp_url'
      submit_url = '&submit=Submit'

      surveyq_list = [
      f'&entry.1690149919={title}',
      f'&entry.1977535025={response_list[0]}',
      f'&entry.266287712={response_list[1]}',
      f'&entry.1353593799={response_list[3]}',
      f'&entry.1619132276={response_list[2]}',
      f'&entry.997960525={response_list[4]}',
      f'&entry.1833143982={response_list[5]}',
      f'&entry.1819709919={response_list[6]}',
      f'&entry.689289533={response_list[7]}'
      f'&entry.1647967109={len(globals())}']

      surveyq_url = ''
      for q in surveyq_list:
        surveyq_url = surveyq_url + q 

      url1 = url_base+form_url+form_url2+surveyq_url+submit_url
      url2 = f'https://docs.google.com/forms/d/e/1FAIpQLScyCGrAprmJusds1VQhc9yQyUXBy2Bd5HWf0ScLUETdXQLGDQ/formResponse?usp=pp_url&entry.1755758539={title}&entry.1401831102={response_list[2]}&entry.1839622038={response_list[3]}&submit=Submit'

      requests.post(url1)  # response [200]
      requests.post(url2)  # response [200]
      print('Exercise response submitted.')
            
      break

def display_form(er_question_list):
  for q in er_question_list:
    print(q[1])
    display(q[2])
    print()

# response survey questions and widgets, first entry is currently unused
er_question_list = [
                ['first_name',
                 'Your first name:',
                 widget_text_shortresponse('Enter your first name here','')],
                ['last_name',
                 'Your last name:',
                 widget_text_shortresponse('Enter your last name here','')],
                ['difficulty',
                 'How difficult was the exercise?',
                 widget_toggle_buttons(['Very Easy', 'Somewhat Easy', 'Neutral',
                                        'Somewhat Difficult', 'Very Difficult'],
                                       'Neutral','')],
                ['time',
                 'How long did it take you to complete the exercise?',
                  widget_toggle_buttons(['30 min or less', '31-60 min', '61-90 min',
                                       '91-120 min', 'More than 2 hours'],
                                       '61-90 min', '')],
                ['confident',
                 'What tools (or concepts) used in this exercise do you feel confident with?',
                  widget_text_bigresponse('Enter your response here','')],
                ['needswork',
                 'What tools (or concepts) do you still need practice with?',
                  widget_text_bigresponse('Enter your response here','')],
                ['suggestions',
                 'What suggestions do you have for improving the exercise?',
                  widget_text_bigresponse('Enter your response here','')],
                 ['corrections',
                  'What corrections should be made (typos. etc)?',
                  widget_text_bigresponse('Enter your response here','')]
                ]