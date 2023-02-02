import pages.dates

import dash
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

from dash import dcc, html, Output, Input, callback
from datetime import date

import plotly.graph_objects as go

dash.register_page(__name__, path='/', title='Covid-19 Tracker')

# store the date of the current day  inside the today variable
today = date.today()

# casting the today variable as a string
str_today = str(today)


# link of the french covid-19 dataset :  https://www.data.gouv.fr/fr/datasets/synthese-des-indicateurs-de-suivi-de-lepidemie-covid-19/
# store the direct url of the dataset inside the url variable
url = "https://www.data.gouv.fr/fr/datasets/r/f335f9ea-86e3-4ffa-9684-93c009d5e617"

# use pandas to read the url
read_csv = pd.read_csv(url)

#######################################
# set the dataframe as a datetime series
#######################################

read_csv["date"] = pd.to_datetime(read_csv["date"], format='%Y-%m-%d')

#####################################
# create new column
#####################################

read_csv['annee'] = read_csv['date'].dt.year
read_csv['mois'] = read_csv['date'].dt.month
read_csv['jour'] = read_csv['date'].dt.day


####################################
# create column full name of month
####################################

read_csv['month_full'] = read_csv['date'].dt.month_name()

######################################
# create short name of month
######################################

read_csv['month_short'] = read_csv['date'].dt.month_name().str[:3]

########################################
# set two digit in mois and jour column
########################################

read_csv['annee'] = read_csv.annee.map("{:04d}".format)
read_csv["mois"] = read_csv.mois.map("{:02d}".format)
read_csv["jour"] = read_csv.jour.map("{:02d}".format)


########################################
# set date as index
########################################

read_csv = read_csv.set_index('date')


########################################
# reset index
########################################

reset_index = read_csv.reset_index()

##########################################
# filter per year
##########################################

filter_year = read_csv[(read_csv["annee"] == today.strftime('%Y'))]

#############################################
# filter per month
##############################################

filter_month = read_csv[read_csv["mois"] == today.strftime('%m')]

#############################################
# filter per day
##############################################

filter_day = read_csv[read_csv["jour"] == today.strftime('%d')]



#################################################
# hosp column = patients in hospital
# rea column = patients in intensive care
# incid_rad column = hospital dischage
# incid_dchosp = dead patients in hospital
#################################################


#################################################
# dict of preformatted subset for hosp column
#################################################

hosp_subset = read_csv[["hosp", "annee", "mois", "jour"]].dropna()
up_to_now_hosp = reset_index[["hosp", "date", "annee", "mois", "jour"]].dropna()
last_6months_hosp = read_csv[['hosp', 'mois', 'month_short']].last('6M').dropna()
display_groupby_hosp = last_6months_hosp.groupby(['month_short'])['hosp'].mean().sort_values().astype(int)

dict_subset_hosp = {
    "last_6months_hosp": last_6months_hosp,
    "up_to_now_subset_hosp": up_to_now_hosp[((up_to_now_hosp['date'] >= f"{pages.dates.BEGINING_YEAR_2020}"))],
    "group_by_last_6months_hosp": display_groupby_hosp
}


display_groupby_hosp_yearly = up_to_now_hosp.groupby('annee')['hosp'].agg(['min', 'max', 'mean']).reset_index().astype(int)
display_groupby_hosp_yearly.rename(columns={'annee': 'Year', 'min': 'Lowest', 'max': 'Highest', 'mean': 'Average'}, inplace=True)

display_groupby_hosp_yearly_to_df = pd.DataFrame(data=display_groupby_hosp_yearly)

#################################################
# dict of preformatted subset for rea column
#################################################

rea_subset = read_csv[["rea", "annee", "mois", "jour"]].dropna()
up_to_now_rea = reset_index[["rea", "date", "annee", "mois", "jour"]].dropna()
last_6months_rea = read_csv[['rea', 'mois', 'month_short']].last('6M').dropna()
display_groupby_rea = last_6months_rea.groupby(['month_short'])['rea'].mean().sort_values().astype(int)
dict_subset_rea = {
    "last_6months_rea": last_6months_rea,
    "up_to_now_subset_rea": up_to_now_rea[((up_to_now_rea['date'] >= f"{pages.dates.BEGINING_YEAR_2020}"))],
}

