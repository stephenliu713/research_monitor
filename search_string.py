import requests
from bs4 import BeautifulSoup
import pandas as pd
import research_monitor_func as func
import os
import datetime

def main():
    print("Getting search string of ISSD ...")

    # get latest team list
    url_team = "https://issd.iism.kit.edu/team.php"
    html_team = func.get_html(url_team)
    soup_team = BeautifulSoup(html_team,"html.parser")
    last_name = []
    first_name = []
    for table in soup_team.find_all('table',class_="collapseTable"):
        caption = table.find('caption',align = 'top')
        # select only prof., postdocs, doctoral researcher and junior research
        if (str(caption.text).find("Professor and Chairperson") != -1) \
            or (str(caption.text).find("PostDocs") != -1)\
            or (str(caption.text).find("Doctoral Researchers") != -1)\
            or (str(caption.text).find("Junior Researchers") != -1)\
            :
            for tr in table.find_all('tr'):
                for a in tr.find_all('a',itemprop='name'):
                    name = str(a.text)
                    temp = name.split(", ")
                    last_name.append(temp[0])
                    first_name.append(temp[1])
    namelist = {'Last name':last_name,'First name':first_name}
    df_team_de = pd.DataFrame(namelist)
    df_team_now = df_team_de.copy()
    df_team_now = func.replace_ger_char(df_team_now)

    # add team members who have already left (based on previous list)
    path_team_previous = os.path.abspath('') + \
                         '\\researchers list\\researchers list {}.xlsx'.format(func.get_last_2_quarters(date=datetime.date.today() - datetime.timedelta(180),connector='-'))
    df_team_previous = pd.read_excel(path_team_previous)
    df_team = pd.concat([df_team_now,df_team_previous],verify_integrity=True,ignore_index=True)

    # get HoF list
    path_hof = os.path.abspath('') + '\\researchers list\Hall of Fame.xlsx'
    df_hof = pd.read_excel(path_hof,sheet_name='HoF')

    # concat team list and HoF list and remove duplicates
    df_total = pd.concat([df_team,df_hof],verify_integrity=True,ignore_index=True)
    df_total = df_total.drop_duplicates()

    # save list and search string
    last2quarter_hyphen = func.get_last_2_quarters(connector='-')
    file_name = 'researchers list {}.xlsx'.format(last2quarter_hyphen)
    path_list = os.path.abspath('') + '\\researchers list\{}'.format(file_name)
    df_total.to_excel(excel_writer=path_list,index=False)

    # add german name to the dataframe
    df_search = df_total.copy()
    last_name_flag_de = df_team_de['Last name'].isin(df_total['Last name'])
    first_name_flag_de = df_team_de['First name'].isin(df_total['First name'])
    for i in range(len(df_team_de)):
        if (last_name_flag_de[i]==False) or (first_name_flag_de[i]==False):
            df_search = df_search.append(df_team_de.loc[i],ignore_index=True)

    # generate search string and save it to txt-file
    search_str = ''
    for i in range(len(df_search)):
        if (str(df_search['Last name'][i]).find(' ')!= -1) or (str(df_search['First name'][i]).find(' ')!= -1):
            search_str +='"'+ df_search['Last name'][i] + ', '+ df_search['First name'][i] + '"'
        else:
            search_str += df_search['Last name'][i] + ', '+ df_search['First name'][i]
        if i != (len(df_search)-1):
            search_str += ' OR '
    path_search_str = os.path.abspath('') + '\\researchers list\search string {}.txt'.format(last2quarter_hyphen)
    with open(path_search_str,"w",encoding='utf-8') as f:
        f.write(search_str)

    print("Successfully created file of search string under path: {}".format(path_search_str))

if __name__ == '__main__':
    main()