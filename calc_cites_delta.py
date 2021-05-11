import pandas as pd
import research_monitor_func as func
import datetime
import numpy as np
import os

def main():
    #calc the 'Total citations'
    print("Calculating relative data of PoPCites.csv...")

    last2quarters_hyphen = func.get_last_2_quarters(connector='-')
    path_pop = func.get_abspath_pop()
    #     # calc total citations
    df_pop = pd.read_csv(path_pop)
    popcites = df_pop.loc[(df_pop['Year'] > 2009 ),['Year','Authors','Title','Cites']] # filter conditions: Year > 2009
    popcites['Title'] = popcites['Title'].str.lower()
    popcites['Year'] = popcites['Year'].astype(int)
    popcites_remove_duplicate = popcites.drop_duplicates(subset = 'Title')
    total_cites = popcites_remove_duplicate['Cites'].sum()
    path_pop_new = os.path.abspath('')+'\data\{}\PoPCites clean.csv'.format(last2quarters_hyphen)
    popcites_remove_duplicate.to_csv(path_pop_new,index=False,encoding='utf_8_sig')

    # automatically edit 'PoPCites_delta'
    halfyear_before_today = datetime.date.today()-datetime.timedelta(180)
    path_delta_pre = os.path.abspath('') + '\data\{}\citation_delta.csv'.format(func.get_last_2_quarters(date=halfyear_before_today,connector='-'))
    path_delta =os.path.abspath('')+'\data\{}\citation_delta.csv'.format(last2quarters_hyphen)
    df_delta = pd.read_csv(path_delta_pre,encoding='utf-8-sig')
    df_delta.replace(np.nan,0,inplace=True)
    df_delta.replace(np.inf,0,inplace=True)
    querydate_quarter = func.get_last_quarter(connector='_')
    querydate_quarter_pre = func.get_last_quarter(halfyear_before_today,connector='_')
    total_cites_pre = df_delta[df_delta['QueryDateQuarter']== querydate_quarter_pre].iloc[0]['Cites']
    # idx_delta = df_delta.index[df_delta['QueryDateQuarter'] == querydate_quarter_pre].to_list()[0] + 1
    delta_cites = total_cites - int(total_cites_pre)
    df_newrow = pd.DataFrame(data=[[querydate_quarter,total_cites,delta_cites]],columns=['QueryDateQuarter','Cites','delta'])
    if df_newrow['QueryDateQuarter'].isin(df_delta['QueryDateQuarter']).bool() == False:
        df_delta = df_delta.append(df_newrow,ignore_index=True)
    df_delta.to_csv(path_delta,index=False,encoding='utf-8-sig')

    print("Successfully calculated data and saved under path: {}".format(path_delta))

if __name__ == '__main__':
    main()