display_groupby_rea_yearly = up_to_now_rea.groupby('annee')['rea'].agg(['min', 'max', 'mean']).reset_index().astype(int)
display_groupby_rea_yearly.rename(columns={'annee': 'Year', 'min': 'Lowest', 'max': 'Highest', 'mean': 'Average'}, inplace=True)

display_groupby_rea_yearly_to_df = pd.DataFrame(data=display_groupby_rea_yearly)


#####################################################
# dict of preformatted subset for incid_rad column
#####################################################

incid_rad_subset = read_csv[["incid_rad", "annee", "mois", "jour"]].dropna()
up_to_now_incid_rad = reset_index[["incid_rad", "date", "annee", "mois", "jour"]].dropna()
last_6months_incid_rad = read_csv[['incid_rad','mois', 'month_short']].last('6M').dropna()
display_groupby_incid_rad = last_6months_incid_rad.groupby(['month_short'])['incid_rad'].mean().sort_values().astype(int)
dict_subset_incid_rad = {
    "last_6months_incid_rad": last_6months_incid_rad,
    "up_to_now_subset_rad": up_to_now_incid_rad[((up_to_now_incid_rad['date'] >= f"{pages.dates.BEGINING_YEAR_2020}"))],
}

display_groupby_incid_rad_yearly = up_to_now_incid_rad.groupby('annee')['incid_rad'].agg(['min', 'max', 'mean']).reset_index().astype(int)
display_groupby_incid_rad_yearly.rename(columns={'annee': 'Year', 'min': 'Lowest', 'max': 'Highest', 'mean': 'Average'}, inplace=True)

display_groupby_incid_rad_yearly_to_df = pd.DataFrame(data=display_groupby_incid_rad_yearly)



######################################################
# dict of preformatted subset for incid_dchosp column
#####################################################

incid_dchosp_subset = read_csv[["incid_dchosp", "annee", "mois", "jour"]].dropna()
up_to_now_incid_dchosp = reset_index[["incid_dchosp", "date", "annee", "mois", "jour"]].dropna()
last_6months_incid_dchosp = read_csv[['incid_dchosp', 'mois', 'month_short']].last('6M').dropna()
display_groupby_incid_dchosp = last_6months_incid_dchosp.groupby(['month_short'])['incid_dchosp'].mean().sort_values().astype(int)
incid_dict_subset_dchosp = {
    "last_6months_incid_dchosp": last_6months_incid_dchosp,
    "up_to_now_subset_incid_dchosp": up_to_now_incid_dchosp[((up_to_now_incid_dchosp['date'] > f"{pages.dates.BEGINING_YEAR_2020}"))]
}

display_groupby_incid_dchosp_yearly = up_to_now_incid_dchosp.groupby('annee')['incid_dchosp'].agg(['min', 'max', 'mean']).reset_index().astype(int)
display_groupby_incid_dchosp_yearly.rename(columns={'annee': 'Year', 'min': 'Lowest', 'max': 'Highest', 'mean': 'Average'}, inplace=True)

display_groupby_incid_dchosp_yearly_to_df = pd.DataFrame(data=display_groupby_incid_dchosp_yearly)



########################################################
# displaying fig for hosp column
########################################################

"""
from 2020 up to now
"""

#TODO hosp up to now
hosp_up_to_now = px.area(dict_subset_hosp["up_to_now_subset_hosp"], x="date", y="hosp")

hosp_up_to_now.update_xaxes(showspikes=True,tickprefix="<b>",ticksuffix ="</b>")
hosp_up_to_now.update_yaxes(showspikes=True,tickprefix="<b>",ticksuffix ="</b>")

hosp_up_to_now.update_xaxes(
    dtick="M1",
    tickformat="%b\n%d\n%Y",
    tickangle=-45,
    showgrid=False)

hosp_up_to_now.update_yaxes(showgrid=False)

hosp_up_to_now.update_traces(line_color='#E36414',
                             hovertemplate='Date: %{x} <br>Nb. of patients: %{y}')

