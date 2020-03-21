import os
from bs4 import BeautifulSoup
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

__all__ = [
    'auth_in_google_drive',
    'get_article_html',
]


def auth_in_google_drive(google_scopes, credentials_filepath):
    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_filepath, google_scopes
    )
    drive = GoogleDrive(gauth)
    return drive


def remove_spans(soup):
    for span in soup.findAll('span'):
        span.unwrap()


def remove_style(soup):
    for style in soup.findAll('style'):
        style.extract()


def remove_attrs(soup, attrs=["class", "id"]):
    for tag in soup():
        for attribute in attrs:
            del tag[attribute]


def get_article_html(gdrive_api, doc_id, ):
    article_doc = gdrive_api.CreateFile({'id': doc_id})
    article_doc.FetchMetadata(fetch_all=True)
    html = article_doc.GetContentString(mimetype='text/html')
    soup = BeautifulSoup(html, "html.parser")
    remove_attrs(soup)

    body_tag = soup.body
    article_tag = soup.new_tag("article")
    article_tag.contents = body_tag.contents

    return article_doc['title'], article_tag.prettify()


def main():
    google_scope = [
        # 'https://www.googleapis.com/auth/spreadsheets', # disabled
        'https://www.googleapis.com/auth/drive',
    ]
    doc_id = '1BgpkXOAgsnVgbAir8AK-KyEWHxM_mV51WgJSLOLASgo'

    gdrive_api = auth_in_google_drive(google_scope, os.getenv('GAPI_CREDENTIALS'))

    title, article_html = get_article_html(gdrive_api, doc_id)
    print(title)
    print(article_html)

def main_demo():
    google_scope = [
        # 'https://www.googleapis.com/auth/spreadsheets', # disabled
        'https://www.googleapis.com/auth/drive',
    ]
    doc_id = '1BgpkXOAgsnVgbAir8AK-KyEWHxM_mV51WgJSLOLASgo'

    gdrive_api = auth_in_google_drive(google_scope, os.getenv('GAPI_CREDENTIALS'))

    article_doc = gdrive_api.CreateFile({'id': doc_id})
    article_doc.FetchMetadata(fetch_all=True)
    html = article_doc.GetContentString(mimetype='text/html')
    soup = BeautifulSoup(html, "html.parser")
    pretty_html = soup.prettify()

    with open('test.html', 'w') as file:
        file.write(pretty_html)


if __name__ == '__main__':
    # main()
    main_demo()
