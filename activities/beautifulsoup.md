## Parsing HTML

Regular expresssions are not ideal HTML parsers

In order to parse HTML, you need an HTML parser, like those included in
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start).
To install BeautifulSoup, run `python3 -m pip install --user bs4`.


```python
from bs4 import BeautifulSoup
import re

# open a previously saved HTML file and soupify it
# BeautifulSoup can take a str or a file object as its first argument
with open('Healthcare_in_Canada-wikipedia.html') as healthy_file:
    soup = BeautifulSoup(healthy_file, 'html.parser')
```

Let's find all the headers with \<h2\> tags in this article.

```python
print(soup.find_all('h2'))
```

Let's extract all of the links on this page.

```python
for a in soup.find_all('a'):
    print(a.get('href'))
```

Let's find all the \<span\> tags in this article with `id=Public_opinion`.

```python
print(soup.find_all('span', id='Public_opinion'))
```

Now find elements with 'poll' in the text.

```python
print(soup.find_all(string='poll'))
# or even better...
# print(soup.find_all(string=re.compile(r'\bpoll\b', re.I)))
```
