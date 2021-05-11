import pandas as pd
import numpy as np
import os
import research_monitor_func as func

def main():
    print("Getting data of authors...")

    # get namelist of authors
    path_namelist = func.get_abspath_researcher()
    namelist = pd.read_excel(path_namelist)
    firstname = namelist['First name']
    lastname = namelist['Last name']
    fullname_list = lastname+', '+firstname  # format example: "Jasper, Feine"
    # print(fullname_list)

    # read report and get author list
    path_report = func.get_abspath_folder_lastquarter()+\
                  'report_{}_clean.xlsx'.format(func.get_last_2_quarters(connector=''))
    df_report = pd.read_excel(path_report)
    df_author = df_report['Autor']
    df_author_eng = func.replace_ger_char(df_author)
    # print(df_author_eng)

    # get matrix
    x = np.zeros(shape=(len(df_author_eng),len(fullname_list)),dtype=np.int,order='C')
    for i in range(len(df_author_eng)):
        for h in range(len(fullname_list)):
            if df_author_eng[i].find(fullname_list[h]) != -1:
                x[i,h] = 1
    # print(x)

    # merge result and generate .xlsx
    df_result = pd.DataFrame(data=x,columns=fullname_list)
    # print(df_result)
    path_data_network = os.path.abspath('') + '\data\{}\data_network_{}.xlsx'.format(func.get_last_2_quarters(connector='-'),
                                                                                     func.get_last_2_quarters())
    df_result.to_excel(path_data_network, index=False)

    print("Successfully saved author data under path: {}".format(path_data_network))

if __name__ == '__main__':
    main()