hosp_up_to_now.update_layout(paper_bgcolor='#FFFFFF',
                             title_text='<b>Patients in hospital since 2020</b>',
                             font=dict(family="Arial",size=14,color='#4169E1'),
                             xaxis_title="",
                             yaxis_title="",
                             xaxis={'visible': True, 'showticklabels': True},
                             yaxis={'visible': True, 'showticklabels': True},
                             plot_bgcolor='#FFFFFF',
                             hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))

hosp_up_to_now.update_layout(showlegend=False)

"""
group by
"""
#TODO hosp group by 6 months
fig_last_6months_hosp_up_to_now_groupby = px.bar(dict_subset_hosp["group_by_last_6months_hosp"],
                                                 x=dict_subset_hosp["group_by_last_6months_hosp"],
                                                 y=dict_subset_hosp["group_by_last_6months_hosp"].index,
                                                 orientation='h',
                                                 color='hosp',
                                                 #color_continuous_scale=px.colors.diverging.Tropic,
                                                 color_continuous_scale=px.colors.sequential.Oryel,
                                                 labels={"hosp": "<b>Avg. nb. of patients</b>"},
                                                 text_auto=True)

fig_last_6months_hosp_up_to_now_groupby.update_layout(paper_bgcolor='#FFFFFF',
                                                      title_text="<b>Patients in hospital for the last 6 months </b>",
                                                      font=dict(family="Arial",size=14,color='#4169E1'),
                                                      xaxis_title="",
                                                      yaxis_title="",
                                                      yaxis={'visible': True, 'showticklabels': True},
                                                      xaxis={'visible': False, 'showticklabels': False},
                                                      plot_bgcolor='#FFFFFF',
                                                      hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))

fig_last_6months_hosp_up_to_now_groupby.update_xaxes(showspikes=False,tickprefix="<b>",ticksuffix ="</b>")
fig_last_6months_hosp_up_to_now_groupby.update_yaxes(showspikes=False,tickprefix="<b>",ticksuffix ="</b>")


fig_last_6months_hosp_up_to_now_groupby.update_traces(hovertemplate='Month: %{y} <br>Avg. nb. of patients: %{x}')


colorscale = [[0, '#6495ED'], [.5, '#d9d9d9'], [1, '#ffffff']]
font_colors = ['#ffffff', '#000000','#000000']

#TODO hosp table summary

figTableGroupBy_hosp = go.Figure(
                                 data=[
                                     go.Table(header=dict(
                                         values=['<b>Year</b>', '<b>Lowest</b>', '<b>Highest</b>', '<b>Average</b>'],
                                         fill_color='#6495ED',
                                         line_color='#000000',
                                         align='center',
                                         font=dict(color='white')
                                     ),
                                         cells=dict(values=[display_groupby_hosp_yearly_to_df.Year,
                                                            display_groupby_hosp_yearly_to_df.Lowest,
                                                            display_groupby_hosp_yearly_to_df.Highest,
                                                            display_groupby_hosp_yearly_to_df.Average,
                                                            ],
                                                    fill_color='#FFFFFF',
                                                    line_color='#000000',
                                                    height=25,
                                                    align='center'))])

figTableGroupBy_hosp.update_layout(paper_bgcolor='#FFFFFF',
                                   font=dict(family="sans serif", size=14),
                                   title_text="<b>Summary stats of patients in hospital</b>",
                                   title_font_color='#4169E1',
                                   title_font_family="Arial")


figTableGroupBy_hosp.update_layout({'margin': {'t':30}}),



########################################################
# displaying fig for rea column
########################################################


"""
from 2020 up to now
"""
#TODO rea up to now
rea_up_to_now = px.area(dict_subset_rea["up_to_now_subset_rea"], x="date", y="rea")
rea_up_to_now.update_xaxes(showspikes=True,tickprefix="<b>",ticksuffix ="</b>")
rea_up_to_now.update_yaxes(showspikes=True,tickprefix="<b>",ticksuffix ="</b>")

rea_up_to_now.update_xaxes(
    dtick="M1",
    tickformat="%b\n%d\n%Y",
    tickangle=-45, showgrid=False)

