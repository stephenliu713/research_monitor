import wordcloud
import pandas as pd
import research_monitor_func as func
from nltk.corpus import stopwords
import datetime
import os

def get_wordcloud(path_open,path_to_file,width_value=1000,height_value=1000,stopwords_custom = {}):
    f = open((path_open), encoding='utf-8')
    txt_title = f.read()
    stop_words = set(stopwords.words('english'))
    stop_words.update(stopwords_custom)
    w = wordcloud.WordCloud(width=width_value, height=height_value, background_color='white', stopwords=stop_words,font_path='arial')
    w.generate(txt_title)
    w.to_file(path_to_file)

def main():
    print("Generating wordclouds of paper titles...")

    # check folder exists
    path_report_title = func.get_abspath_folder_lastquarter()+'report title'
    if not os.path.exists(path_report_title):
        os.makedirs(path_report_title)

    # get report and generate wordcloud of issd report
    path_report_issd = func.get_abspath_folder_lastquarter()+'\\report_{}_clean.xlsx'.format(func.get_last_2_quarters())
    df_report_issd = pd.read_excel(path_report_issd)
    df_title_issd = df_report_issd['Titel']
    df_title_issd.to_csv(path_report_title+'\\report_title_issd_{}.txt'.format(func.get_last_2_quarters()),index=False)
    path_title_issd = path_report_title+'\\report_title_issd_{}.txt'.format(func.get_last_2_quarters())
    path_wordcloud_issd = func.get_abspath_folder_lastquarter()+'wordcloud_issd.png'

    get_wordcloud(path_title_issd,path_wordcloud_issd)

    # get report and report from last years
    lastyr = datetime.datetime.now().year - 1
    for i in range(4):
        if i <= 3:
            df_title_issd_tmp = df_report_issd.loc[(df_report_issd['Erscheinungsjahr'] == lastyr-i),['Titel']]
        elif i == 4:
            df_title_issd_tmp = df_report_issd.loc[(df_report_issd['Erscheinungsjahr'] <= (lastyr-i)), ['Titel']]
        df_title_issd_tmp.to_csv(path_report_title+'\\report_title_issd_{}.txt'.format(lastyr-i),index=False)
        path_title_issd_tmp = path_report_title+'\\report_title_issd_{}.txt'.format(lastyr-i)
        path_wordcloud_issd_tmp = func.get_abspath_folder_lastquarter() + 'wordcloud_issd_{}.png'.format(lastyr-i)

        get_wordcloud(path_title_issd_tmp, path_wordcloud_issd_tmp,width_value=1000,height_value=600)

    #get report and generate .txt of iism report
    path_report_im = func.get_abspath_folder_lastquarter() + 'report_im_{}.xlsx'.format(func.get_last_2_quarters())
    df_report_issd = pd.read_excel(path_report_im, sheet_name='Publikationen')
    df_title_issd = df_report_issd['Titel']
    df_title_issd.to_csv(path_report_title+'\\report_title_im_{}.txt'.format(func.get_last_2_quarters()),index=False)
    path_title_iism = path_report_title+'\\report_title_im_{}.txt'.format(func.get_last_2_quarters())
    path_wordcloud_im = func.get_abspath_folder_lastquarter() + 'wordcloud_im.png'

    get_wordcloud(path_title_iism, path_wordcloud_im)

    print("Successfully generated wordclous of paper titles")

if __name__ == '__main__':
    main()