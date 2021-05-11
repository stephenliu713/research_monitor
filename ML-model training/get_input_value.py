import pandas as pd
import research_monitor_func as func
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import re
import os

def main():
    print("Getting input value from latest report...")

    path_report = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\data\{}\\report_{}_clean.xlsx'.format(func.get_last_2_quarters(connector='-'),func.get_last_2_quarters())
    df_report = pd.read_excel(path_report)
    quelle = df_report['Quelle']

    # merge quelle into one string
    text_quelle = ''
    for single_que in quelle:
        text_quelle += single_que
    # print(text_quelle)

    # delete numbers and punctuation, keep letters only
    quelle_letters_only = re.sub("[^a-zA-Z]", " ", text_quelle)
    # print(quelle_letters_only)

    # tokenize and filter text
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(quelle_letters_only)
    filtered_text = [w for w in tokens if not w in stop_words]

    # top 200
    fdist = FreqDist(filtered_text)
    tops = fdist.most_common(200)
    df_tops = pd.DataFrame(tops)
    print(df_tops)
    df_tops.to_excel('freq_words_top{}.xlsx'.format(len(df_tops)))

    print("Successfully saved most frequent words into 'freq_words_top{}.xlsx' under this folder".format(len(df_tops)))


if __name__ == '__main__':
    main()
