# (c) 2012-2016 Continuum Analytics, Inc. / http://continuum.io
# All Rights Reserved
#
# conda is distributed under the terms of the BSD 3-clause license.
# Consult LICENSE.txt or http://opensource.org/licenses/BSD-3-Clause.
'''
We use the following conventions in this module:

    dist:        canonical package name, e.g. 'numpy-1.6.2-py26_0'

    ROOT_PREFIX: the prefix to the root environment, e.g. /opt/anaconda

    PKGS_DIR:    the "package cache directory", e.g. '/opt/anaconda/pkgs'
                 this is always equal to ROOT_PREFIX/pkgs

    prefix:      the prefix of a particular environment, which may also
                 be the root environment

Also, this module is directly invoked by the (self extracting) tarball
installer to create the initial environment, therefore it needs to be
standalone, i.e. not import any other parts of `conda` (only depend on
the standard library).
'''
import os
import re
import sys
import json
import shutil
import stat
from os.path import abspath, dirname, exists, isdir, isfile, islink, join
from optparse import OptionParser


on_win = bool(sys.platform == 'win32')
try:
    FORCE = bool(int(os.getenv('FORCE', 0)))
except ValueError:
    FORCE = False

LINK_HARD = 1
LINK_SOFT = 2  # never used during the install process
LINK_COPY = 3
link_name_map = {
    LINK_HARD: 'hard-link',
    LINK_SOFT: 'soft-link',
    LINK_COPY: 'copy',
}

