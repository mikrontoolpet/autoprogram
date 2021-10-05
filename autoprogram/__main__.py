import asyncio
import argparse
from .app import App

parser = argparse.ArgumentParser()
parser.add_argument('--machine', type=str, nargs=1)
parser.add_argument('--mode', type=str, nargs=1)
parser.add_argument('--name', type=str, nargs="+")
parser.add_argument('--family', type=str, nargs="+")
parser.add_argument('--params', type=str, nargs="+")
parser.add_argument('--create_file_path', type=str, nargs="+")
args = parser.parse_args()

if __name__ == '__main__':
	asyncio.run(App.run(args))