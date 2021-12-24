# removes all links that dont start with http
def remove_invalid_links(links):
    valid = {}
    for link in links:
        if link[0:8] == 'https://':
            valid.add(link)
    return link

