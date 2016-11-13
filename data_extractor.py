# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 19:57:14 2016

@author: Julia
"""

import urllib2
import os
import shutil
import re
import unicodedata

opener = urllib2.build_opener()

# WORKING DIRECTORY
data_dir = 'C:/Users/Julia/Documents/wiki/'
os.chdir(data_dir)

#Make the directory to store the HTML pages. (this might not be necessary!)
if not os.path.isdir('wikipages'):
    os.mkdir('wikipages')
    print "Created new directory for storing the pages"


# FUNCTIONS:
def find_info(target,article):
    # This function finds and splits the lines that contain Infobox target info.
    # Check the data exists:
    if not re.search(target,article):
        target_info = False 
    else:
    # If it exists, save it in target_info:
        target_regexp = '\|.*' + target + '.*\n' #This will retrieve the whole line
        target_search = re.search(target_regexp,article)
        if not target_search:
            target_info = False
        else:
            target_info = target_search.group()
    return target_info

def continue_search(list_page):
    if re.search('cmcontinue', list_page):
        cmcontinue = True
    else:
        cmcontinue = False
    return cmcontinue

def continue_where(list_page):
    continue_search = re.search('cmcontinue=\"page\|([a-zA-Z0-9\|]+)\"',list_page)
    continue_id = re.search('page\|([a-zA-Z0-9\|]+)',continue_search.group()).group()
    return continue_id

def get_age(birth,death):
    age = death[0]-birth[0]
    if death[1]-birth[1] < 0:
        age = age -1
    elif death[1]-birth[1] == 0:
        if death[2]-birth[2] < 0:
            age = age -1
    return age
        

# DEFINE CATEGORY TO SEARCH

wiki_category = 'German film actresses'
wiki_cat_sub = re.sub(' ','%20', wiki_category) # I replace spaces with %20

# OPEN FILE TO DROP DATA
f = open('data_' + re.sub(' ','_',wiki_category) + '.txt', 'w')
print >> f, 'pageid,title,birth_y,birth_m,birth_d,death_y,death_m,death_d,death_age'

# STEP 1: GET LIST OF ARTICLES TO SEARCH IN A GIVEN CATEGORY


# Begin search on first page.
infile = opener.open('https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:'+wiki_cat_sub+'&cmlimit=500&format=xml')
page = infile.read()

# Retrieve page ids for all pages in the list.
search_ids = re.findall('pageid=\"(.*?)\"',page)

# If list is not complete, continue with the following 500 until no more left
# (the api only allows to get 500 pages in each query, so if there are
# pages left, it returns a "continue" code).

cmcontinue = continue_search(page)
if cmcontinue:
    continue_id = continue_where(page)
i=0
while cmcontinue:
    i = i+1
    print i
    infile_cont = opener.open('https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:'+wiki_cat_sub+'&cmcontinue='+continue_id+'&cmlimit=500&format=xml')
    page_cont = infile_cont.read()
    page_ids = re.findall('pageid=\"(.*?)\"',page_cont)
    search_ids = search_ids + page_ids
    cmcontinue = continue_search(page_cont)
    if cmcontinue:
        continue_id = continue_where(page_cont)
    

# STEP 2: RETRIEVE INFO FROM EACH ARTICLE

#Read article
p=0
for pageid in search_ids:
    print p
    inarticle = opener.open('https://en.wikipedia.org/w/api.php?action=query&pageids='+pageid+'&prop=revisions&rvprop=content&rvsection=0&format=xml')
    article = inarticle.read()
    
    page_title = re.findall('title=\"(.*?)\"',article)[0].decode('utf-8')
    page_title_ascii = unicodedata.normalize('NFKD',page_title).encode('ascii','ignore')
    page_title_ascii = re.sub('&#039;','\'',page_title_ascii) #correct apostrophes (not recognised)
    page_title_ascii = re.sub(',','',page_title_ascii) #get rid of commas in title
    
    death_info = find_info('death_date', article)
    birth_info = find_info('birth_date', article)
    
    if not ((not death_info) or (not birth_info)) :
        d_dates = re.findall('[0-9]{4}\|[0-9]{1,2}\|[0-9]{1,2}',death_info)
        b_date = re.findall('[0-9]{4}\|[0-9]{1,2}\|[0-9]{1,2}',birth_info)
        if len(d_dates) == 1 & len(b_date) == 1:
            death_date = map(int,re.split('\|',d_dates[0]))
            birth_date = map(int,re.split('\|',b_date[0]))
            include = True
        elif len(d_dates) == 2:
            death_date = map(int,re.split('\|',d_dates[0]))
            birth_date = map(int,re.split('\|',d_dates[1]))
            include = True
        else:
            include = False
    else:
         include = False
    p=p+1
    if include:
        death_age = get_age(birth_date,death_date)
        print >> f, '{0},{1},{2},{3},{4},{5},{6},{7},{8}'.format(int(pageid), page_title_ascii, birth_date[0], birth_date[1],birth_date[2],death_date[0],death_date[1],death_date[2],death_age)
        print 'Included'
f.close()
    
