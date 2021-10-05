import pandas as pd
import asyncio
import time

from autoprogram import config
from autoprogram import tools
from autoprogram.vgpro import VgPro

class App:
	"""
	Main class
	"""
	@classmethod
	async def run(cls, args):
		"""
		Main method
		"""
		machine = args.machine[0]
		with VgPro(config.VGPRO_PATH, machine) as vgp:
			print(f"Waiting for {config.VGPRO_PATH} to start...", flush=True)
			await asyncio.sleep(20)
			print(f"{config.VGPRO_PATH} started!", flush=True)
			try:
				mode = args.mode[0]
				# Initialize all available tool classes
				cls.family_dict = {}
				for T in (tools.drills.drills.Titanium,): # new tool classes must be added here
					cls.family_dict[T.family_address] = T
				if mode == "create_manual":
					name = args.name[0]
					family = args.family[0]
					params = args.params
					await cls.create_tool(name, family, params)
				elif mode == "create_auto":
					create_file_path = args.create_file_path[0]
					sh = pd.read_excel(create_file_path, sheet_name=0)
					for idx, row in sh.iterrows():
						family = row.loc["family"]
						name = row.loc["name"]
						params = row.filter(like="params").tolist()
						res = await cls.create_tool(name, family, params)
				else:
					cls.error_list(0)
			except RuntimeError:
				cls.error_list(1)

	@classmethod
	async def create_tool(cls, name, family, params):
		"""
		Create tool from name, family and a variable number of parameters,
		depending on how many arguments are needed by the class representing
		the tool.
		"""
		Tool = cls.family_dict[family]
		async with Tool(name, *params) as tool:
			res = await tool.create()

	@classmethod
	def error_list(cls, err_id):
		"""
		In case of error
		"""
		if err_id == 0:
			return ValueError("The selected mode doesn't exist.")
		elif err_id == 1:
			return TimeoutError("OPC-UA client timeout error.")