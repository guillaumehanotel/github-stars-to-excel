import requests
import json
from time import time
from pyexcelerate import Workbook
from datetime import date

today = date.today()

def get_github_stars(username, token):
    headers = {'Authorization': 'token ' + token}

    per_page = 100
    stars = []

    for page in range(1, 15):
        response = requests.get(f"https://api.github.com/users/{username}/starred?per_page={per_page}&page={page}",
                                headers=headers)
        if response.status_code == 200:
            raw_stars_batch = json.loads(response.content)
            if len(raw_stars_batch) != 0:
                def apply(raw_star):
                    try:
                        return {
                            'id': raw_star['id'],
                            'name': raw_star['name'],
                            'full_name': raw_star['full_name'],
                            'url': raw_star['html_url'],
                            'stargazers_count': raw_star['stargazers_count'],
                            'language': raw_star['language'],
                            'archived': raw_star['archived'],
                            'disabled': raw_star['disabled'],
                            'forks_count': raw_star['forks_count'],
                            'open_issues_count': raw_star['open_issues_count'],
                            'license': raw_star['license']['name'],
                            'created_at': raw_star['created_at'],
                            'updated_at': raw_star['updated_at'],
                        }
                    except TypeError:
                        pass
                stars.extend(list(map(apply, raw_stars_batch)))
        else:
            print(response.content)
    return stars

def write_stars_to_xlsx(username, stars):
    wb_stars = Workbook()
    ws_stars = wb_stars.new_sheet("Sheet1")
    formatted_date = today.strftime("%y%m%d")
    wb_stars_path = f"./{username} - Github Stars {formatted_date}.xlsx"

    ws_stars[1][1] = "id"
    ws_stars[1][2] = "name"
    ws_stars[1][3] = "full_name"
    ws_stars[1][4] = "url"
    ws_stars[1][5] = "stargazers_count"
    ws_stars[1][6] = "language"
    ws_stars[1][7] = "archived"
    ws_stars[1][8] = "disabled"
    ws_stars[1][9] = "forks_count"
    ws_stars[1][10] = "open_issues_count"
    ws_stars[1][11] = "license"
    ws_stars[1][12] = "created_at"
    ws_stars[1][13] = "updated_at"

    row_counter = 2
    for count, star in enumerate(stars):
        if star is not None:
            ws_stars[row_counter][1] = star['id']
            ws_stars[row_counter][2] = star['name']
            ws_stars[row_counter][3] = star['full_name']
            ws_stars[row_counter][4] = star['url']
            ws_stars[row_counter][5] = star['stargazers_count']
            ws_stars[row_counter][6] = star['language']
            ws_stars[row_counter][7] = star['archived']
            ws_stars[row_counter][8] = star['disabled']
            ws_stars[row_counter][9] = star['forks_count']
            ws_stars[row_counter][10] = star['open_issues_count']
            ws_stars[row_counter][11] = star['license']
            ws_stars[row_counter][12] = star['created_at']
            ws_stars[row_counter][13] = star['updated_at']
            row_counter = row_counter + 1
        else:
            print(count)

    wb_stars.save(wb_stars_path)

def main():

    username = 'guillaumehanotel'
    # https://github.com/settings/tokens/new
    token = 'XXXXXXXXXXXXXXXXXXX'

    stars = get_github_stars(username, token)
    write_stars_to_xlsx(username, stars)


if __name__ == '__main__':
    start_time = time()
    main()
    print("--- %.2f seconds ---" % (time() - start_time))

