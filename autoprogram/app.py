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
		machine = args.machine[0] # machine can be specified only here
		async with VgPro(config.VGPRO_EXE_PATH, machine, config.SERVER_URL) as vgp_client:
			# Initialize all available tool classes
			cls.family_dict = {}
			for T in (tools.drills.drills.titaniumg5.Tool,): # new tool classes must be added here
				cls.family_dict[T.family_address] = T

			# Different tool creation methods depending on the mode parameter
			mode = args.mode[0]
			if mode == "create_manual":
				await cls.create_manual(vgp_client, args)
			elif mode == "create_auto":
				await cls.create_auto(vgp_client, args)
			else:
				cls.error_list(0)

	@classmethod
	async def create_tool(cls, vgp_client, name, family, params):
		"""
		Create tool from name, family and a variable number of parameters,
		depending on how many arguments are needed by the class representing
		the tool.
		"""
		try:
			ToolFamily = cls.family_dict[family]
		except KeyError:
			cls.error_list(2)

		async with ToolFamily(vgp_client, name, *params) as tool:
			await tool.create()

	@classmethod
	async def create_manual(cls, vgp_client, args):
		name = args.name[0]
		family = args.family[0]
		params = args.params
		await cls.create_tool(vgp_client, name, family, params)

	@classmethod
	async def create_auto(cls, vgp_client, args, row):
		create_file_path = args.create_file_path[0]
		sh = pd.read_excel(create_file_path, sheet_name=0)
		for idx, row in sh.iterrows():
			family = row.loc["family"]
			name = row.loc["name"]
			params = row.filter(like="params").tolist()
			await cls.create_tool(vgp_client, name, family, params)

	@classmethod
	def error_list(cls, err_id):
		"""
		In case of error
		"""
		if err_id == 0:
			raise ValueError("The selected mode doesn't exist.")
		elif err_id == 1:
			raise TimeoutError("OPC-UA client timeout error.")
		elif err_id == 2:
			raise ValueError("Specified tool family doesn't exist.")