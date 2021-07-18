from pprint import pprint
from typing import List, Union
import os
import sys
import configparser
import argparse
import logging
import shlex
import subprocess

from httpie import core as httpie




def main(args: List[Union[str, bytes]] = sys.argv):
    module_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.getenv('HTTPIES_BASEDIR', False)
    args, urlscript_args = parse_args()
    log_level = args.verbose
    logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)

    if base_dir is False:
        logging.critical('$HTTPIES_BASEDIR not set, please add HTTPIES_BASEDIR to your environment variables.')
        sys.exit(-1)

    config = parse_config(module_dir, base_dir)

    props = merge_config(config, args)
    logging.debug("using base_dir: %s" % props['base_dir'])

    if not os.path.isdir(props['base_dir']):
        logging.critical('- Base_dir "%s" does not exist, exiting' % props['base_dir'])
        sys.exit(-1)
    props = find_executable(props, config)

    httpie_args = exec_url_script(props, get_script_args(urlscript_args))
    logging.info("your url-script returned:")
    logging.info(httpie_args.decode('utf-8'))

    exit_status = exec_request(httpie_args)

    sys.exit(exit_status)


def parse_args():
    arg_parser = argparse.ArgumentParser(
                                prog="httpies",
                                description="Script httie requests and execute them by url.",
                                epilog="Add \"param=value\" pairs to the command to pass arguments to you urls scripts (used for GET/POST values). \n"
                                       "To UNSET a parameter that is set within your url script, use \"param=None\"",
                                usage="%(prog)s get.py /user/profile script_arg_1=value script_arg_2=value script_unset_value=None"
                             )

    arg_parser.add_argument('method', choices=['get', 'post', 'put', 'patch', 'delete'], help="Http request method")
    arg_parser.add_argument('url', help="The url to request (ea. /user/profile)")
    arg_parser.add_argument('-c', '--config',  help="Set config file to read")
    arg_parser.add_argument('-b', '--basedir',
                            help="Set the url script base dir, will overwrite config file and environment")
    arg_parser.add_argument('-d', '--domain', help="Used to override the domain (ea. https://example.com)")
    arg_parser.add_argument('-v', '--verbose',
                            help="Set log-level (10=debug, 50=critical)",
                            type=int,
                            default=logging.WARNING,
                            choices=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
                            )
    args, script_args = arg_parser.parse_known_args()
    return args, script_args


def parse_config(module_dir, base_dir):
    base_file = os.path.join(base_dir, 'httpies.conf')
    mod_file = os.path.join(module_dir, 'httpies.conf')
    if not os.path.isfile(base_file):
        logging.info(
            "Reading config from %s, you can overwrite this by adding httpies.conf to your base_dir" % mod_file
        )

    config = configparser.RawConfigParser()
    config.read([mod_file, base_file])
    return config


def merge_config(config, args):
    props = {
        "base_dir":os.getenv('HTTPIES_BASEDIR'),
        "executable": config.get('global', 'httpie_executable_name'),
        "method": args.method,
        "domain": args.domain if args.domain else os.getenv('HTTPIES_DEFAULT_DOMAIN',
                                                            config.get('global', 'default_domain')
                                                            ),
        "url": args.url,
        "script_file": None,
        "verbose": args.verbose
    }
    if args.basedir:
        props['base_dir'] = os.path.realpath(args.basedir)

    url = props['url']
    if url[0] == '/':
        url = url[1:]

    props['script_file'] = os.path.join(props['base_dir'],
                                        config.get('global', 'url_script_dir'),
                                        url,
                                        props['method'].lower()
                                        )
    return props


def get_script_args(script_args):
    return_list = []
    dashes = '--'
    for arg in script_args:
        splitted = arg.split('=', 1)
        if len(splitted) == 2:
            return_list.append("%s=%s" % (splitted[0], shlex.quote(splitted[1]),))
        else:
            return_list.append("%s%s" % (dashes, shlex.quote(arg)))
            if dashes == '':
                dashes = '--'
            else:
                dashes = ''
    return return_list


def find_executable(props, config):
    logging.info("Looking for url-script: %s" % props['script_file'])
    if os.path.isfile(props['script_file']):
        if not os.access(props['script_file'], os.X_OK):
            if config.get('global', 'chmod_url_scripts') == 'yes':
                logging.warning('Script file is not executable, running "chmod 0777 %s"' % props['script_file'])
                os.system('chmod 0755 %s' % props['script_file'])
                if not os.access(props['script_file'], os.X_OK):
                    logging.critical('Script is not executable, exiting')
                    sys.exit(-1)
            else:
                logging.critical('Script is not executable, exiting')
                sys.exit(-1)
        logging.info("Found: %s" % props['script_file'])
        return props

    elements = dict(config.items('executables'))
    for ext, exe in elements.items():
        new_path = "%s.%s" % (props['script_file'], ext,)
        logging.debug('Trying: %s' % new_path)
        if os.path.isfile(new_path):
            props['exec_with'] = exe.replace('[HTTPIES_BASEDIR]', props['base_dir'])
            props['script_file'] = new_path
            logging.info("Found: %s" % props['script_file'])
            return props

    logging.critical('- %s does not exist, exiting' % props['script_file'])
    sys.exit(-1)

def exec_url_script(props, script_args):
    command_list = [
        props['script_file'],
        '%s' % shlex.quote(props['method'].upper()),
        '"%s"' % shlex.quote(props['domain']),
        '"%s"' % shlex.quote(props['url'])

    ]
    if props['exec_with']:
        command_list.insert(0, props['exec_with'])

    command_list.extend(script_args)
    logging.info("Executing: %s" % " ".join(command_list))
    proc = subprocess.Popen(" ".join(command_list), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = proc.communicate()
    if len(stderr) > 0:
        logging.critical('%s : %s ' % (props['script_file'], stderr))
    if proc.returncode != 0:
        logging.critical('Url-script returned a non-zero exitcode, it returned "%s"', proc.returncode)
        logging.critical("tried to execute: %s" % " ".join(command_list))
        # I really just wanna dump the contents of the script... for debugging
        # @todo is this how we wanna do this.
        if props['verbose'] < 50:
            print("\n DISABLE THIS MESSAGE using -v 50")
            print("The stdout from your url-script was: \n")
            print("%s" % stdout.decode("utf-8"))
            print("The stderr from your url-script was: \n")
            print("%s" % stderr.decode("utf-8"))
        sys.exit(proc.returncode)

    return stdout

def exec_request(httpie_args):
    args = httpie_args.splitlines()
    args = [x.strip() for x in args]
    httpie.main(args)

