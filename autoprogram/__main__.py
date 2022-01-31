import asyncio
import argparse
from .app import App



async def main():
	"""
	CLI arguments are passed while instancing the App class, subsequently they
	will passed using GUI windows inside the app
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('--machine', type=str, nargs=1)
	parser.add_argument('--mode', type=str, nargs=1)
	parser.add_argument('--name', type=str, nargs="+")
	parser.add_argument('--family', type=str, nargs="+")
	parser.add_argument('--params', type=str, nargs="+")
	parser.add_argument('--create_file_path', type=str, nargs="+")
	cli_args_ns = parser.parse_args()
	cli_args_dict = vars(cli_args_ns)
	# Page 1 - select machine
	# GUI HERE TO SELECT MACHINE!!!
	cli_machine = cli_args_dict["machine"][0]
	async with App(cli_machine, cli_args_dict) as app:
		await app.run()

if __name__ == '__main__':
	asyncio.run(main())