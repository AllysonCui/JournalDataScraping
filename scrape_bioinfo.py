import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tqdm
import os

def get_article_links(page, url = 'https://bmcbioinformatics.biomedcentral.com/articles?tab=keyword&searchType=journalSearch&sort=PubDate&volume=24&page='):
    url = url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ol_listing = soup.find('ol', class_='c-listing')

    articles = []

    a_tags = ol_listing.find_all('a', href=True)
    for a in a_tags:
        href = a['href']
        if 'pdf' not in href and href not in articles and '10.1186' in href:
            articles.append(href)
    return articles

def combine_article_links():
    all_articles = []
    for page in tqdm.tqdm(np.arange(1, 11)):
        articles = get_article_links(page)
        for article in articles:
            all_articles.append(article)
    return all_articles


# Only keep the main github page instead of sub-sections (the link should be somewhat the shortest compared to other similar links)
def filter_exclusive(strings):
    # Create a set to hold unique strings
    unique_strings = set(strings)

    # Iterate over the strings to find which strings to remove
    to_remove = set()
    for s in unique_strings:
        # Check if this string should be removed based on being a superstring of any other
        for other in unique_strings:
            if s != other and other in s:
                to_remove.add(s)
                break

    # Return the result as a list after removing non-exclusive superstrings
    return list(unique_strings - to_remove)


def retrieve_info(all_articles):
    doi_links = []
    titles = []
    pubDates = []
    git_links = []

    for i in tqdm.tqdm(np.arange(len(all_articles))):
        article = all_articles[i]
        response = requests.get(
            "https://bmcbioinformatics.biomedcentral.com" + article)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find DOI link
        doi_abbr = soup.find('abbr', title="Digital Object Identifier")
        parent = doi_abbr.find_parent()
        doi_span = parent.find('span',
                               class_='c-bibliographic-information__value')
        doi_links.append(doi_span.text.strip())

        # Find title
        title_tag = soup.find('h1')
        titles.append(title_tag.text.strip())

        # Find publication date
        article_header = soup.find('div', class_='c-article-header')
        identifiers = article_header.find('ul', class_='c-article-identifiers',
                                          attrs={
                                              'data-test': 'article-identifier'})
        time_tag = identifiers.find('time')
        pubDates.append(time_tag['datetime'])

        # Find GitHub link(s)
        links = []
        article_content = soup.find('article', {'lang': 'en'})
        a_tags = article_content.find_all('a', href=True)
        for a in a_tags:
            href = a['href']

            # Clean the link
            if href.endswith('.git'):
                href = href[:-4]
            count = 0
            for i, char in enumerate(href):
                if char == '/':
                    count += 1
                if count == 5:
                    href = href[:i]
                    break

            if href not in links and 'https://github' in href:
                links.append(href)
        if len(links) > 1:
            git_links.append(filter_exclusive(links))
        else:
            git_links.append(links)

    df = pd.DataFrame({
        'doi': doi_links,
        'title': titles,
        'pubDate': pubDates,
        'githubLink': git_links
    })
    print(df.info())
    return df

if __name__ == "__main__":
    article_info = retrieve_info(combine_article_links())
    article_info.to_csv(os.path.join("data", "scientific_data_articles.csv"))
