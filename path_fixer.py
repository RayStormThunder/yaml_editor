import re

def sanitize_path_component(name: str) -> str:
	"""
	Removes or replaces characters not allowed in Windows filenames.
	These include: \ / : * ? " < > |
	"""
	return re.sub(r'[<>:"/\\|?*]', '~', name)
