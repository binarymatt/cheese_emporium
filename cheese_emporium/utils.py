from path import path
from werkzeug.contrib.cache import SimpleCache
from flask import render_template
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import xmlrpclib
import zipfile


class TarArchive:
    def __init__(self, filename):
        self.filename = filename
	mode = "r"
	if filename.endswith('.bz2'):
	    mode = "r:bz2"
	elif filename.endswith('.gz') or filename.endswith('.tgz'):
	    mode = "r:gz"
        self.tgz = tarfile.TarFile.open(filename, mode)

    def names(self):
        return self.tgz.getnames()

    def lines(self, name):
        return self.tgz.extractfile(name).readlines()

    def extract(self, name, tempdir):
        return self.tgz.extract(name, tempdir)

    def extractall(self, tempdir):
        os.system('cd %s && tar xzf %s' % (tempdir, 
                                           os.path.abspath(self.filename)))

    def close(self):
        return self.tgz.close()
 
class ZipArchive:
    def __init__(self, filename):
        self.filename = filename
        self.zipf = zipfile.ZipFile(filename, 'r')

    def names(self):
        return self.zipf.namelist()

    def lines(self, name):
        return self.zipf.read(name).split('\n')

    def extract(self, name, tempdir):
        data = self.zipf.read(name)
        fn = name.split(os.sep)[-1]
        fn = os.path.join(tempdir, fn)
        f = open(fn, 'wb')
        f.write(data)

    def extractall(self, tempdir):
        os.system('cd %s && unzip %s' % (tempdir, 
                                         os.path.abspath(self.filename)))

    def close(self):
        return self.zipf.close()

def _extract_name_version(filename, tempdir):
    archive = None
    if filename.endswith('.gz') or filename.endswith('.tgz') or filename.endswith('.bz2'):
        archive = TarArchive(filename)

    elif filename.endswith('.egg') or filename.endswith('.zip'):
        archive = ZipArchive(filename)
    
    if archive is None:
        return
    try:
        for name in archive.names():
            if len(name.split('/'))==2  and name.endswith('PKG-INFO'):
                project, version = None, None
                lines = archive.lines(name)
                for line in lines:
                    key, value = line.split(':', 1)
                    if key == 'Name':
                        print filename, value
                        project = value.strip()
                        
                    elif key == 'Version':
                        version = value.strip()
                    
                    if project is not None and version is not None:
                        return project, version
                    continue
        archive.extractall(tempdir)
        dirs = os.listdir(tempdir)
        dir = os.path.join(tempdir, dirs[0])
        if not os.path.isdir(dir):
            dir = tempdir
        command = ('cd %s && %s setup.py --name --version'
                       % (dir, sys.executable))
        popen = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                shell=True,
                                )
        output = popen.communicate()[0]
        archive.close()
        return output.splitlines()[:2]
    except:
        archive.close()
        import traceback
        print traceback.format_exc()
    return

def regenerate_package(indexpath, package_filename):
    #get project name
    tempdir = tempfile.mkdtemp()
    indexpath = path(indexpath)
    project, revision = _extract_name_version(package_filename, tempdir)
    dirname = indexpath / project
    if not dirname.exists():
        regenerate_index(indexpath)
        return
    shutil.rmtree(tempdir)
    indexpath = path(indexpath)
    files = indexpath.files(project+'*')
    items = parse_files(files)
    for key, value in items:
        sub = indexpath / key / 'index.html' 
        package_html = render_template('package_template.html', value=value, key=key)
        sub.write_text(package_html)

def parse_files(file_list):
    projects = {}
    for item in file_list:
        print item
        try:
            tempdir = tempfile.mkdtemp()
            project, revision = _extract_name_version(os.path.join(path,item), tempdir)
            projects.setdefault(project, []).append((revision, item))
            shutil.rmtree(tempdir)
        except:
            import traceback
            print traceback.format_exc()

    items = projects.items()
    items.sort()
    return items

def regenerate_index(indexpath, filename='index.html'):
    print "Regenerate index"
    indexpath = path(indexpath)
    if not indexpath.exists():
        indexpath.makedirs()
    files = indexpath.files()
    items = parse_files(files)
    
    f = indexpath / filename
    for key, value in items:
        dirname = indexpath / key
        if not dirname.exists():
            dirname.makedirs()
        sub = indexpath / key / 'index.html' 
        package_html = render_template('package_template.html', value=value, key=key)
        sub.write_text(package_html)

    index_html = render_template('index_template.html',items=items)
    f.write_text(index_html)

cache = SimpleCache()

def list_pypi():
    rs = cache.get('package-list')
    if rs:
        print 'found cached list'
        return rs
    else:
        print 'getting list from pypi'
        client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
        rs = client.list_packages()
        cache.set('package-list',rs,timeout=5 * 60)
        return rs


def search_pypi(package_name):
    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    return client.package_releases(package_name)


def package_details(package_name, version_number):
    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    return client.release_urls(package_name,version_number)
