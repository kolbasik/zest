import argparse

def invoke(command):
  print(repr(__file__))
  parser = argparse.ArgumentParser(parents=[command])
  args = parser.parse_args()
  if args.verbose:
    print(repr(args))
