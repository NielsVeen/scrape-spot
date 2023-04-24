import requests
from lxml import html

USERNAME = ''
PASSWORD = ''

def start_session():
    session_requests = requests.session()
    session_requests.headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    login_url = "https://www.spotontrack.com/login"
    result = session_requests.get(login_url)

    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='_token']/@value")))[0]

    # create payload to send with request
    form_data = {
        '_token':authenticity_token,
        'email': USERNAME,
        'password':PASSWORD,
    }

    # Perform site login 
    response = session_requests.post(login_url,data=form_data)

    return authenticity_token, session_requests

def search_track(spotify_url,session):
    url = f"https://www.spotontrack.com/api/search?type=tracks&keywords={spotify_url}"
    response = session.get(url)
    return response.json()[0]['link'],session

def get_page(pageurl,session):
    session.get(pageurl)
    return session

def get_file(track_link,session):
    url = f"{track_link}/export?platforms=spotify&type=current_playlists"
    session.headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,bg;q=0.6,de;q=0.5',
        'Connection':'Keep-Alive',
        'Content-Encoding':'gzip',
        'Cookie':f"XSRF-TOKEN={str(session.cookies['XSRF-TOKEN'])}; laravel_session={str(session.cookies['laravel_session'])}",
        'DNT':'1',
        'Host':'www.spotontrack.com',
        'Referer':f'{track_link}/playlists',
        'Upgrade-Insecure-Request':'1',
        'Sec-Fetch-Dest':'document',
        'Sec-Fetch-Mode':'navigate'

    }

    response = session.get(url)
    content = response.content.decode('UTF-8')
    return response

token,session = start_session()
url, session = search_track('https://open.spotify.com/track/2BxpTbiPVty66AwYhTrKbt?si=1b2d66ab58224db7',session)
session = get_page(url,session)
content = get_file(url,session)
print(content)