# these may be changed in main()
ROOT_PREFIX = sys.prefix
PKGS_DIR = join(ROOT_PREFIX, 'pkgs')
SKIP_SCRIPTS = False
IDISTS = {
  "cffi-1.9.1-py36_0": {
    "md5": "bb3e425ee5b39e201bf373ceb7ecca6e", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/cffi-1.9.1-py36_0.tar.bz2"
  }, 
  "conda-4.3.11-py36_0": {
    "md5": "13807b7108548c38f9ba85f5cdc0ca30", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/conda-4.3.11-py36_0.tar.bz2"
  }, 
  "conda-env-2.6.0-0": {
    "md5": "4bcba5618e1c70cbfb5107c3e61f2488", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/conda-env-2.6.0-0.tar.bz2"
  }, 
  "cryptography-1.7.1-py36_0": {
    "md5": "ed785381e520814b3d7abaeee88a9eb1", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/cryptography-1.7.1-py36_0.tar.bz2"
  }, 
  "idna-2.2-py36_0": {
    "md5": "40fdcb50dd238b79231cc5af4b9e7508", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/idna-2.2-py36_0.tar.bz2"
  }, 
  "openssl-1.0.2k-0": {
    "md5": "228cdb42dc2a4b7053e6bf0f1afa1c75", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/openssl-1.0.2k-0.tar.bz2"
  }, 
  "pip-9.0.1-py36_1": {
    "md5": "fc57004131181a6cc00cd57eae5f910e", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/pip-9.0.1-py36_1.tar.bz2"
  }, 
  "pyasn1-0.1.9-py36_0": {
    "md5": "9dca3d42cc9eec50eed86d3e4aa79fa3", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/pyasn1-0.1.9-py36_0.tar.bz2"
  }, 
  "pycosat-0.6.1-py36_1": {
    "md5": "95f56c0ec3c75cf54a77ac127e796b18", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/pycosat-0.6.1-py36_1.tar.bz2"
  }, 
  "pycparser-2.17-py36_0": {
    "md5": "611ceb73cab44c6f9bed234bc243ec30", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/pycparser-2.17-py36_0.tar.bz2"
  }, 
  "pyopenssl-16.2.0-py36_0": {
    "md5": "fd123b463a893715308d585359c2035a", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/pyopenssl-16.2.0-py36_0.tar.bz2"
  }, 
  "python-3.6.0-0": {
    "md5": "db74ffd5188a55be53902cfffbce666a", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/python-3.6.0-0.tar.bz2"
  }, 
  "readline-6.2-2": {
    "md5": "0801e644bd0c1cd7f0923b56c52eb7f7", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/readline-6.2-2.tar.bz2"
  }, 
  "requests-2.12.4-py36_0": {
    "md5": "3e70cadfc03d33453b31484b6b79c9f9", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/requests-2.12.4-py36_0.tar.bz2"
  }, 
  "ruamel_yaml-0.11.14-py36_1": {
    "md5": "1ff3815ce6ca1fe88923c3341f892343", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/ruamel_yaml-0.11.14-py36_1.tar.bz2"
  }, 
  "setuptools-27.2.0-py36_0": {
    "md5": "33a5ca1ffb4a6ea4a4457f7e649bf37f", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/setuptools-27.2.0-py36_0.tar.bz2"
  }, 
  "six-1.10.0-py36_0": {
    "md5": "be4b72c0d36adcd7dc2d79edeec639d2", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/six-1.10.0-py36_0.tar.bz2"
  }, 
  "sqlite-3.13.0-0": {
    "md5": "dacf9558b650e37c4ec9003fe7f6b405", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/sqlite-3.13.0-0.tar.bz2"
  }, 
  "tk-8.5.18-0": {
    "md5": "6de7b2d4c4c9cc0f60150da541c0d843", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/tk-8.5.18-0.tar.bz2"
  }, 
  "wheel-0.29.0-py36_0": {
    "md5": "c7e1bd872a1cd5f651addec7f17c711b", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/wheel-0.29.0-py36_0.tar.bz2"
  }, 
  "xz-5.2.2-1": {
    "md5": "c8d5d3f406b5309e575c6848091f2fd2", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/xz-5.2.2-1.tar.bz2"
  }, 
  "yaml-0.1.6-0": {
    "md5": "7b1c018bf975c88fbe9df6292bf370b1", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/yaml-0.1.6-0.tar.bz2"
  }, 
  "zlib-1.2.8-3": {
    "md5": "49b15627e7048317806615d519a5b581", 
    "url": "https://repo.continuum.io/pkgs/free/osx-64/zlib-1.2.8-3.tar.bz2"
  }
}
C_ENVS = {
  "root": [
    "python-3.6.0-0", 
    "cffi-1.9.1-py36_0", 
    "conda-env-2.6.0-0", 
    "cryptography-1.7.1-py36_0", 
    "idna-2.2-py36_0", 
    "openssl-1.0.2k-0", 
    "pyasn1-0.1.9-py36_0", 
    "pycosat-0.6.1-py36_1", 
    "pycparser-2.17-py36_0", 
    "pyopenssl-16.2.0-py36_0", 
    "readline-6.2-2", 
    "requests-2.12.4-py36_0", 
    "ruamel_yaml-0.11.14-py36_1", 
    "setuptools-27.2.0-py36_0", 
    "six-1.10.0-py36_0", 
    "sqlite-3.13.0-0", 
    "tk-8.5.18-0", 
    "xz-5.2.2-1", 
    "yaml-0.1.6-0", 
    "zlib-1.2.8-3", 
    "conda-4.3.11-py36_0", 
    "pip-9.0.1-py36_1", 
    "wheel-0.29.0-py36_0"
  ]
}



def _link(src, dst, linktype=LINK_HARD):
    if on_win:
        raise NotImplementedError

    if linktype == LINK_HARD:
        os.link(src, dst)
    elif linktype == LINK_COPY:
        # copy relative symlinks as symlinks
        if islink(src) and not os.readlink(src).startswith('/'):
            os.symlink(os.readlink(src), dst)
        else:
            shutil.copy2(src, dst)
    else:
        raise Exception("Did not expect linktype=%r" % linktype)


def rm_rf(path):
    """
    try to delete path, but never fail
    """
    try:
        if islink(path) or isfile(path):
            # Note that we have to check if the destination is a link because
            # exists('/path/to/dead-link') will return False, although
            # islink('/path/to/dead-link') is True.
            os.unlink(path)
        elif isdir(path):
            shutil.rmtree(path)
    except (OSError, IOError):
        pass


def yield_lines(path):
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        yield line


prefix_placeholder = ('/opt/anaconda1anaconda2'
                      # this is intentionally split into parts,
                      # such that running this program on itself
                      # will leave it unchanged
                      'anaconda3')

