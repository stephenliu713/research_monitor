
import pandas as pd
import numpy as np
from keras.models import load_model
import research_monitor_func as func


def main():
    print("Predicting blank KIT-tags in the report...")

    path_report_clean = func.get_abspath_folder_lastquarter() + 'report_{}_clean.xlsx'.format(
        func.get_last_2_quarters(connector=''))
    # path_report_clean = "ML-model training/test set.xlsx"
    df_report = pd.read_excel(path_report_clean)
    df_blank = df_report.loc[(df_report['KIT-Tagging'].isnull()), ['Publikationstyp','Autor','Quelle']]
    df_blank = df_blank.reset_index(drop=True)

    if len(df_blank) > 0:
        author_eng = func.replace_ger_char(df_blank['Autor'])
        # pub_typ = df_blank['Publikationstyp']
        quelle = df_blank['Quelle']
        # print(quelle)

        path_tag = 'MasterData/master_data_ranking_2020.xlsx'
        publication = pd.read_excel(path_tag, sheet_name='Publications')
        kit_tag = publication['kit_tag']

        path_input = 'ML-model training/ML input.xlsx'
        df_input = pd.read_excel(path_input,sheet_name='top125')['Input'] #change version of input list
        # # **** quelle ****
        x = np.zeros(shape=(len(quelle), len(df_input)), dtype=np.int, order='C')
        for i in range(len(author_eng)):
            for h in range(len(df_input)):
                if quelle[i].find(df_input[h]) != -1:
                    x[i,h] = 1

        # ML prediction
        path_model = 'ML-model training/tag_model.h5'
        model = load_model(path_model)
        x_t = model.predict(x)
        df_top3 = pd.DataFrame(columns=['No.1', 'No.2', 'No.3'])
        for i in range(len(x_t)):
            top_k = 3
            arr = x_t[i]
            top_k_idx = arr.argsort()[-top_k:][::-1]
            df_newrow = pd.DataFrame(data=[[kit_tag[top_k_idx[0]],kit_tag[top_k_idx[1]],kit_tag[top_k_idx[2]],]],columns=['No.1','No.2','No.3'])
            df_top3 = df_top3.append(df_newrow, ignore_index=True)

        # save result
        path_predict = func.get_abspath_folder_lastquarter()+'tag_prediction_{}.xlsx'.format(func.get_last_2_quarters())
        df_top3 = pd.concat([df_blank['Quelle'],df_top3],axis=1)
        df_top3.to_excel(path_predict, index=False)

        print(df_top3)
        print("Successfully saved predictions under path: {}".format(path_predict))

    else:
        print("There aren't any blank KIT-tags in the report")

if __name__ == '__main__':
    main()