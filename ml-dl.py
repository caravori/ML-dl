import requests
import json
import os



def main():
    header = {'X-Requested-With': 'XMLHttpRequest'}
    
    print('Código do manga:  ')
    index = 1

    inp = input()
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
            print(f'cap: {cap_number} id: {cap_id}')
            try:
                os.mkdir(f'./manga/manga_{inp}/capitulo_{cap_number}')
            except OSError as error:
                print(error)
            link = f'https://mangalivre.net/leitor/pages/{cap_id}.json'
            r = requests.get(link)
            text = json.loads(r.text)
            for index in range(len(text['images'])):
                image = text['images'][index]['legacy']
                print(f'Imagem {index}: {image}\n')
                os.system(f'wget {image} -P ./manga/manga_{inp}/capitulo_{cap_number}')
        
        index +=1


if __name__ == '__main__':
    main()