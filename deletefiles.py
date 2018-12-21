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
  willdelete = []
  for i, f in enumerate(files):
    outname = "./downloads/" + f['name']
    if 'url_private_download' in f:
      data = requests.get(f['url_private_download']).content
      with file(outname, "wb") as out:
        out.write(data)
      print "", "download", f['name']
    else:
      print "", "    skip", f['name']

    willdelete.append(f)
  return willdelete
  

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
def main(token, ndays, minmb):
  """
  Download and delete up to 1000 largest slack files. 
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

  willdelete = download_all(token, files)
  for f in willdelete:
    print 'will rm:', f['size'], '\t', ('url_private_download' in f), '\t', f['name']
  raw_input('Press enter to delete.  Ctl-c to quit.')
  for i, f in enumerate(willdelete):
    fid = f['id']
    status = delete_file(token, fid)
    print 'deleted', i, 'of', len(willdelete), fid, status


if __name__ == "__main__":
  main()