import json
from collections import defaultdict
import sys
import os

def analyze_json_file(json_file_name: str, threshold: str, columns: list) -> dict:
    try:
        with open(json_file_name, 'r', encoding="UTF-8") as json_file:
            data = json.loads(json_file.read())
    except Exception as e:
        print("[ERR] Ошибка загрузки файла. Некорректный JSON. Формат должен быть: [{key: value}, {key: value}]. " + e)
        return dict()

    analysis = defaultdict(int)

    try:
        for row in data:
            col_name = '_'.join([str(row[col]) for col in columns])
            analysis[col_name] += 1
    except Exception as e:
        print("[ERR] Ошибка записи частоты. Возможно, указана несуществующая колонка. " + str(e))
        return dict()

    keys_for_deleting = list()
    for key in analysis:
        if analysis[key] < threshold:
            keys_for_deleting.append(key)

    for key in keys_for_deleting:
        analysis.pop(key)

    return dict(analysis)

def raise_help() -> None:
    print("Для использования вызовите скрипт в следующем формате: \n" \
            + f"python {__file__.split(os.sep)[-1]} -f [json_file_name] -t [threshold] -cols col col col" 
        )

if __name__ == "__main__":
    arguments = sys.argv
    if "--help" in arguments:
        raise_help()
        sys.exit(0)

    try:
        json_file_name = arguments[arguments.index("-f") + 1]
        threshold = int(arguments[arguments.index("-t") + 1])
        
        cols = arguments[arguments.index("-cols") + 1:]
    except Exception as e:
        print("[ERR] " + str(e))
        raise_help()
        sys.exit(-1)

    print(analyze_json_file(json_file_name=json_file_name
                            , threshold=threshold
                            , columns=cols))
