import os, importlib, argparse

ZEST_NAME = 'zest'
ZEST_VERSION = '0.0.5'
ZEST_GIT = 'https://github.com/kolbasik/zest'

parser = argparse.ArgumentParser(
  prog=ZEST_NAME,
  description='%s cli is a distributed command runner' % ZEST_NAME,
  epilog='see more: %s' % ZEST_GIT,
  add_help=False
)
parser.add_argument('command', type=str)
parser.add_argument('--zwd', type=str, default=ZEST_NAME)
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

# https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
if not os.path.exists(args.zwd):
  def download(url, file_name):
    try: # 2.7
      import urllib
      urllib.urlretrieve(url, file_name)
    except AttributeError: # 3.8
      import urllib.request, shutil
      with open(file_name, 'wb') as file:
        with urllib.request.urlopen(url) as response:
          shutil.copyfileobj(response, file)

  def unzip(zip_file_name, dest):
    import zipfile
    with zipfile.ZipFile(zip_file_name) as zip_file:
      zip_file.extractall(dest)
      return zip_file.namelist()[0]

  zest_zip = '%s.zip' % ZEST_NAME
  download('%s/archive/%s.zip' % (ZEST_GIT, os.getenv("ZEST_VERSION", ZEST_VERSION)), zest_zip)
  os.rename(unzip(zest_zip, '.'), args.zwd)
  os.remove(zest_zip)

try:
  imported_command = importlib.import_module(
    '.%s' % args.command,
    package='%s.commands' % (args.zwd if args.zwd != '.' else '')
  )
  imported_command.invoke(parser)
except ModuleNotFoundError:
  print('Unknown command: %s' % args.command)
