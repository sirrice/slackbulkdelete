#!/usr/bin/env python2.7

from os import system, getcwd
from os.path import join
from re import compile
from selenium import webdriver
import click

@click.command()
@click.argument("urlfname")
def main(urlfname):
  """
  To run, you need:

   1. The Google Chrome browser.

   2. You need Selenium.

       pip install selenium

   3. You need to put the ChromeDriver binary in your PATH.

       https://sites.google.com/a/chromium.org/chromedriver/downloads 

  """
  urls = [] 
  with file(urlfname) as f:
    for url in f:
      urls.append(url.strip())


  system("mkdir -p downloads")
  co = webdriver.ChromeOptions()
  co.add_experimental_option('prefs',
    {
        'download.default_directory': join(getcwd(), "downloads"),
        'download.prompt_for_download': False,
        'plugins.always_open_pdf_externally': True
    })
  browser = webdriver.Chrome(chrome_options=co)
  browser.get("https://pfunk.slack.com/")
  raw_input("Press 'return' when you have signed in to start download.")

  for i, url in enumerate(urls):
    browser.get(url)
    print i, "of", len(urls)
  browser.quit()

if __name__ == "__main__":
  main()

