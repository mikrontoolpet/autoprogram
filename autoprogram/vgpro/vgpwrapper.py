import asyncio

from .vgpapp import VgpApp
from .vgpclient import VgpClient

class VgpWrapper:
	"""
	Wrap vgp server and client
	"""
	def __init__(self, machine):
		self.machine = machine
		self.vgp_app = VgpApp(self.machine)
		self.vgp_client = VgpClient()

	async def __aenter__(self):
		"""
		Start VgPro application and connect the client to the OPC-UA server
		"""
		self.vgp_app.__enter__()
		await self.vgp_client.__aenter__() # this __aenter__ method return a connected VgpClient instance
		return self # very important!!!

	async def __aexit__(self, exc_type, exc_value, traceback):
		"""
		Disconnect client and close VgPro application
		"""
		await self.vgp_client.__aexit__(exc_type, exc_value, traceback)
		self.vgp_app.__exit__(exc_type, exc_value, traceback)