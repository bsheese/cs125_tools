# if you ever come back to this...
# new forms need to be set to accept public responses (outside IWU)
# this is in forms -> settings, and is unrelated to the share settings

import warnings
from IPython.display import HTML

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


# response form functions start here

def widget_slider(min1, max1, step1, value1, description1):
    w1 = widgets.IntSlider(
        min=min1,
        max=max1,
        step=step1,
        description=description1,
        value=value1)
    return w1


def widget_text_shortresponse(box_text, box_description):
    w1 = widgets.Text(
        value='',
        placeholder=box_text,
        description=box_description,
        disabled=False)
    return w1


def widget_text_bigresponse(box_text, box_description):
    w1 = widgets.Textarea(
        value='',
        placeholder=box_text,
        description=box_description,
        disabled=False)
    return w1


def widget_toggle_buttons(option_list, start_value, qdescription):
    w1 = widgets.ToggleButtons(
        options=option_list,
        description=qdescription,
        disabled=False,
        value=start_value,
        button_style='warning')  # 'success', 'info', 'warning', 'danger' or ''
    return w1


def widget_drop_down(option_list, start_value, qdescription):
    w1 = widgets.Dropdown(
        options=option_list,
        description=qdescription,
        disabled=False)
    return w1


def submit_exercise_response(er_question_list):
    '''
    takes exercise title and list of widgets
    submits to google form
    crazy hodgepodge of new and old code
    refactor this
    '''

    while True:

        if er_question_list[0][2].value.strip() == '' or er_question_list[1][2].value.strip() == '':
            print('Please enter your first and last name in the form above and then rerun this cell.')
            break
        if er_question_list[2][2] == 'None selected':
            print('Please enter your class name in the form above and then rerun this cell.')
            break
        if er_question_list[3][2] == 'None selected':
            print('Please enter the project name in the form above and then rerun this cell.')
            break
        if er_question_list[4][2].value.strip() == '':
            print('Please enter the link to your shared notebook in the form above and then rerun this cell.')
            break

            
        else:
            response_list = []
            for r in er_question_list:
                response_list.append(r[2].value)

            url_base = 'https://docs.google.com/forms/d/e/'
            form_url = '1FAIpQLSfNdA6gJbOzAqU3s-UZHexbeeYPreEYRdDgfJbX8MG5pX9pOg/'
            form_url2 = 'formResponse?usp=pp_url'
            submit_url = '&submit=Submit'

            surveyq_list = [
                f'&entry.922239715={response_list[0]}',
                f'&entry.23194895={response_list[1]}',
                f'&entry.319075564={response_list[2]}',
                f'&entry.1378021819={response_list[3]}',
                f'&entry.1741521526={response_list[4]}']

            surveyq_url = ''
            for q in surveyq_list:
                surveyq_url = surveyq_url + q

            url1 = url_base + form_url + form_url2 + surveyq_url + submit_url
            url1 = url1.replace(" ", "%20")
            # print(url1)

            requests.post(url=url1)  # response [200]
            print('Exercise response submitted.')

            break


def display_form(er_question_list):
    print(
        'If this form does not display correctly in Colab, select "Runttime" from the menu at the top, then select "Restart and run all"')
    for q in er_question_list:
        print(q[1])
        display(HTML(
            '''<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"> '''))
        display(q[2])
        print()


# response survey questions and widgets, first entry is currently unused
er_question_list = [
    ['first_name',
     'Your first name:',
     widget_text_shortresponse('Enter your first name here', '')],
    ['last_name',
     'Your last name:',
     widget_text_shortresponse('Enter your last name here', '')],
    ['class',
     'What class was this project for?',
     widget_drop_down(['None selected',
                       'CS/DS125',
                       'DS225',
                       'CS/DS377',
                       'CS380/DS395'],
                       'None selected', '')],
    ['project',
     'Which project are you submitting?',
     widget_drop_down(['None selected', '9.9.2 Visualizations - Multiple',
                       '10.9.9 Correlations/Scatterplots',
                       '15.9.9 Complete Analysis',
                       '17.9.1 Simple Linear Regression',
                       '18.9.1 Classification',
                       'Other'],
                       'None selected', '')],
    ['share',
     "Share your notebook.\nSelect 'Share' at the top of the screen. Then select 'Get Link'.\nChange the Link so anyone can view it.\nClick 'Copy Link', then 'Done'. Paste the link here.",
     widget_text_bigresponse('Enter your response here', '')]]
