import datetime
import click
import os
import requests
import time
import json

from os import system, getcwd
from os.path import join
from selenium import webdriver




def list_files(token, ts_to):
  uri = 'https://slack.com/api/files.list'
  params = {
    'token': token
    ,'ts_to': ts_to
    ,'count': 5000
  }

  response = requests.get(uri, params=params)
  return json.loads(response.text)['files']

def download_all(token, files):
  """
  To run, you need:

   1. The Google Chrome browser.

   2. You need Selenium.

       pip install selenium

   3. You need to put the ChromeDriver binary in your PATH.

       https://sites.google.com/a/chromium.org/chromedriver/downloads 

  """

  os.system("mkdir -p ./downloads")
  print "Downloading files to ./downloads"
  urls = [f['url_private_download'] for f in files if 'url_private_download' in f]
  if not urls:
    return

  co = webdriver.ChromeOptions()
  co.add_experimental_option('prefs',
    {
        'download.default_directory': join(getcwd(), "downloads"),
        'download.prompt_for_download': False,
        'plugins.always_open_pdf_externally': True
    })
  browser = webdriver.Chrome(chrome_options=co)
  browser.get(urls[0])
  raw_input("Press 'return' when you have signed in to start download.")

  for i, url in enumerate(urls[1:]):
    browser.get(url)
    print (i+2), "of", len(urls)
  browser.quit()


def delete_file(token, file_id):
  params = {
    'token': token
    ,'file': file_id
    }
  uri = 'https://slack.com/api/files.delete'
  response = requests.get(uri, params=params)
  return json.loads(response.text)['ok']


@click.command()
@click.argument("token")
@click.option("-ndays", type=int, default=30, help="Delete files up to n days old.")
@click.option("-minmb", type=float, default=0.5, help="Delete files larger than this.")
@click.option("-filetypes", type=str, default="", help="Comma delimited list of file extensions to delete e.g., pdf,docx")
@click.option("-skipdl", is_flag=True, help="Skip downloading files.")
@click.option("-skiprm", is_flag=True, help="Skip deleting files.")
def main(token, ndays, minmb, filetypes, skipdl, skiprm):
  """
  Download and delete up to the 1000 largest slack files. 
  Only downloads files explicitly uploaded to Slack.
  Does not download files downloaded from e.g., dropbox links.

  Go to this URL to get the API token:

    https://api.slack.com/custom-integrations/legacy-tokens
  """
  ts_to = int(time.time()) - ndays * 24 * 60 * 60
  nbytes = int(1000000 * minmb)
  files = list_files(token, ts_to)
  files = filter(lambda f: f['size'] >= nbytes, files)
  files.sort(key=lambda f: f['size'], reverse=True)

  filetypes = filetypes.split(",")
  if filetypes:
    func = lambda f: any(f['name'].endswith(ftype) for ftype in filetypes)
    files = filter(func, files)

  # edit the code here if you want to filter files based on file type or file name
  # files = filter(lambda f: f['name'], files)
  # files = filter(lambda f: f['filetype'], files)

  if not files:
    print "No files to delete.  Done"
    return

  total_size = int(sum(f['size'] for f in files) / 100000) / 10.

  print "I found %s MB from %d files (MBs, tstamp, will download, name):" % (total_size, len(files))
  for f in files:
    dt = datetime.datetime.utcfromtimestamp(f['timestamp']).strftime('%Y-%m-%d')
    print '\t', (f['size'] / 100000) / 10., '\t', dt, '\t', ('url_private_download' in f), '\t', f['name']

  if not skipdl:
    download_all(token, files)

  if not skiprm:
    raw_input('Press enter to delete.  Ctl-c to quit.')
    for i, f in enumerate(files):
      fid = f['id']
      status = delete_file(token, fid)
      print 'deleted', i, 'of', len(files), fid, status


if __name__ == "__main__":
  main()