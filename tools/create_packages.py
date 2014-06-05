from __future__ import print_function
import getpass
import sys
import shutil
from subprocess import Popen, PIPE
import os
import fileinput
from operator import methodcaller

__author__ = 'Maxaon'

join = lambda *s: os.path.abspath(os.path.join(*s))
import argparse
from Crypto.PublicKey import RSA

parser = argparse.ArgumentParser(description='Create extension and add keys.')
parser.add_argument('--domains', default="http://localhost:8000/",
                    help="Coma separated domains, where extension will be work")
parser.add_argument('--public-key', default=None, help="Public key, which will be used to verify domain")
parser.add_argument('--extension-key', default=None, help="Key to sign extension")
parser.add_argument('--name', default=None, help="Name of the file extencion")
parser.add_argument('--destination', default=None, help="Name of the file extencion")

chrome_manual_path = None


def write(file_path, b):
    with open(file_path, "w") as h:
        h.write(b)


def _find_chrome():
    chrome_path = chrome_manual_path
    if not chrome_path:
        if os.name == 'nt':
            chrome_path = os.path.expandvars(r'%programfiles(x86)%\Google\Chrome\Application\chrome.exe')
            if not os.path.isfile(chrome_path):
                chrome_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe')
        elif os.name == 'posix':
            for name in ('google-chrome', 'google-chrome-stable', 'chrome'):
                p = Popen(['which', name], stdout=PIPE)
                res = p.wait()
                if res == 0:
                    chrome_path = p.stdout.readline().strip()
                    break
    if not chrome_path:
        raise Exception("Can not find chrome executable path")
    return chrome_path


def _genrate_rsa_keypari(name, encrypt=True):
    key_password = None
    if encrypt:
        key_password = getpass.getpass()
        if not key_password:
            exit("Password can't be empty")
    key = RSA.generate(2048)
    ext = None
    if "." in name:
        name, ext = name.split(".")
    if ext == 'pem':
        write(name + '.pem', key.exportKey('PEM', key_password))
    if not ext or ext == 'pub':
        public_key = key.publickey()
        write(name + '.pub', public_key.exportKey('PEM'))


def _copy_extension_path(extension_srs, ext_path):
    try:
        shutil.rmtree(ext_path)
    except OSError:
        pass
    shutil.copytree(extension_srs, ext_path)


def _modify_background_file(domains_formated, public_key_path, temp_ext_path):
    for line in fileinput.input(join(temp_ext_path, "background.js"), inplace=True):
        if "var public_key" in line:
            with open(public_key_path) as pk:
                pkl = map(str.strip, pk.readlines())
                print("var public_key='{}'+".format(pkl[0]), end="")
                for l in pkl[1:-1]:
                    print("\n               '{}'+".format(l), end="")
                print("\n               '{}';".format(pkl[-1]))
        elif "http://localhost:8000/*" in line:
            print(line.replace('"http://localhost:8000/*"', domains_formated), end="")
        else:
            print(line, end="")


def _modify_manifest_file(domains_formated, temp_ext_path):
    for line in fileinput.input(join(temp_ext_path, "manifest.json"), inplace=True):
        if '"http://*/*"' in line:
            print(line.replace('"http://*/*"', domains_formated), end="")
        else:
            print(line, end="")


def main(args=None):
    extension_srs = join(os.path.dirname(__file__), '../chrome_extension')
    domains = map(methodcaller('rstrip', '/'), args.domains.split(","))
    domains_formated = ", ".join(map(lambda d: '"{}/*"'.format(d), domains))
    public_key_path = args.public_key
    if not args.public_key:
        if os.path.isfile('key.pub'):
            public_key_path = "key.pub"
        else:
            public_key_path = "key.pub"
            _genrate_rsa_keypari('key')
    public_key_path = join(public_key_path)
    ext_name = args.name or 'signature-check'
    temp_ext_path = join('tmp', ext_name)
    _copy_extension_path(extension_srs, temp_ext_path)

    _modify_background_file(domains_formated, public_key_path, temp_ext_path)
    _modify_manifest_file(domains_formated, temp_ext_path)
    chrome_path = _find_chrome()
    chrome_cmd = [chrome_path, '--pack-extension=' + temp_ext_path]
    if not args.extension_key and os.path.isfile('extension_key.pem'):
        args.extension_key = 'extension_key.pem'
    if args.extension_key:
        chrome_cmd.append('--pack-extension-key=' + join(args.extension_key))

    p = Popen(chrome_cmd)
    if p.wait() != 0:
        exit("Cant't create package")

    if not args.extension_key:
        os.rename(temp_ext_path + '.pem', join('extension_key.pem'))

    if args.destination:
        if args.destination.endswith('.crx'):
            destination = args.destination
        else:
            destination = join(args.destination, ext_name + '.crx')
    else:
        destination = ext_name + '.crx'
    try:
        os.unlink(destination)
    except OSError:
        pass
    os.rename(temp_ext_path + '.crx', destination)
    shutil.rmtree(join(temp_ext_path, '..'))


if __name__ == '__main__':
    main(parser.parse_args())
