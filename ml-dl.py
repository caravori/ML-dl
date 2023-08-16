import requests
import json
import subprocess
import os
from shlex import split
from timeit import default_timer as timer
from datetime import timedelta


def main():
    header = {'X-Requested-With': 'XMLHttpRequest'}
    
    print('Código do manga:  ')
    index = 1

    inp = input()

    try:
        os.mkdir(f'./manga/manga_{inp}')
        print(f'Created folder manga_{inp}\n')
    except OSError as error:
        print(error)

    while(True):
        link = f'https://mangalivre.net/series/chapters_list.json?page={index}&id_serie={inp}'
        r = requests.get(link, headers=header)
        text = json.loads(r.text)
        if(not text['chapters']):
            break

        for chaps in text['chapters']:
            cap_number = chaps['number']
            id_scan = list(chaps['releases'].keys())
            cap_id = chaps['releases'][id_scan[0]]['id_release']
            print(f'Starting Cap {cap_number} with id of {cap_id}: ')
            try:
                os.mkdir(f'./manga/manga_{inp}/capitulo_{cap_number}')
                print(f'\tCreated folder manga_{inp}/capitulo_{cap_number}')
            except OSError as error:
                print(error)
            link = f'https://mangalivre.net/leitor/pages/{cap_id}.json'
            r = requests.get(link)
            text = json.loads(r.text)

            big_append = ""
            for index in range(len(text['images'])):
                image = text['images'][index]['legacy']
                big_append += f"{image} "
            
            command = f'wget {big_append} -P ./manga/manga_{inp}/capitulo_{cap_number}'
            start = timer()
            subprocess.run(split(command), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            end = timer()
            print(f'\tChapter {cap_number} done in {timedelta(seconds=end-start)} seconds\n')
            
        index +=1


if __name__ == '__main__':
    main()