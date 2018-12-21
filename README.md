# Bulk download and delete from slack

This script finds attachments in your slack workspace, downloads attachments that were explicitly uploaded to slack to your local directory (i.e., not dropbox links auto downloaded by slack), and deletes the files from slack.
It will warn you before actually deleting files.

The script uses the Chrome browser to actually download the files into `./downloads/`.  It then uses the Slack web api to delete those files.

## Setup

Install

    pip install requests click
    pip install selenium

You need to put the ChromeDriver binary in your PATH.  Go here and download it:

    https://sites.google.com/a/chromium.org/chromedriver/downloads 

## Help

Follow the help instructions.  Get [an API token first](https://api.slack.com/custom-integrations/legacy-tokens)

    python deletefiles.py --help

	Usage: deletefiles.py [OPTIONS] TOKEN

	  Download and delete up to the 1000 largest slack files.  Only downloads
	  files explicitly uploaded to Slack. Does not download files downloaded
	  from e.g., dropbox links.

	  Go to this URL to get the API token:

		https://api.slack.com/custom-integrations/legacy-tokens

	Options:
	  -ndays INTEGER   Delete files up to n days old.
	  -minmb FLOAT     Delete files larger than this.
	  -filetypes TEXT  Comma delimited list of file extensions to delete e.g.,
					   pdf,docx
	  -skipdl          Skip downloading files.
	  -skiprm          Skip deleting files.
	  --help           Show this message and exit.

## Examples

Delete files up to a month old

    python deletefiles.py <token> -ndays=30

Delete files at least 10MB in size that are zip or pdf files

    python deletefiles.py <token> -minmb=10 -filetypes=zip,pdf

Just list files but don't download and don't delete

    python deletefiles.py <token> -minmb=10 -filetypes=zip,pdf -skipdl -skiprm

