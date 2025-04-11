import requests 
import csv
from bs4 import BeautifulSoup

def get_info():
    date = input("Enter the date in MM/DD/YYYY format: ")
    return date
def get_page(date):
    page=requests.get(f"https://www.yallakora.com/match-center/مركز-المباريات?{date}")
    return page
def get_soup(page):
    soup = BeautifulSoup(page.content, 'lxml')
    return soup
def get_shampionships(soup):
    shampionships= soup.find_all('div', class_='matchCard')
    return shampionships
def get_matches_details(shampionships):
    result=[]
    for i in shampionships :
        title_class= i.find('div',class_='title')
        if title_class :
            parent_of_title=title_class.find('a',class_='tourTitle')
            if parent_of_title :
                title=parent_of_title.find('h2').text.strip()
        tag_out=i.find('div',class_='ul')
        matches=tag_out.find_all('div',class_='teamsData')
        for j in matches :
            teamA=j.find('div',class_='teamA').text.strip()
            teamB=j.find('div',class_='teamB').text.strip()
        result.append({"title":title,"first_team":teamA,"second_team":teamB})
    return result
def save_to_csv(data):
    with open("./result.csv",'w',newline='',encoding='utf-8') as output_file:
        keys=data[0].keys()
        dict_obj=csv.DictWriter(output_file,fieldnames=keys)
        dict_obj.writeheader()
        dict_obj.writerows(data)
def main():
    date=get_info()
    page=get_page(date)
    soup=get_soup(page)
    shampionships=get_shampionships(soup)
    result=get_matches_details(shampionships)
    save_to_csv(result)
if __name__ == "__main__":
    main()