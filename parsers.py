import re
from bs4 import BeautifulSoup


def parse_grad(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all("td", attrs={"name": "Button1"})
    data = list()
    for res in results:
        name = res.strong.a.font.string.rstrip()
        res = res.next_sibling.next_sibling
        n_washers = (res.strong.font.string.rstrip())
        res = res.next_sibling.next_sibling
        n_dryers = (res.strong.font.string.rstrip())
        res = res.next_sibling.next_sibling.next_sibling.next_sibling
        n_used_washers = (res.strong.font.string.rstrip())
        res = res.next_sibling.next_sibling.next_sibling.next_sibling
        n_used_dryers = (res.strong.font.string.rstrip())
        data.append([name, n_washers, n_dryers, n_used_washers, n_used_dryers])
    return data


def parse_hall(html):
    pat = re.compile('<font color="#000000"><strong><font size="2" face="Arial, Helvetica, sans\-serif">\s+(\d+)\s+<\/font><\/strong><\/font>\s+<\/div>\s+<\/td>\s+<td align="center" valign="middle" bgcolor="#\w{6}"\s+<div align="center">\s+<font color="#\w{6}"><font size="1" face="Arial, Helvetica, sans\-serif">\s+([\w\s\-\(\)]+)\s+<\/font><\/font>\s+<\/div>\s+<\/td>\s+<td align="center" valign="middle" bgcolor="#\w{6}"\s+<div align="center">\s+<font color="#\w{6}"><font size="2" face="Arial, Helvetica, sans-serif">\s([\w\s]+)(<br><font size="1">[\S\s]+<\/font>)?\s+<\/font><\/font>\s+<\/div>\s+<\/td>')
    results = pat.findall(html)
    data = list()
    for res in results:
        data.append([(res[0])]+[c.strip() for c in res[1:]])
    return data