def read_has_prefix(path):
    """
    reads `has_prefix` file and return dict mapping filenames to
    tuples(placeholder, mode)
    """
    import shlex

    res = {}
    try:
        for line in yield_lines(path):
            try:
                placeholder, mode, f = [x.strip('"\'') for x in
                                        shlex.split(line, posix=False)]
                res[f] = (placeholder, mode)
            except ValueError:
                res[line] = (prefix_placeholder, 'text')
    except IOError:
        pass
    return res


def exp_backoff_fn(fn, *args):
    """
    for retrying file operations that fail on Windows due to virus scanners
    """
    if not on_win:
        return fn(*args)

    import time
    import errno
    max_tries = 6  # max total time = 6.4 sec
    for n in range(max_tries):
        try:
            result = fn(*args)
        except (OSError, IOError) as e:
            if e.errno in (errno.EPERM, errno.EACCES):
                if n == max_tries - 1:
                    raise Exception("max_tries=%d reached" % max_tries)
                time.sleep(0.1 * (2 ** n))
            else:
                raise e
        else:
            return result


class PaddingError(Exception):
    pass


def binary_replace(data, a, b):
    """
    Perform a binary replacement of `data`, where the placeholder `a` is
    replaced with `b` and the remaining string is padded with null characters.
    All input arguments are expected to be bytes objects.
    """
    def replace(match):
        occurances = match.group().count(a)
        padding = (len(a) - len(b)) * occurances
        if padding < 0:
            raise PaddingError(a, b, padding)
        return match.group().replace(a, b) + b'\0' * padding

    pat = re.compile(re.escape(a) + b'([^\0]*?)\0')
    res = pat.sub(replace, data)
    assert len(res) == len(data)
    return res


def update_prefix(path, new_prefix, placeholder, mode):
    if on_win:
        # force all prefix replacements to forward slashes to simplify need
        # to escape backslashes - replace with unix-style path separators
        new_prefix = new_prefix.replace('\\', '/')

    path = os.path.realpath(path)
    with open(path, 'rb') as fi:
        data = fi.read()
    if mode == 'text':
        new_data = data.replace(placeholder.encode('utf-8'),
                                new_prefix.encode('utf-8'))
    elif mode == 'binary':
        if on_win:
            # anaconda-verify will not allow binary placeholder on Windows.
            # However, since some packages might be created wrong (and a
            # binary placeholder would break the package, we just skip here.
            return
        new_data = binary_replace(data, placeholder.encode('utf-8'),
                                  new_prefix.encode('utf-8'))
    else:
        sys.exit("Invalid mode:" % mode)

    if new_data == data:
        return
    st = os.lstat(path)
    # unlink in case the file is memory mapped
    exp_backoff_fn(os.unlink, path)
    with open(path, 'wb') as fo:
        fo.write(new_data)
    os.chmod(path, stat.S_IMODE(st.st_mode))


def name_dist(dist):
    return dist.rsplit('-', 2)[0]


def create_meta(prefix, dist, info_dir, extra_info):
    """
    Create the conda metadata, in a given prefix, for a given package.
    """
    # read info/index.json first
    with open(join(info_dir, 'index.json')) as fi:
        meta = json.load(fi)
    # add extra info
    meta.update(extra_info)
    # write into <prefix>/conda-meta/<dist>.json
    meta_dir = join(prefix, 'conda-meta')
    if not isdir(meta_dir):
        os.makedirs(meta_dir)
        with open(join(meta_dir, 'history'), 'w') as fo:
            fo.write('')
    with open(join(meta_dir, dist + '.json'), 'w') as fo:
        json.dump(meta, fo, indent=2, sort_keys=True)


def run_script(prefix, dist, action='post-link'):
    """
    call the post-link (or pre-unlink) script, and return True on success,
    False on failure
    """
    path = join(prefix, 'Scripts' if on_win else 'bin', '.%s-%s.%s' % (
            name_dist(dist),
            action,
            'bat' if on_win else 'sh'))
    if not isfile(path):
        return True
    if SKIP_SCRIPTS:
        print("WARNING: skipping %s script by user request" % action)
        return True

    if on_win:
        try:
            args = [os.environ['COMSPEC'], '/c', path]
        except KeyError:
            return False
    else:
        shell_path = '/bin/sh' if 'bsd' in sys.platform else '/bin/bash'
        args = [shell_path, path]

    env = os.environ
    env['PREFIX'] = prefix

    import subprocess
    try:
        subprocess.check_call(args, env=env)
    except subprocess.CalledProcessError:
        return False
    return True


