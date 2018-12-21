# Bulk download and delete from slack

This script finds attachments in your slack workspace, downloads attachments that were explicitly uploaded to slack to your local directory (i.e., not dropbox links auto downloaded by slack), and deletes the files from slack.
It will warn you before actually deleting files.

## Setup

Install

    pip install requests click

Follow the help instructions to get an API token:

    python deletefiles.py --help


	Usage: deletefiles.py [OPTIONS] TOKEN

	  Download and delete up to the 1000 largest slack files.  Only downloads files
	  explicitly uploaded to Slack. Does not download files downloaded from
	  e.g., dropbox links.

	  Go to this URL to get the API token:

		https://api.slack.com/custom-integrations/legacy-tokens

	Options:
	  -ndays INTEGER   Delete files up to n days old.
	  -minmb FLOAT     Delete files larger than this.
	  -filetypes TEXT  Comma delimited list of file extensions to delete e.g.,
					   pdf,docx
	  --help           Show this message and exit.


## Examples

Delete files up to a month old

    python deletefiles.py <token> -ndays=30

Delete files at least 10MB in size that are zip or pdf files

    python deletefiles.py <token> -minmb=10 -filetypes=zip,pdf