rea_up_to_now.update_yaxes(showgrid=False)


rea_up_to_now.update_traces(line_color='#E36414',
                             hovertemplate='Date: %{x} <br>Nb. of patients: %{y}')
rea_up_to_now.update_layout(paper_bgcolor='#FFFFFF',
                            title_text='<b>Patients in intensive care since 2020</b>',
                            font=dict(family="Arial",size=14,color='#4169E1'),
                            xaxis_title="",
                            yaxis_title="",
                            xaxis={'visible': True, 'showticklabels': True},
                            yaxis={'visible': True, 'showticklabels': True},
                            plot_bgcolor='#FFFFFF',
                            hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))

rea_up_to_now.update_layout(showlegend=False)

"""
group by
"""
#TODO rea group by 6 months

fig_last_6months_rea_up_to_now_groupby = px.bar(display_groupby_rea, x=display_groupby_rea, y=display_groupby_rea.index,
                                    orientation='h',
                                    color='rea',
                                    color_continuous_scale=px.colors.sequential.Oryel,
                                    labels={"rea": "<b>Avg. nb. of patients</b>"},
                                    text_auto=True
                                     )
fig_last_6months_rea_up_to_now_groupby.update_layout(paper_bgcolor='#FFFFFF',
                                  title_text="<b>Patients in intensive care for the last 6 months</b>",
                                  font=dict(family="Arial",size=14,color='#4169E1'),
                                  xaxis_title="",
                                  yaxis_title="",
                                  xaxis={'visible': False, 'showticklabels': False},
                                  yaxis={'visible': True, 'showticklabels': True},
                                  plot_bgcolor='#FFFFFF',
                                  hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))

fig_last_6months_rea_up_to_now_groupby.update_xaxes(showspikes=False,tickprefix="<b>",ticksuffix ="</b>")
fig_last_6months_rea_up_to_now_groupby.update_yaxes(showspikes=False,tickprefix="<b>",ticksuffix ="</b>")

fig_last_6months_rea_up_to_now_groupby.update_traces(hovertemplate='Month: %{y} <br>Avg. nb. of patients: %{x}')

#TODO rea table summary

figTableGroupBy_rea = go.Figure(
                                 data=[
                                     go.Table(header=dict(
                                         values=['<b>Year</b>', '<b>Lowest</b>', '<b>Highest</b>', '<b>Average</b>'],
                                         fill_color='#6495ED',
                                         line_color='#000000',
                                         align='center',
                                         font=dict(color='white',)
                                     ),
                                         cells=dict(values=[display_groupby_rea_yearly_to_df.Year,
                                                            display_groupby_rea_yearly_to_df.Lowest,
                                                            display_groupby_rea_yearly_to_df.Highest,
                                                            display_groupby_rea_yearly_to_df.Average,
                                                            ],
                                                    fill_color='#FFFFFF',
                                                    line_color='#000000',
                                                    height=25,
                                                    align='center'))])

figTableGroupBy_rea.update_layout(paper_bgcolor='#FFFFFF',
                                   font=dict(family="sans serif", size=14),
                                   title_text="<b>Summary stats of patients in intensive care</b>",
                                   title_font_color='#4169E1',
                                   title_font_family="Arial")

figTableGroupBy_rea.update_layout({'margin': {'t':30}})


########################################################
# displaying fig for incid_rad column
########################################################

"""
from 2020 up to now
"""
#TODO incid_rad up to now

incid_rad_up_to_now = px.area(dict_subset_incid_rad["up_to_now_subset_rad"], x="date", y="incid_rad")
incid_rad_up_to_now.update_xaxes(showspikes=True,tickprefix="<b>",ticksuffix ="</b>")
incid_rad_up_to_now.update_yaxes(showspikes=True,tickprefix="<b>",ticksuffix ="</b>")

incid_rad_up_to_now.update_xaxes(
    dtick="M1",
    tickformat="%b\n%d\n%Y",
    tickangle=-45,
    showgrid=False)

incid_rad_up_to_now.update_yaxes(showgrid=False)

incid_rad_up_to_now.update_traces(line_color='#E36414',
                                  hovertemplate='Date: %{x} <br>Nb. of hospital discharge: %{y}')