url_pat = re.compile(r'''
(?P<baseurl>\S+/)                 # base URL
(?P<fn>[^\s#/]+)                  # filename
([#](?P<md5>[0-9a-f]{32}))?       # optional MD5
$                                 # EOL
''', re.VERBOSE)

def read_urls(dist):
    try:
        data = open(join(PKGS_DIR, 'urls')).read()
        for line in data.split()[::-1]:
            m = url_pat.match(line)
            if m is None:
                continue
            if m.group('fn') == '%s.tar.bz2' % dist:
                return {'url': m.group('baseurl') + m.group('fn'),
                        'md5': m.group('md5')}
    except IOError:
        pass
    return {}


def read_no_link(info_dir):
    res = set()
    for fn in 'no_link', 'no_softlink':
        try:
            res.update(set(yield_lines(join(info_dir, fn))))
        except IOError:
            pass
    return res


def linked(prefix):
    """
    Return the (set of canonical names) of linked packages in prefix.
    """
    meta_dir = join(prefix, 'conda-meta')
    if not isdir(meta_dir):
        return set()
    return set(fn[:-5] for fn in os.listdir(meta_dir) if fn.endswith('.json'))


def link(prefix, dist, linktype=LINK_HARD):
    '''
    Link a package in a specified prefix.  We assume that the packacge has
    been extra_info in either
      - <PKGS_DIR>/dist
      - <ROOT_PREFIX>/ (when the linktype is None)
    '''
    if linktype:
        source_dir = join(PKGS_DIR, dist)
        info_dir = join(source_dir, 'info')
        no_link = read_no_link(info_dir)
    else:
        info_dir = join(prefix, 'info')

    files = list(yield_lines(join(info_dir, 'files')))
    has_prefix_files = read_has_prefix(join(info_dir, 'has_prefix'))

    if linktype:
        for f in files:
            src = join(source_dir, f)
            dst = join(prefix, f)
            dst_dir = dirname(dst)
            if not isdir(dst_dir):
                os.makedirs(dst_dir)
            if exists(dst):
                if FORCE:
                    rm_rf(dst)
                else:
                    raise Exception("dst exists: %r" % dst)
            lt = linktype
            if f in has_prefix_files or f in no_link or islink(src):
                lt = LINK_COPY
            try:
                _link(src, dst, lt)
            except OSError:
                pass

    for f in sorted(has_prefix_files):
        placeholder, mode = has_prefix_files[f]
        try:
            update_prefix(join(prefix, f), prefix, placeholder, mode)
        except PaddingError:
            sys.exit("ERROR: placeholder '%s' too short in: %s\n" %
                     (placeholder, dist))

    if not run_script(prefix, dist, 'post-link'):
        sys.exit("Error: post-link failed for: %s" % dist)

    meta = {
        'files': files,
        'link': ({'source': source_dir,
                  'type': link_name_map.get(linktype)}
                 if linktype else None),
    }
    try:    # add URL and MD5
        meta.update(IDISTS[dist])
    except KeyError:
        meta.update(read_urls(dist))
    meta['installed_by'] = 'Miniconda3-4.3.11-MacOSX-x86_64'
    create_meta(prefix, dist, info_dir, meta)


def duplicates_to_remove(linked_dists, keep_dists):
    """
    Returns the (sorted) list of distributions to be removed, such that
    only one distribution (for each name) remains.  `keep_dists` is an
    interable of distributions (which are not allowed to be removed).
    """
    from collections import defaultdict

    keep_dists = set(keep_dists)
    ldists = defaultdict(set) # map names to set of distributions
    for dist in linked_dists:
        name = name_dist(dist)
        ldists[name].add(dist)

    res = set()
    for dists in ldists.values():
        # `dists` is the group of packages with the same name
        if len(dists) == 1:
            # if there is only one package, nothing has to be removed
            continue
        if dists & keep_dists:
            # if the group has packages which are have to be kept, we just
            # take the set of packages which are in group but not in the
            # ones which have to be kept
            res.update(dists - keep_dists)
        else:
            # otherwise, we take lowest (n-1) (sorted) packages
            res.update(sorted(dists)[:-1])
    return sorted(res)


