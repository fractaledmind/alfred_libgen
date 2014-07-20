def search_libgen():
    return search_libgen(query)

def search(wf, query):
    """Search LibGen for `query`.
    """

    

    #Get previous results or do new search
    html = wf.cached_data(query, wrapper, max_age=604800)
    
    # Soupify the HTML results
    res_table = SoupStrainer('table', {"class" : "c"})
    soup = BeautifulSoup(html, parse_only=res_table)
    ind_results = soup.find_all('tr', {"valign" : "top"})

    # Extract the relevant result column names
    keys = [s.text.strip().lower()
            for item in ind_results[0:1]
            for s in item.find_all('td')]
    keys = keys[:10]

    # Generate array of dicts for the results
    items = []
    for item in ind_results[1:]: # for each row
        dct = OrderedDict()
        for idx, element in enumerate(item.find_all('td')): # for each column
            if idx < 9: # if relevant column
                key = keys[idx]
                value = element.text
                if idx == 2: # if `Title` column
                    # Get unique hash for each item
                    link = element.a['href']
                    hash_link = link.replace('book/index.php?', '')
                    dct.update({'hash': hash_link})

                    # remove possible ISBNs
                    extras = [s.text for s in element.find_all('font')
                                if '[' not in s.text] # ISBNs
                    if extras != []:
                        for non in extras:
                            value = element.text.replace(non, '')
                if value == '':
                    value = None
                dct.update({key: value})
        items.append(dct)

    wf.cache_data('results', items)

    for item in items:
        arg = item['hash'] or ""
        title = item['title'] or ""
        creators = item['author(s)'] or ""
        year = item['year'] or ""
        pages = ""
        if item['pages']:
            pages = item['pages'] + ' pages'
        size = item['size'] or ""
        sub = ' '.join([creators, year]) + ' (' + '; '.join([pages, size]) + ')'
        
        wf.add_item(title,
                    sub,
                    valid=True,
                    arg=arg)

    wf.send_feedback()
