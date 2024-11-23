import os
import glob

def get_savemodel_name(name:str, mod:str|None=None, direct:str='Model\\') -> str:
    file_list = glob.glob(f'{direct}{name}_*.cbm')
    if len(file_list) == 0:
        next_file_name = f'{name}_1'
    else:
        latest_file = max(file_list, key=os.path.getctime)
        last_file_num = int(latest_file.split('_')[1][:-4])
        next_file_name = f'{name}_{last_file_num+1}'
    
    if mod is not None:
        next_file_name += f'_{mod}'
    
    next_file_name += '.cbm'
    
    print(next_file_name)
    return f'{direct}{next_file_name}'