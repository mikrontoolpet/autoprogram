import asyncio
import argparse
from .app import App

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, nargs=1)
parser.add_argument('--family', type=str, nargs=1)
parser.add_argument('--params', type=float, nargs="+")
args = parser.parse_args()

if __name__ == '__main__':
	asyncio.run(App.run(args))