incid_rad_up_to_now.update_layout(paper_bgcolor='#FFFFFF',
                                  title_text="<b>Hospital discharge since 2020</b>",
                                  font=dict(family="Arial",size=14,color='#4169E1'),
                                  xaxis_title="",
                                  yaxis_title="",
                                  xaxis={'visible': True, 'showticklabels': True},
                                  yaxis={'visible': True, 'showticklabels': True},
                                  plot_bgcolor='#FFFFFF',
                                  hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))

incid_rad_up_to_now.update_layout(showlegend=False)


"""
group by
"""
#TODO incid_rad group by 6 months

fig_last_6months_incid_rad_up_to_now_groupby = px.bar(display_groupby_incid_rad, x=display_groupby_incid_rad, y=display_groupby_incid_rad.index,
                                    orientation='h',
                                    color='incid_rad',
                                    color_continuous_scale=px.colors.sequential.Oryel,
                                    labels={"incid_rad": "<b>Avg. nb. hospital discharge</b>"},
                                    text_auto=True
                                     )

fig_last_6months_incid_rad_up_to_now_groupby.update_traces(
                                  hovertemplate='Month: %{y} <br>Avg. nb. of hospital discharge: %{x}')

fig_last_6months_incid_rad_up_to_now_groupby.update_layout(paper_bgcolor='#FFFFFF',
                                  title_text="<b>Hospital discharge for the last 6 months</b>",
                                  font=dict(family="Arial",size=14,color='#4169E1'),
                                  xaxis_title="",
                                  yaxis_title="",
                                  xaxis={'visible': False, 'showticklabels': False},
                                  yaxis={'visible': True, 'showticklabels': True},
                                  plot_bgcolor='#FFFFFF',
                                  hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))

fig_last_6months_incid_rad_up_to_now_groupby.update_xaxes(showspikes=False,tickprefix="<b>",ticksuffix ="</b>")
fig_last_6months_incid_rad_up_to_now_groupby.update_yaxes(showspikes=False,tickprefix="<b>",ticksuffix ="</b>")

#TODO incid_rad table summary

figTableGroupBy_incid_rad = go.Figure(
                                 data=[
                                     go.Table(header=dict(
                                         values=['<b>Year</b>', '<b>Lowest</b>', '<b>Highest</b>', '<b>Average</b>'],
                                         fill_color='#6495ED',
                                         line_color='#000000',
                                         align='center',
                                         font=dict(color='white',)
                                     ),
                                         cells=dict(values=[display_groupby_incid_rad_yearly_to_df.Year,
                                                            display_groupby_incid_rad_yearly_to_df.Lowest,
                                                            display_groupby_incid_rad_yearly_to_df.Highest,
                                                            display_groupby_incid_rad_yearly_to_df.Average,
                                                            ],
                                                    fill_color='#FFFFFF',
                                                    line_color='#000000',
                                                    height=25,
                                                    align='center'))])

figTableGroupBy_incid_rad.update_layout(paper_bgcolor='#FFFFFF',
                                   font=dict(family="sans serif", size=14),
                                   title_text="<b>Summary stats of hospital discharge</b>",
                                   title_font_color='#4169E1',
                                   title_font_family="Arial")

figTableGroupBy_incid_rad.update_layout({'margin': {'t':30}})

########################################################
# displaying fig for incid_dchosp column
########################################################

"""
from 2020 up to now
"""

#TODO incid_dchosp to now

incid_dchosp_up_to_now = px.area(incid_dict_subset_dchosp["up_to_now_subset_incid_dchosp"], x="date", y="incid_dchosp")
incid_dchosp_up_to_now.update_xaxes(showspikes=True,tickprefix="<b>",ticksuffix ="</b>")
incid_dchosp_up_to_now.update_yaxes(showspikes=True,tickprefix="<b>",ticksuffix ="</b>")

incid_dchosp_up_to_now.update_xaxes(
    dtick="M1",
    tickformat="%b\n%d\n%Y",
    tickangle=-45,
    showgrid=False)

incid_dchosp_up_to_now.update_yaxes(showgrid=False)


