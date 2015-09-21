from selenium import webdriver
import bs4
import re
import random
import nltk
nltk.download('punkt')

FANCY_CITIES = [
  'New+York%2C+NY',
  'San+Francisco%2C+CA',
  'Los+Angeles%2C+CA',
  'Honolulu%2C+HI',
  'Chicago%2C+IL',
  'Boston%2C+MA',
  'Portland%2C+OR',
  'Seattle%2C+WA',
  'Washington%2C+DC',
  'Houston%2C+TX',
  'Philadelphia%2C+PA',
  'Phoenix%2C+AZ',
  'San+Antonio%2C+TX',
  'San+Diego%2C+CA',
  'San+Jose%2C+CA',
  'Dallas%2C+TX',
  'Austin%2C+TX',
  'Atlanta%2C+GA',
  'Saint+Louis%2C+MO',
  'Minneapolis%2C+MN',
  'Las+Vegas%2C+NV',
  'London',
  'Denver%2C+CO'
]
BASE_URL = 'http://www.yelp.com'

def parsed_response(url):
  print('getting url {0}'.format(url))
  driver = webdriver.PhantomJS()
  driver.get(url)
  content = driver.page_source
  print('got content')
  driver.quit()

  return bs4.BeautifulSoup(content, "html.parser")

def random_page_num(fancy_city):
  all_businesses_url = '{0}/search?find_desc=&find_loc={1}&ns=1#start=0&attrs=RestaurantsPriceRange2.4'.format(BASE_URL, fancy_city)
  businesses_list = parsed_response(all_businesses_url)
  num_pages_text = businesses_list.select('.page-of-pages')[0].text
  num_pages = int(re.search('of (\d+)', num_pages_text).groups()[0])
  return random.randint(1, num_pages)

def random_fancy_business(fancy_city):
  starting_point = random_page_num(fancy_city) * 10 # pages are 10 businesses apart
  random_page_url = '{0}/search?find_desc=&find_loc={1}&ns=1#start={2}&attrs=RestaurantsPriceRange2.4'.format(
    BASE_URL, fancy_city, starting_point
  )
  random_page = parsed_response(random_page_url)
  random_business = random.choice(random_page.select('a.biz-name'))
  random_business_url = '{0}{1}?sort_by=rating_asc'.format(BASE_URL, random_business.attrs['href'])
  return parsed_response(random_business_url)

def random_review(business_page, num_stars):
  reviews = business_page.select('.stars_{0}'.format(num_stars))
  if reviews:
    random_review = random.choice(reviews)
    review_text = random_review.parent.parent.parent.parent.select('[itemprop=description]')[0].text
    if (len(review_text) > 140):
      tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
      sentences = tokenizer.tokenize(review_text)
      total_text = ''
      random_starting_point = random.randint(0, len(sentences) - 1)
      for sentence in sentences[random_starting_point:(len(sentences) - 1)]:
        total_text += sentence
        if len(total_text) >= 140:
          return total_text[0:139]
    else:
      return review_text

def find_angry_review():
  fancy_city = random.choice(FANCY_CITIES)
  random_business = random_fancy_business(fancy_city)
  one_star_review = random_review(random_business, 1)
  if one_star_review:
    return one_star_review
  else:
    two_star_review = random_review(random_business, 2)
    if two_star_review:
      return two_star_review
    else:
      return find_angry_review()

print(find_angry_review())