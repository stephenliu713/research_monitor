import research_monitor_func as func
import os
import search_string
import get_KITopen
import clean_report
import calc_cites_delta
import get_data_network
import get_network
import get_wordcloud
import search_string_im
import get_KITopen_im
import predict_tag

def main():
    # create folder if it does not exist yet
    path_lastqtr = func.get_abspath_folder_lastquarter()
    print(path_lastqtr)
    if not os.path.exists(path_lastqtr):
        os.makedirs(path_lastqtr)

    # execute relative modules
    #   get and clean data
    search_string.main()
    search_string_im.main()
    get_KITopen.main()
    get_KITopen_im.main()
    clean_report.main()

    # predict tag
    predict_tag.main()

    #   calculate PoPCites.scv
    while os.path.exists(path=func.get_abspath_folder_lastquarter()+"PoPCites.csv") == False:
        pause = input("Please add PoPCites.csv of {} under the path: {} and then enter any values to continue".format(func.get_last_2_quarters(),func.get_abspath_folder_lastquarter()))
    calc_cites_delta.main()

    #   get author relationship and network
    get_data_network.main()
    get_network.main()

    #   get wordcloud
    get_wordcloud.main()

if __name__ == '__main__':
    main()