incid_dchosp_up_to_now.update_traces(line_color='#E36414',
                                     hovertemplate='Date: %{x} <br>Nb. of dead patients in hospital: %{y}')
incid_dchosp_up_to_now.update_layout(paper_bgcolor='#FFFFFF',
                                     title_text='<b>Dead patients in hospital since 2020</b>',
                                     font=dict(family="Arial",size=14,color='#4169E1'),
                                     xaxis_title="",
                                     yaxis_title="",
                                     xaxis={'visible': True, 'showticklabels': True},
                                     yaxis={'visible': True, 'showticklabels': True},
                                     plot_bgcolor='#FFFFFF',
                                     hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))

incid_dchosp_up_to_now.update_layout(showlegend=False)


"""
group by
"""

#TODO incid_dchosp group by 6 months

fig_last_6months_incid_dchosp_up_to_now_groupby = px.bar(display_groupby_incid_dchosp, x=display_groupby_incid_dchosp, y=display_groupby_incid_dchosp.index,
                                    orientation='h',
                                    color='incid_dchosp',
                                    color_continuous_scale=px.colors.sequential.Oryel,
                                    labels={"incid_dchosp" : "<b>Avg. nb. of dead patients</b>"},
                                    text_auto=True
                                     )

fig_last_6months_incid_dchosp_up_to_now_groupby.update_traces(
                                  hovertemplate='Month: %{y} <br>Avg. of dead patients in hospital: %{x}')

fig_last_6months_incid_dchosp_up_to_now_groupby.update_layout(paper_bgcolor='#FFFFFF',
                                  title_text="<b>Dead patients in hospital for the last 6 months</b>",
                                  font=dict(family="Arial",size=14,color='#4169E1'),
                                  xaxis_title="",
                                  yaxis_title="",
                                  xaxis={'visible': False, 'showticklabels': False},
                                  yaxis={'visible': True, 'showticklabels': True},
                                  plot_bgcolor='#FFFFFF',
                                  hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))

fig_last_6months_incid_dchosp_up_to_now_groupby.update_xaxes(showspikes=False,tickprefix="<b>",ticksuffix ="</b>")
fig_last_6months_incid_dchosp_up_to_now_groupby.update_yaxes(showspikes=False,tickprefix="<b>",ticksuffix ="</b>")

#TODO incid_dchosp table summary

figTableGroupBy_incid_dchosp = go.Figure(
                                 data=[
                                     go.Table(header=dict(
                                         values=['<b>Year</b>', '<b>Lowest</b>', '<b>Highest</b>', '<b>Average</b>'],
                                         fill_color='#6495ED',
                                         line_color='#000000',
                                         align='center',
                                         font=dict(color='white',)
                                     ),
                                         cells=dict(values=[display_groupby_incid_dchosp_yearly_to_df.Year,
                                                            display_groupby_incid_dchosp_yearly_to_df.Lowest,
                                                            display_groupby_incid_dchosp_yearly_to_df.Highest,
                                                            display_groupby_incid_dchosp_yearly_to_df.Average,
                                                            ],
                                                    fill_color='#FFFFFF',
                                                    line_color='#000000',
                                                    height=25,
                                                    align='center'))])

figTableGroupBy_incid_dchosp.update_layout(paper_bgcolor='#FFFFFF',
                                   font=dict(family="sans serif", size=14),
                                   title_text="<b>Summary stats of dead patients in hospital</b>",
                                   title_font_color='#4169E1',
                                   title_font_family="Arial")

figTableGroupBy_incid_dchosp.update_layout({'margin': {'t':30}})


