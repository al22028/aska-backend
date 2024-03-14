import json

def key_with_min_value(data_dict:dict) -> str:
    min_value_key = min(data_dict, key=data_dict.get)
    return min_value_key

def transform_data(data:dict) -> dict:
    transformed = {}
    for outer_key, inner_dict in data.items():
        for inner_key, value in inner_dict.items():
            if inner_key not in transformed:
                transformed[inner_key] = {}
            transformed[inner_key][outer_key] = value
    return transformed

def in_check(l:list[tuple],id:str,rc:int) -> bool:
    for tup in l:
        if tup[rc] == id:
            return True
    return False

def extract_value(l:list[tuple],row_id:str,col_id:str) -> tuple:
    for d in l:
        if d[0] == row_id :return d
        if d[1] == col_id :return d
    return ("","")

def find_page_matching() -> None:
    with open("sandbox/zaki/data/similarity_score.json","r") as sim:
        data = json.load(sim)
    data = data[0]
    t_data = transform_data(data)

    row_mins = [(d,key_with_min_value(data[d])) for d in (data.keys())]
    col_mins = [(key_with_min_value(t_data[d]),d) for d in (t_data.keys())]

    result = []

    for rows in row_mins.copy():
        if rows in col_mins:
            result.append(rows)
            row_mins.pop(row_mins.index(rows))
            col_mins.pop(col_mins.index(rows))


    for i in row_mins:
        if not in_check(result,i[0],0):
            row_pair = extract_value(row_mins,i[0],"")
            col_pair = extract_value(col_mins,i[0],"")
            if not in_check(result,row_pair[1],0) and row_pair != ("","") : result.append(row_pair)
            if not in_check(result,col_pair[1],1) and col_pair != ("","") : result.append(col_pair)

    print(result)

if __name__ == '__main__':
    find_page_matching()



