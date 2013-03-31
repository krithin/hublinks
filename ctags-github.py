from flask import Flask, request, Response

app = Flask(__name__)

app.debug = True

import tempfile
import subprocess
import os
import os.path
import shutil
import urlparse
import json
from sys import stderr

import pyctags

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/tagify')
def tagify():
    repo = request.args.get('repo')
    filepath = request.args.get('file')
    callback = request.args.get('callback', False)

    resp = json.dumps(get_mapping(repo, filepath)) if repo and filepath else ''

    if callback:
        resp = callback + '(' + resp + ');'    
    if repo and filepath:
        return Response(resp, mimetype='application/json')
    return ' '.join(['Give me more arguments! I only got:', 
                     str(repo), ' and ', str(filepath)])

def build_tagset(repo, repodir):
    make_tags(repodir)
    ct = pyctags.ctags_file(str(os.path.join(repodir, 'tags')))
    
    # don't worry about duplicates for now
    tagsets[repo] = {tag.name: dict(destFile=tag.file, destLine=tag.line_number) for tag in ct.tags }

    # clean up
    shutil.rmtree(repodir)
    
def make_tags(d):
    CTAGS = ['ctags', '-R', '--fields=+n']
    subprocess.call(CTAGS, cwd=d)

# maps repository IDs (whatever they are) to mappings from symbols to 
# sets of (filename, line #) pairs
tagsets = dict()

def get_mapping(repo, filepath):
    build_repo(repo)
    return tagsets[repo]

# clone repo, build global tag data structure that maps tags to file/line
def build_repo(repo):
    if repo in tagsets:
        return
    cloneDir = get_repo_path(repo)

    if not os.path.exists(cloneDir):
        os.makedirs(cloneDir)
        subprocess.call(['git', 'clone', '--depth=1', repo, cloneDir])
    build_tagset(repo, cloneDir)

 	
def words(f):
    for lineno, line in enumerate(f, start=1):
	for word in line.strip().split():
            yield (lineno, word)

repositoryDir = tempfile.mkdtemp()
def get_repo_path(repo):
    p = urlparse.urlparse(repo).path
    return os.path.join(repositoryDir, p[1:])

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)

def theapp(arg1, arg2):
    app.run('0.0.0.0', port=80)
