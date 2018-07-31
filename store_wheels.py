import os
import requests
import urllib.request

repo = os.getenv('REPO')
date = os.getenv('DATE')

response = requests.get('https://api.github.com/repos/{}/wheels/releases'.format(repo))
for release in response.json():
    if not os.path.exists(os.getcwd()+'/'+release.get('name')):
        os.makedirs(release.get('name'))
    for asset in release.get('assets',[]):
        if date < release['created_at']:
            urllib.request.urlretrieve(asset.get('browser_download_url'),os.path.join(release['name'],asset['name']))
