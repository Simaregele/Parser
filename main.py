from bs4 import BeautifulSoup
import requests
import pandas as pd

# две df временная (она будет сохранять в себе по однйо карточке), которую добавляем к основной и основная
df = pd.DataFrame()
main_df = pd.DataFrame()

def create_url(page_number):
  # создает URL страницы
  return "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p={}&region=1&room1=1&room9=1&type=4".format(str(page_number))

def get_navigation_last_num_element(element_number, url):
  # возвращает последний элемент нав меню внизу страницы
  print(element_number)
  new_page = requests.get(url)
  soup = BeautifulSoup(new_page.text, 'html.parser')
  exit_val = soup.find_all(class_="_93444fe79c--list-itemLink--3o7_6")[element_number].get_text()
  return exit_val


def count_number_of_category_pages(url):
  # считает кол-во страниц в выбранной категории, запускается на странице
  while True:
    pages_menu_last__numeric_element = get_navigation_last_num_element(-1, url)
    print(pages_menu_last__numeric_element)
    if pages_menu_last__numeric_element.isdigit():
      # проверяет какой последний элемент, если тот цифра то значит это индекс
      # последней страницы
      print(pages_menu_last__numeric_element + " WOW")
      return pages_menu_last__numeric_element
    else:
      # в ином случае вытаскивает предпослежний элемент и использует в качестве
      # индекса для генерация новой страницы на которой проверяется последний
      # элемент может быть 1

      pages_menu_last__numeric_element = get_navigation_last_num_element(-2, url)
      url = create_url(pages_menu_last__numeric_element)


pages_count = count_number_of_category_pages(create_url(1))
for i in pages_count:
  print(i)