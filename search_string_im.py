import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import research_monitor_func as func



def main():
    print("Getting search string of IM ...")

    # get team list
    url_team = "https://im.iism.kit.edu/team.php"
    html_team = func.get_html(url_team)
    soup_team = BeautifulSoup(html_team,"html.parser")
    last_name = []
    first_name = []
    for table in soup_team.find_all('table',class_="collapseTable"):
        caption = table.find('caption',align = 'top')
        # select only prof., postdocs, doctoral researcher and junior research
        if (str(caption.text).find("Leitung") != -1) \
            or (str(caption.text).find("Forschungsgruppenleitung") != -1)\
            or (str(caption.text).find("Wissenschaftliche Mitarbeiter*Innen am KIT und FZI") != -1)\
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
    df_team = df_team_de.copy()
    df_team = func.replace_ger_char(df_team)

    df_search = df_team.copy()
    last_name_flag_de = df_team_de['Last name'].isin(df_team['Last name'])
    first_name_flag_de = df_team_de['First name'].isin(df_team['First name'])
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
    path_search_str = os.path.abspath('')+'\\researchers list\search string_im {}.txt'.format(func.get_last_2_quarters(connector='-'))
    with open(path_search_str,"w",encoding='utf-8') as f:
        f.write(search_str)

    print("Successfully created file of search string under path: {}".format(path_search_str))

if __name__ == '__main__':
    main()