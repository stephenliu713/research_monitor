import requests
import os
import xlwt
import research_monitor_func as func

def main():
    print("Getting data of ISSD from KIT-Open...")

    last2quarter_hyphen = func.get_last_2_quarters(connector='-')
    path_search_str = os.path.abspath('') + '\\researchers list\search string {}.txt'.format(last2quarter_hyphen)
    with open(path_search_str, 'r',encoding='utf-8') as f:
        search_str = f.read()
    url_author_str = func.replace_name_url(search_str)
    url = 'https://publikationen.bibliothek.kit.edu/auswertungen/report.php?external_publications=all&open_access_availability=do_not_care&full_text=do_not_care&key_figures=number_of_publications&year=2010-&consider_online_advance_publication_date=true&consider_additional_pof_structures=false&row=type&column=year&authors='\
            + url_author_str\
            + '&in_opac=false&format=excel&publications=true'
    # print(url)
    r = requests.get(url, allow_redirects=True)
    path_report = func.get_abspath_report()
    with open(path_report, 'wb') as f:
        f.write(r.content)

    print("Successfully saved data of ISSD into Excel file under path: {}".format(path_report))

if __name__ == '__main__':
    main()

# r = requests.get(url, allow_redirects=True)
#
# path = 'data/2020-Q3u4/test.xlsx'
# with open(path, 'wb') as f:
#     f.write(r.content)