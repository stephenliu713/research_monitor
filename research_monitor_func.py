import datetime
import pandas as pd
import numpy as np
import re
import os
import requests

# get year and quarter like '2020-Q3u4'
def get_last_2_quarters(date=datetime.date.today(),connector = ''):
    year = date.year
    month = date.month
    if month >= 7:
        text = str(year)+ connector + 'Q1u2'
    else:
        last_year = year -1
        text = str(last_year)+ connector + 'Q3u4'
    return text

def get_last_quarter(date=datetime.date.today(),connector = ''):
    year = date.year
    month = date.month
    if month >= 7:
        text = str(year)+ connector + 'Q2'
    else:
        last_year = year -1
        text = str(last_year)+ connector + 'Q4'
    return text

def get_abspath_cites_delta():
    path_cites = os.path.abspath('')+'\data\{}\citation_delta.csv'.format(get_last_2_quarters(connector='-'))
    return path_cites

def get_abspath_pop():
    path_pop = os.path.abspath('')+'\data\{}\PoPCites.csv'.format(get_last_2_quarters(connector='-'))
    return path_pop

def get_abspath_report():
    path_report = os.path.abspath('')+'\data\{}\{}.xlsx'.format(get_last_2_quarters(connector='-'), 'report_' + get_last_2_quarters())
    return path_report

def get_abspath_folder_lastquarter():
    path_folder = os.path.abspath('')+'\data\{}\\'.format(get_last_2_quarters(connector='-'))
    return path_folder

def get_abspath_researcher():
    path_researcher = os.path.abspath('')+'\\researchers list\\researchers list {}.xlsx'.format(get_last_2_quarters(
        connector='-'))
    return path_researcher

def get_html(url):
    headers = {
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    html = response.text
    return html

"""
url explaination

url = 'https://publikationen.bibliothek.kit.edu/auswertungen/report.php?external_publications=all&open_access_availability=do_not_care&full_text=do_not_care&key_figures=number_of_publications&year=2010-&consider_online_advance_publication_date=true&consider_additional_pof_structures=false&row=type&column=year&' 
      authors=Maedche%2C%20Alexander%20OR%20Gnewuch%2C%20Ulrich%20OR%20Nadj%2C%20Mario%20OR%20Toreini%2C%20Peyman%20OR%20Benke%2C%20Ivo%20OR%20Feine%2C%20Jasper%20OR%20Gau%2C%20Michael%20OR%20Haug%2C%20Saskia%20OR%20Knaeble%2C%20Merlin%20OR%20Loewe%2C%20Nico%20OR%20
      %22Meza%20Martinez%2C%20Miguel%20Angel%22
      %20OR%20Michalczyk%2C%20Sven%20OR%20Rietz%2C%20Tim%20OR%20Ruoff%2C%20Marcel%20OR%20Scheu%2C%20Sven%20OR%20Schloss%2C%20Daniel%20OR%20Seiffer%2C%20Anja%20OR%20Langner%2C%20Moritz%20OR%20Schulz%2C%20Melanie%20OR%20Schwarzenboeck%2C%20Jonathan%20OR%20Botzenhardt%2C%20Achim%20OR%20Heckmann%2C%20Carl%20OR%20Graupner%2C%20Enrico%20OR%20Kahrau%2C%20Felix%20OR%20Hadasch%2C%20Frank%20OR%20Meth%2C%20Hendrik%20OR%20Lauterbach%2C%20Jens%20OR%20Berner%2C%20Martin%20OR%20Kretzer%2C%20Martin%20OR%20Koppenhagen%2C%20Norbert%20OR%20Gass%2C%20Oliver%20OR%20Schacht%2C%20Silvia%20OR%20Morana%2C%20Stefan%20OR%20Li%2C%20Ye%20OR%20Fleig%2C%20Christian%20OR%20Liu%2C%20Xuanhui%20OR%20Rissler%2C%20Rephael%20OR%20Hummel%2C%20Dennis%20OR%20Morschheuser%2C%20Benedikt%20OR%20Haake%2C%20Philip%20OR%20Mueller%2C%20Benjamin%20OR%20Werder%2C%20Karl%20OR%20
      M%C3%A4dche%2C%20Alexander
      %20OR%20Kn%C3%A4ble%2C%20Merlin%20OR%20
      Schlo%C3%9F%2C%20Daniel%20OR%20
      Schwarzenb%C3%B6ck%2C%20Jonathan
      &in_opac=false&format=excel&publications=true'

',' = %2C%20
' ' = %20
'"' = %22
'ä' = %C3%A4
'ö' = %C3%B6
'ß' = %C3%9F

"""
def replace_name_url(str1):
    str2 = str1
    str2 = str2.replace(',','%2C%20')
    str2 = str2.replace(' ','%20')
    str2 = str2.replace('"','%22')
    str2 = str2.replace('ä','%C3%A4')
    str2 = str2.replace('ö','%C3%B6')
    str2 = str2.replace('ß','%C3%9F')
    return str2

# clean the data
def clean_csv(filepath_popcites,savepath):
    # read csv
    df = pd.read_csv(filepath_popcites,engine='python',encoding='utf-8-sig')
    df.replace(np.nan,0,inplace=True)
    df.replace(np.inf,0,inplace=True)

    # clean 'QueryDate'
    query_date = df['QueryDate'][0]
    yyyy = query_date[0:4]
    mm = query_date[5:7]
    dd = query_date[8:10]
    query_date_clean = dd + '/' + mm + '/' + yyyy
    df.iloc[:,9] = query_date_clean     # column[9] is 'QueryDate'

    # clean 'Year'
    df[['Year']] = df[['Year']].astype('int')

    # save cleaned data as new csv
    df.to_csv(savepath,index=False,encoding='utf-8-sig')

def replace_ger_char(df): #replace some special german characters with english character
    # df = df.str.replace('ä','ae')
    # df = df.str.replace('ö', 'oe')
    # df = df.str.replace('ü', 'ue')
    # df = df.str.replace('ß', 'ss')
    df.replace(to_replace='ä',value='ae',regex=True,inplace=True)
    df.replace(to_replace='ö', value='oe', regex=True, inplace=True)
    df.replace(to_replace='ü', value='ue', regex=True, inplace=True)
    df.replace(to_replace='ß', value='ss', regex=True, inplace=True)
    return df

def isIncludeKeyWord(detailinfo,tmp_keyword):
    if  -1 != detailinfo.find(tmp_keyword):
        pattern_str='(^'+tmp_keyword+'$)|(^'+tmp_keyword+'(\W+).*)|(.*(\W+)'+tmp_keyword+'$)|(.*(\W+)'+tmp_keyword+'(\W+).*)'
        m = re.match(r''+pattern_str+'', detailinfo)
        if m:
            return 1
    return 0

def get_fullname_list():
    namelist = pd.read_excel(get_abspath_researcher())
    firstname = namelist['First name']
    lastname = namelist['Last name']
    fullname_list = lastname + ', ' + firstname
    return fullname_list

def main():
    pass

if __name__ == '__main__':
    main()