def remove_duplicates():
    idists = []
    for line in open(join(PKGS_DIR, 'urls')):
        m = url_pat.match(line)
        if m:
            fn = m.group('fn')
            idists.append(fn[:-8])

    keep_files = set()
    for dist in idists:
        with open(join(ROOT_PREFIX, 'conda-meta', dist + '.json')) as fi:
            meta = json.load(fi)
        keep_files.update(meta['files'])

    for dist in duplicates_to_remove(linked(ROOT_PREFIX), idists):
        print("unlinking: %s" % dist)
        meta_path = join(ROOT_PREFIX, 'conda-meta', dist + '.json')
        with open(meta_path) as fi:
            meta = json.load(fi)
        for f in meta['files']:
            if f not in keep_files:
                rm_rf(join(ROOT_PREFIX, f))
        rm_rf(meta_path)


def link_idists():
    src = join(PKGS_DIR, 'urls')
    dst = join(ROOT_PREFIX, '.hard-link')
    assert isfile(src), src
    assert not isfile(dst), dst
    try:
        _link(src, dst, LINK_HARD)
        linktype = LINK_HARD
    except OSError:
        linktype = LINK_COPY
    finally:
        rm_rf(dst)

    for env_name in sorted(C_ENVS):
        dists = C_ENVS[env_name]
        assert isinstance(dists, list)
        if len(dists) == 0:
            continue

        prefix = prefix_env(env_name)
        for dist in dists:
            assert dist in IDISTS
            link(prefix, dist, linktype)

        for dist in duplicates_to_remove(linked(prefix), dists):
            meta_path = join(prefix, 'conda-meta', dist + '.json')
            print("WARNING: unlinking: %s" % meta_path)
            try:
                os.rename(meta_path, meta_path + '.bak')
            except OSError:
                rm_rf(meta_path)


def prefix_env(env_name):
    if env_name == 'root':
        return ROOT_PREFIX
    else:
        return join(ROOT_PREFIX, 'envs', env_name)


def post_extract(env_name='root'):
    """
    assuming that the package is extracted in the environment `env_name`,
    this function does everything link() does except the actual linking,
    i.e. update prefix files, run 'post-link', creates the conda metadata,
    and removed the info/ directory afterwards.
    """
    prefix = prefix_env(env_name)
    info_dir = join(prefix, 'info')
    with open(join(info_dir, 'index.json')) as fi:
        meta = json.load(fi)
    dist = '%(name)s-%(version)s-%(build)s' % meta
    if FORCE:
        run_script(prefix, dist, 'pre-unlink')
    link(prefix, dist, linktype=None)
    shutil.rmtree(info_dir)


def main():
    global ROOT_PREFIX, PKGS_DIR

    p = OptionParser(description="conda link tool used by installers")

    p.add_option('--root-prefix',
                 action="store",
                 default=abspath(join(__file__, '..', '..')),
                 help="root prefix (defaults to %default)")

    p.add_option('--post',
                 action="store",
                 help="perform post extract (on a single package), "
                      "in environment NAME",
                 metavar='NAME')

    opts, args = p.parse_args()
    if args:
        p.error('no arguments expected')

    ROOT_PREFIX = opts.root_prefix
    PKGS_DIR = join(ROOT_PREFIX, 'pkgs')

    if opts.post:
        post_extract(opts.post)
        return

    if FORCE:
        print("using -f (force) option")

    link_idists()


def main2():
    global SKIP_SCRIPTS

    p = OptionParser(description="conda post extract tool used by installers")

    p.add_option('--skip-scripts',
                 action="store_true",
                 help="skip running pre/post-link scripts")

    p.add_option('--rm-dup',
                 action="store_true",
                 help="remove duplicates")

    opts, args = p.parse_args()
    if args:
        p.error('no arguments expected')

    if opts.skip_scripts:
        SKIP_SCRIPTS = True

    if opts.rm_dup:
        remove_duplicates()
        return

    post_extract()


if __name__ == '__main__':
    if IDISTS:
        main()
    else: # common usecase
        main2()
