import re
import util
import bs4
import queue
import json
import sys
import csv


def crawler(filename, index_filename):
    starting_url = "https://www.teenlife.com/search/?q=None&l=None&c=Summer%20Program&p=1"
    limiting_domain = "teenlife.com"

    links_visited = []
    index_dictionary = {}
    pages_crawled = 0
    q = queue.Queue()
    q.put(starting_url)
    while q.empty() == False and pages_crawled < num_pages_to_crawl:
        link = q.get()
        mini_crawler(link, q, links_visited, limiting_domain, index_dictionary)
        # add function here to pull information from the websites 
        pages_crawled += 1

    with open(course_map_filename, 'r') as f:
        mapping = json.load(f)
    with open(index_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key,values in index_dictionary.items():
            for value in values:
                writer.writerow([str(mapping[key]) + '|' + value])


def mini_crawler(url, q, links_visited, limiting_domain, index_dictionary):
    '''
    Crawl the college catalog and adds to an index dictionary to map set of 
    words with associated course identifier.

    Inputs:
        url: starting url to begin crawling with
        q: queue of urls in line to be crawled
        links_visited: list of visited links
        limiting_domain: domain name
        index_dictionary: dictionary that maps words to course identifiers 
    '''    
    if url in links_visited:
        return
    request = util.get_request(url)
    if request is None: 
        return
    post_url = util.get_request_url(request)
    if post_url in links_visited:
        return
    html = util.read_request(request)
    soup = bs4.BeautifulSoup(html, features="html5lib")
    # make_index(soup, index_dictionary)
    find_links(soup, url, post_url, q, links_visited, limiting_domain)
    tag_list = soup.find_all("ul", attrs = {"class": "pagination"})
    parser = tag_list[0].findChild()
    next_page = parser.next_sibling.next_sibling.findChild().get('href')
    q.put(next_page)



def find_links(soup, url, post_url, q, links_visited, limiting_domain):
    '''
    Adds links to be visited to the queue 'q' and adds links visited to the list
    'links_visited.'

    Inputs:
        soup: soup object from the text of the HTML document
        url: starting url to begin crawling with
        post_url: this is the processed absolute url
        q: queue of urls that is being added to for each url crawled
        links_visited: list of visited links
        limiting_domain: domain name
    '''       
    tag_list = soup.find_all("div", attrs = {"class":"search-listing-content"})
    for tag in tag_list:
        href_tag = tag.findChild()
        possible_link = href_tag.get('href')
        actual_link = util.convert_if_relative_url(post_url, possible_link)
        if actual_link is not None and actual_link not in links_visited:
            if util.is_url_ok_to_follow(actual_link, limiting_domain):
                q.put(actual_link)
    links_visited.append(url)
    if post_url != url:
        links_visited.append(post_url) 


# def make_index(soup, index_dictionary):
#     '''
#     Adds words from course title and description to the index dictionary.
#     Uses the helper function pull_words to map the set of words to the 
#     associated course identifier.

#     Inputs:
#         soup: soup object from the text of the HTML document
#         index_dictionary: dictionary that maps words to course identifiers 
#     '''
#     main_words = set()
#     tags = soup.find_all("div", class_ = "courseblock main")
#     for tag in tags:
#         main_words, course_id = pull_words(tag)
#         subtags = util.find_sequence(tag)
#         if subtags:
#             for subtag in subtags:
#                 seq_words, seq_id = pull_words(subtag)
#                 index_dictionary[seq_id] = seq_words|main_words
#         else:
#             index_dictionary[course_id] = main_words


# def pull_words(tag):
#     '''
#     Creates a set of words and the associated course identifier.

#     Inputs:
#         tag: div tag object from the soup object  

#     Outputs:
#         (words, course_id): (set of words tied to the course identifier, 
#         course identifier) 
#     '''
#     title_tag = tag.find_all("p", class_="courseblocktitle")
#     desc_tag = tag.find_all("p", class_="courseblockdesc")
#     title_and_desc = title_tag[0].text + desc_tag[0].text
#     course_title = title_and_desc.replace(u"\xa0",u" ")
#     course_id = course_title[0:10]
#     course_title = course_title.lower()
#     title_words = re.findall('[a-z][a-z0-9]*', course_title)
#     words = set()
#     for title_word in title_words:
#         if title_word not in INDEX_IGNORE:
#             words.add(title_word)
#     return (words, course_id)
