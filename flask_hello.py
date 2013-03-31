from flask import Flask, request, Response

app = Flask(__name__)

app.debug = True

import tempfile
import uuid
import subprocess
import os
import os.path
import shutil
import urlparse
import json
from sys import stderr

from collections import defaultdict

import pyctags

@app.route('/')
def hello_world():
    return 'Hello World!'

repositoryDir = tempfile.mkdtemp()

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

# going to need to canonicalize repository identification so the mappings
# work
def normalize_repo(repository):
    return repository

# clone repo, build global tag data structure that maps tags to
def build_repo(repo):
    if repo in repoToDirectory:
        return

    tmpdir = tempfile.mkdtemp()
    subprocess.call(['git', 'clone', '--depth=1', repo], cwd=tmpdir)

    cloneDir = os.path.join(tmpdir, os.path.join(tmpdir, os.listdir(tmpdir)[0]))
    repoToDirectory[repo] = cloneDir
    build_tagset(repo, cloneDir)

def build_tagset(repo, repodir):
    make_tags(repodir)
    ct = pyctags.ctags_file(os.path.join(repodir, 'tags')) # don't worry about duplicates for now
    tagsets[repo] = {tag.name: (tag.file, tag.line_number) for tag in ct.tags }
    
def make_tags(d):
    subprocess.call(CTAGS, cwd=d)

# maps repository IDs (whatever they are) to mappings from symbols to 
# sets of (filename, line #) pairs
tagsets = dict()

# maps repository IDs (whatever they are) to temporary directories
repoToDirectory = dict()

def getdir(repo):
    return repoToDirectory[repo]

def get_mapping(repo, filepath):
    repo = normalize_repo(repo)
    build_repo(repo)
    
    tagset = tagsets[repo]
    tagMapping = dict()
    with open(os.path.join(repoToDirectory[repo], filepath)) as f:
        for lineno, word in words(f):
            if word in tagset:
                destFile, destLine = tagset[word]
                tagMapping[word] = dict(destFile=destFile, destLine=destLine)
    
    return tagMapping
 	
CTAGS = ['ctags', '-R', '--fields=+n']
def words(f):
    for lineno, line in enumerate(f, start=1):
	for word in line.strip().split():
            yield (lineno, word)

def get_repo_path(repo):
    # strip off the ".git"
    p = urlparse.urlparse(repo).path[:-4]
    return os.path.join(repositoryDir, p)

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)

def theapp(arg1, arg2):
    app.run('0.0.0.0', port=80)
