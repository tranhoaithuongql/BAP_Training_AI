
from urllib.request import urlopen
import json
import connection_db as conn


helper = conn.DBHelper('127.0.0.1','root', '1234','3306','baitap')
print("correctlt connect")


f = open('3000words.txt', 'r')
list1 = f.read()
list1 = list1.split()


def get_json_data(url,path_variable, entry_id):
    """
    Lấy API từ Web https://www.thesaurus.com/browse/synonym
    Lấy các từ đồng nghĩa vs mức độ đồng nghĩa của nó
    :param url:
    :param path_variable: Biến đường dẫn
    :return:
    """
    try:
        response = urlopen(url+"/"+ path_variable)
        data_json = json.loads(response.read())
        sql = "insert into synonym(entry_word_id, sim_word, similarity) values(%s, %s, %s)"
        data_1 = data_json["data"]
        sim_word = []
        similarity = []
        entry_word = []
        for each in range(len(data_1)):
            data_2 = data_1[each]
            if data_2['targetTerm'] not in sim_word:
                entry_word.append(data_2['entry'])
                sim_word.append(data_2['targetTerm'])
                similarity.append(((data_2['synonyms'])[0])['similarity'])

        for i in range(len(entry_word)):
            a = (entry_id, sim_word[i], similarity[i])
            helper.insert(sql, *a)
            print(a)
    except:
        pass

entry_id = 0
for each_word in list1[1:]:
    get = get_json_data('https://tuna.thesaurus.com/relatedWords', each_word, entry_id)
    entry_id += 1
    print('done')


