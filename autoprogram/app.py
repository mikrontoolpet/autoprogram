import pandas as pd
import asyncio
import time

from autoprogram import config
from autoprogram import tools
from autoprogram.vgpro import VgpApp, VgpClient

class App:
	"""
	Application class
	"""
	def __init__(self, machine, cli_args_dict): #_machine, _mode, _name, _family, _params, _create_file_path):
		"""
		Initialize user defined variables from cli
		"""
		self.machine = machine
		# THESE INSTANCE VARIABLES WILL BE DEFINED FROM GUI!!!
		# Page 2 (mode)
		self.cli_mode = cli_args_dict["mode"][0]
		# Page 3 - case "manual" (tool-specific arguments)
		if self.cli_mode == "manual":
				self.cli_name = cli_args_dict["name"][0]
				self.cli_family = cli_args_dict["family"][0]
				self.cli_params = cli_args_dict["params"]
		elif self.cli_mode == "auto":
			# Page 4 - case "auto" (arguments from spreadsheet)
			self.create_file_path = cli_args_dict["create_file_path"][0]
		else:
			self.error_list(0, self.cli_mode)

		# THESE INSTANCE VARIABLES STAY!!!
		self.vgp_app = VgpApp(self.machine)
		self.vgp_client = VgpClient()

	async def __aenter__(self):
		"""
		Start VgPro application
		"""
		self.vgp_app.__enter__()
		await self.vgp_client.__aenter__() # this __aenter__ method return a connected VgpClient instance
		return self # very important!!!

	async def __aexit__(self, exc_type, exc_value, traceback):
		"""
		Close VgPro application
		"""
		await self.vgp_client.__aexit__(exc_type, exc_value, traceback)
		self.vgp_app.__exit__(exc_type, exc_value, traceback)

	def init_tool_classes(self):
		"""
		Initialize all available tool classes and put them in self.family_dict
		"""
		self.family_dict = {}
		for T in (tools.drills.drills.titaniumg5.Tool, tools.drills.drills.ic.Tool): # new tool classes must be added here
			self.family_dict[T.family_address] = T

	async def run(self):
		"""
		Main method
		"""
		self.init_tool_classes()

		# SELECT MODE GUI HERE!!!
		# Page 2 (mode)

		# Different tool creation methods depending on the mode parameter
		# In the "manual" mode, all parameters are taken from cli
		if self.cli_mode == "manual":
			# USER PARAMETERS GUI HERE!!! Page 3 - case "manual" (tool-specific arguments)
			# assign user defined variables (from GUI instead of cli arguments)
			name = self.cli_name
			family = self.cli_family
			params = self.cli_params
			await self.create_tool(name, family, params)
		# In the "auto" mode, tool parameters are taken from a spreadsheet
		elif self.cli_mode == "auto":
			# CREATE FILE BROWSE GUI HERE!!! Page 4 - case "auto" (arguments from spreadsheet)
			# assign create file path (from GUI instead of cli arguments)
			create_file_path = self.create_file_path
			await self.create_auto(create_file_path)
		else:
			self.error_list(0, mode)

	async def create_tool(self, name, family, params):
		"""
		Create single tool from name, family and a variable number of parameters,
		depending on how many arguments are needed by the class representing
		the tool.
		"""
		try:
			ToolFamily = self.family_dict[family]
		except KeyError:
			self.error_list(2, family)

		# an active VgpClient instance must be passed to the ToolFamily instance,
		# in order to be able to call the OPC-UA functions
		async with ToolFamily(self.machine, self.vgp_client, name, *params) as tool: # tool is an instance of the ToolFamily class
			await tool.create()

	async def create_auto(self, create_file_path):
		"""
		Takes the first sheet, parse the user parameters for every row and
		create the tool
		"""
		sh = pd.read_excel(create_file_path, sheet_name=0)
		for idx, row in sh.iterrows():
			family = row.loc["family"]
			name = row.loc["name"]
			params = row.filter(like="params").tolist()
			try:
				await self.create_tool(name, family, params)
			except Exception:
				pass

	def error_list(self, err_id, *args, **kwargs):
		"""
		In case of error
		"""
		if err_id == 0:
			raise ValueError(f"The selected mode doesn't exist: {self.cli_mode}")
		elif err_id == 1:
			raise TimeoutError("OPC-UA client timeout error.")
		elif err_id == 2:
			raise ValueError(f"{args[0]} tool family doesn't exist.")