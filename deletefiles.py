import click
import os
import requests
import time
import json




def list_files(token, ts_to):
  uri = 'https://slack.com/api/files.list'
  params = {
    'token': token
    ,'ts_to': ts_to
    ,'count': 1000
  }

  response = requests.get(uri, params=params)
  return json.loads(response.text)['files']

def download_all(token, files):
  os.system("mkdir -p ./downloads")
  print "Downloading files to ./downloads"
  urls = [f['url_private_download'] for f in files if 'url_private_download' in f]
  with file("urls", "w") as urlfile:
    urlfile.write("\n".join(urls))

  print "wrote %s urls" % len(urls)
  os.system("python download.py urls")
  raw_input('press "enter" when all files are downloaded')
  

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

  if not skipdl:
    download_all(token, files)

  if not skiprm:
    for f in files:
      print 'will rm:', f['size'], '\t', ('url_private_download' in f), '\t', f['name']
    raw_input('Press enter to delete.  Ctl-c to quit.')
    for i, f in enumerate(files):
      fid = f['id']
      status = delete_file(token, fid)
      print 'deleted', i, 'of', len(files), fid, status


if __name__ == "__main__":
  main()