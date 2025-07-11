from fastapi import FastAPI, Request
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

class HTMLPayload(BaseModel):
    html: str

@app.post("/parse")
async def parse_html(payload: HTMLPayload):
    html_content = payload.html
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []

    for post in soup.find_all('tr', class_='athing submission'):
        pid = post.get('id')
        tl = post.find('span', class_='titleline')
        if not tl: continue
        a = tl.find('a')
        if not a or 'github.com' not in a.get('href', '').lower():
            continue

        url = a['href']
        title = a.get_text(strip=True)

        sb = tl.find('span', class_='sitebit comhead')
        site = sb.find('span', class_='sitestr').get_text(strip=True) if sb and sb.find('span') else ''

        subtext = post.find_next_sibling('tr')
        if not subtext: continue
        sub_td = subtext.find('td', class_='subtext')
        if not sub_td: continue

        score = sub_td.find('span', class_='score')
        score = score.get_text(strip=True) if score else '0 points'
        author = sub_td.find('a', class_='hnuser')
        author = author.get_text(strip=True) if author else 'unknown'
        age = sub_td.find('span', class_='age')
        age = age.get_text(strip=True) if age else 'unknown'
        comments = sub_td.find_all('a')[-1].get_text(strip=True) if sub_td.find_all('a') else '0 comments'

        posts.append({
            'id': pid,
            'title': title,
            'url': url,
            'site': site,
            'score': score,
            'author': author,
            'age': age,
            'comments': comments,
            'hn_url': f'https://news.ycombinator.com/item?id={pid}'
        })

    return posts

# Optional for manual run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
