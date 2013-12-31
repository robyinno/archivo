def capitalize_lang_path(path_file):
	index = 0 
	path_infos = path_file.split('/')
	new_path_infos = []
	for path_info in path_infos:
		if index == 1 :
			path_add = path_info.capitalize()
		else:
			path_add = path_info
		new_path_infos.append(path_add)
		index = index + 1
	return '/'.join(new_path_infos)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d