layout = html.Div(

    [
        dbc.Tabs(
            [
                dbc.Tab(label="Patients in hospital", label_style={"color": "#6495ED", 'fontWeight': 'bold'}, tab_id="hosp"), ##E36414"
                dbc.Tab(label="Patients in intensive care", label_style={"color": "#6495ED", 'fontWeight': 'bold'}, tab_id="rea"),
                dbc.Tab(label="Hospital discharge", label_style={"color": "#6495ED", 'fontWeight': 'bold'}, tab_id="incid_rad"),
                dbc.Tab(label="Dead patients in hospital", label_style={"color": "#6495ED", 'fontWeight': 'bold'}, tab_id="incid_dchosp")
            ],
            id="tabs",
            active_tab="hosp",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

#using the callback tab bootstrap

@callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):

    if active_tab == "hosp":

        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=fig_last_6months_hosp_up_to_now_groupby,
                             config={'displaylogo': False},
                             style={'padding-bottom': '1%'}),
                    xs={'size': 12, 'offset': 0, 'order:': 0},
                    lg={'size': 6, 'offset': 0, 'order:': 1},
                    xl={'size': 6, 'offset': 0, 'order:': 1},

                ),

                dbc.Col(
                    dcc.Graph(figure=figTableGroupBy_hosp,
                              config={'displaylogo': False},
                              style={'padding-right': '10%', 'padding-top': '2%'}),
                    xs={'size': 12, 'offset': 0, 'order:': 0},
                    lg={'size': 6, 'offset': 0, 'order:': 2},
                    xl={'size': 6, 'offset': 0, 'order:': 2},
                ),

                dcc.Graph(figure=hosp_up_to_now, config={'displaylogo': False}),

            ]
        )


    elif active_tab == "rea":

        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=fig_last_6months_rea_up_to_now_groupby,
                             config={'displaylogo': False},
                             style={'padding-bottom': '1%'}),
                    xs={'size': 12, 'offset': 0, 'order:': 0},
                    lg={'size': 6, 'offset': 0, 'order:': 1},
                    xl={'size': 6, 'offset': 0, 'order:': 1},

                ),
                dbc.Col(
                    dcc.Graph(figure=figTableGroupBy_rea,
                              config={'displaylogo': False},
                              style={'padding-right': '10%', 'padding-top': '2%'}),
                    xs={'size': 12, 'offset': 0, 'order:': 0},
                    lg={'size': 6, 'offset': 0, 'order:': 2},
                    xl={'size': 6, 'offset': 0, 'order:': 2},
                ),

                dcc.Graph(figure=rea_up_to_now, config={'displaylogo': False}),

            ]
        )


    elif active_tab == "incid_rad":

        return dbc.Row(
            [
               dbc.Col(
                   dcc.Graph(figure=fig_last_6months_incid_rad_up_to_now_groupby,
                             config={'displaylogo': False},
                             style={'padding-bottom': '1%'}),
                   xs={'size': 12, 'offset': 0, 'order:': 0},
                   lg={'size': 6, 'offset': 0, 'order:': 1},
                   xl={'size': 6, 'offset': 0, 'order:': 1},
               ),

                dbc.Col(
                    dcc.Graph(figure=figTableGroupBy_incid_rad,
                              config={'displaylogo': False},
                              style={'padding-right': '10%', 'padding-top': '2%'}),
                    xs={'size': 12, 'offset': 0, 'order:': 0},
                    lg={'size': 6, 'offset': 0, 'order:': 2},
                    xl={'size': 6, 'offset': 0, 'order:': 2},

                ),

                dcc.Graph(figure=incid_rad_up_to_now, config={'displaylogo': False}),

            ]
        )

    elif active_tab == "incid_dchosp":

        return dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=fig_last_6months_incid_dchosp_up_to_now_groupby,
                              config={'displaylogo': False},
                              style={'padding-bottom': '1%'}),
                    xs={'size': 12, 'offset': 0, 'order:': 0},
                    lg={'size': 6, 'offset': 0, 'order:': 1},
                    xl={'size': 6, 'offset': 0, 'order:': 1},
                ),

                dbc.Col(
                    dcc.Graph(figure=figTableGroupBy_incid_dchosp,
                              config={'displaylogo': False},
                              style={'padding-right': '10%', 'padding-top': '2%'}),
                    xs={'size': 12, 'offset': 0, 'order:': 0},
                    lg={'size': 6, 'offset': 0, 'order:': 2},
                    xl={'size': 6, 'offset': 0, 'order:': 2},
                ),

                dcc.Graph(figure=incid_dchosp_up_to_now, config={'displaylogo': False}),
            ]
        )

    else:
        return []