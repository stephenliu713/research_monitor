import pandas as pd
import numpy as np
import re
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
import os
from keras.models import load_model
import research_monitor_func as func


def replace_ger_char(df): #replace some special german characters with english character
    df = df.str.replace('ä','ae')
    df = df.str.replace('ö', 'oe')
    df = df.str.replace('ü', 'ue')
    df = df.str.replace('ß', 'ss')
    return df

def isIncludeKeyWord(detailinfo,tmp_keyword):
    if  -1 != detailinfo.find(tmp_keyword):
        pattern_str='(^'+tmp_keyword+'$)|(^'+tmp_keyword+'(\W+).*)|(.*(\W+)'+tmp_keyword+'$)|(.*(\W+)'+tmp_keyword+'(\W+).*)'
        m = re.match(r''+pattern_str+'', detailinfo)
        if m:
            return 1
    return 0

def main():
    print("Training machine learning model...")

    path_namelist = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\researchers list\\researchers list {}.xlsx'.format(func.get_last_2_quarters(connector='-'))
    namelist = pd.read_excel(path_namelist)
    firstname = namelist['First name']
    lastname = namelist['Last name']
    fullname_list = lastname+', '+firstname  # format example: "Jasper, Feine"
    pub_typ_list = ['Proceedingsbeitrag','Zeitschriftenaufsatz']

    path_training = 'training set.xlsx'
    df_training = pd.read_excel(path_training, sheet_name='training')
    author = df_training['Autor']
    pub_typ = df_training['Publikationstyp']
    quelle = df_training['Quelle']
    classes = df_training['tag_pub']
    author_eng = replace_ger_char(author) # clean the data, transfer all the german characters to english

    path_input = 'ML input.xlsx'
    df_input = pd.read_excel(path_input,sheet_name='top125')['Input']

    # **** quelle ****
    x = np.zeros(shape=(len(quelle),len(df_input)),dtype=np.int,order='C')
    for i in range(len(author_eng)):
        for h in range(len(df_input)):
            if quelle[i].find(df_input[h]) != -1:
                x[i,h] = 1

    tag_file =  os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\MasterData\master_data_ranking_2020.xlsx'
    publication = pd.read_excel(tag_file, sheet_name='Publications')
    kit_tag = publication['kit_tag']

    y = np.zeros(shape=(len(author_eng), len(kit_tag)), dtype=np.int, order='C') # result, there is only one '1' in each row to show the result
    z = np.zeros(shape=(len(author_eng)), dtype=np.int, order='C')
    sum = 0
    for i in range(len(author_eng)):
        for j in range(len(kit_tag)):
            if classes[i] == kit_tag[j]:
                y[i][j] = 1
                z[i] = j
                break
            if j == len(kit_tag) - 1:
                z[i] = -1
                sum = sum + 1
    x_train = np.zeros(shape=(len(author_eng)-sum, len(x[0])), dtype=np.int, order='C')
    x_test = np.zeros(shape=(sum, len(x[0])), dtype=np.int, order='C')
    y_train = np.zeros(shape=(len(author_eng)-sum, len(y[0])), dtype=np.int, order='C')
    y_test = np.zeros(shape=(sum, len(y[0])), dtype=np.int, order='C')
    index_train = 0
    index_test = 0
    for i in range(len(author_eng)):
        if z[i] == -1:
            x_test[index_test] = x[i]
            y_test[index_test] = y[i]
            index_test = index_test + 1
        else:
            x_train[index_train] = x[i]
            y_train[index_train] = y[i]
            index_train = index_train + 1

    input_sh = len(x[0])
    output_len = len(kit_tag)
    model = Sequential()
    model.add(Dense(128, input_shape=(input_sh,), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(output_len, activation='softmax'))

    opt = keras.optimizers.Adam(learning_rate=0.01)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=200, batch_size=6)
    x_p = model.evaluate(x_train, y_train)
    save_dir = 'tag_model.h5'
    model.save(save_dir)

    print("Successfully saved model under the same folder")

if __name__ == '__main__':
    main()

