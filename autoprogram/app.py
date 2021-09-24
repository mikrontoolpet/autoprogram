from autoprogram.tools import *

class App:
	async def run(args):
		name = args.name[0]
		family = args.family[0]
		params = args.params
		family_dict = {}
		for T in (drills.drills.Titanium,): # new tool classes must be added here
			family_dict[T.family_address] = T
		Tool = family_dict[family]
		tool = Tool(*params)
		await tool.create(name)