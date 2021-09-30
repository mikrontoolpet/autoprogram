from autoprogram import tools

class App:
	async def run(args):
		name = args.name[0]
		family = args.family[0]
		params = args.params
		family_dict = {}
		for T in (tools.drills.drills.Titanium,): # new tool classes must be added here
			family_dict[T.family_address] = T
		Tool = family_dict[family]
		async with Tool(name, *params) as tool:
			await tool.create()