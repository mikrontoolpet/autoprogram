import pandas as pd
import asyncio

from autoprogram import tools

class App:
	"""
	Main class
	"""
	@classmethod
	async def run(cls, args):
		"""
		Main method
		"""
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
				for coro in [cls.create_tool_from_ws_row(row) for idx, row in sh.iterrows()]: # run coroutines synchronously
					await coro

			else:
				self.error_list(0)

		except RuntimeError:
			self.error_list(1)

	@classmethod
	async def create_tool(cls, name, family, params):
		"""
		Create tool from manual inputs
		"""
		family = row.loc["family"]
		Tool = cls.family_dict[family]
		async with Tool(name, *params) as tool:
			await tool.create()

	@classmethod
	async def create_tool_from_ws_row(cls, row):
		"""
		Create tool from table inputs
		"""
		family = row.loc["family"]
		Tool = cls.family_dict[family]

		name = row.loc["name"]
		params = row.filter(like="params").tolist()
		async with Tool(name, *params) as tool:
			await tool.create()
		return 0

	def error_list(self, err_id):
		"""
		In case of error
		"""
		if err_id == 0:
			print("The selected mode doesn't exist.")
		elif err_id == 1:
			print("OPC-UA client timeout error.")