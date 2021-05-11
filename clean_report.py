import pandas as pd
import research_monitor_func as func
import os
import numpy as np

def clean_report(path_report,path_report_clean):
    df_report = pd.read_excel(path_report, sheet_name='Publikationen')
    # [A:F]
    df_clean = df_report.loc[
        (df_report['Erscheinungsjahr'] > 2009), ['Erscheinungsjahr', 'Publikationstyp', 'Titel', 'Autor', 'KIT-Tagging',
                                                 'Quelle']]
    df_clean = df_clean.loc[(df_report['Publikationstyp'].isin(['Zeitschriftenaufsatz', 'Proceedingsbeitrag']))]
    df_clean = df_clean.reset_index(drop=True)
    df_toadd = pd.DataFrame(columns=['kd2lab_tag', 'tag_pub', 'ranking', 'changed 2020', 'Journal', 'Publication Type'])
    df_clean = pd.concat([df_clean, df_toadd], ignore_index=True)
    # [G]kd2lab_tag
    df_kittag = df_clean['KIT-Tagging'].str.split(pat='\\n')
    df_kittag.fillna(value='', inplace=True)
    kd2lab = pd.DataFrame()
    for i in range(len(df_kittag)):
        flag = False
        for text in df_kittag[i]:
            if text.find('kd2lab') != -1:
                flag = True
        df_clean.loc[i, 'kd2lab_tag'] = flag
    # [H]tag_pub, [I]ranking, [L]Publication Type
    path_ranking = os.path.abspath('') + '\MasterData\master_data_ranking_2020.xlsx'
    master = pd.read_excel(path_ranking, sheet_name='Publications')
    for i in range(len(df_kittag)):
        tag_pub = ''
        ranking = ''
        publ_typ = ''
        for text in df_kittag[i]:
            for j in range(len(master['kit_tag'])):
                if master.loc[j, 'kit_tag'].find(text) != -1:
                    tag_pub = master.loc[j, 'kit_tag']
                    ranking = master.loc[j, 'ranking']
                    publ_typ = master.loc[j, 'Publication Type']
        df_clean.loc[i, 'tag_pub'] = tag_pub
        df_clean.loc[i, 'ranking'] = ranking
        df_clean.loc[i, 'Publication Type'] = publ_typ
    # # [K] Journal
    for i in range(len(df_kittag)):
        flag = False
        for text in df_kittag[i]:
            if text.find('Journal') != -1:
                flag = True
        df_clean.loc[i, 'Journal'] = flag
    df_clean.to_excel(path_report_clean, index=False)

def main():
    print('Cleaning Excel file from KIT Open...')

    # clean report of ISSD
    path_report_issd = func.get_abspath_report()
    path_report_clean_issd = func.get_abspath_folder_lastquarter() + 'report_{}_clean.xlsx'.format(
        func.get_last_2_quarters(connector=''))
    clean_report(path_report_issd,path_report_clean_issd)
    print('Successfully created cleaned report of ISSD under path: {}'.format(path_report_clean_issd))

    # clean report of IISM
    path_report_iism = func.get_abspath_folder_lastquarter()+'report_im_{}.xlsx'.format(func.get_last_2_quarters())
    path_report_clean_iism = func.get_abspath_folder_lastquarter() + 'report_im_{}_clean.xlsx'.format(
        func.get_last_2_quarters(connector=''))
    clean_report(path_report_iism, path_report_clean_iism)
    print('Successfully created cleaned report of IM under path: {}'.format(path_report_clean_issd))

if __name__ == '__main__':
    main()