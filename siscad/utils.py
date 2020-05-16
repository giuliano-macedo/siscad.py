def parse_table(elem):
    """
    Parses HTML and return a list of dicts with keys being the header entries
    """
    keys=[h.text.strip() for h in elem.find("thead").find_all("th") ]
    ans=[]
    for tr in elem.find("tbody").find_all("tr"):
        ans.append(dict(zip(
            keys,
            (elem for elem in tr.find_all("td"))
        )))
    return ans