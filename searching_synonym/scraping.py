
from urllib.request import urlopen
import json
import connection_db as conn


helper = conn.DBHelper('127.0.0.1','root', '1234','3306','baitap')
print("correctlt connect")


f = open('3000words.txt', 'r')
list1 = f.read()
list1 = list1.split()


def get_json_data(url,path_variable):
    """
    Lấy API từ Web https://www.thesaurus.com/browse/synonym
    Lấy các từ đồng nghĩa vs mức độ đồng nghĩa của nó
    :param url:
    :param path_variable: Biến đường dẫn
    :return:
    """
    response = urlopen(url+"/"+ path_variable)
    data_json = json.loads(response.read())
    sql = "insert into entry_similar_word(entry_word, sim_word, similarity) values(%s, %s, %s)"
    data_1 = data_json["data"]
    sim_word = []
    similarity = []
    entry_word = []
    print(len(data_1))

    for each in range(len(data_1)):
        data_2 = data_1[each]
        if data_2['targetTerm'] not in sim_word:
            entry_word.append(data_2['entry'])
            sim_word.append(data_2['targetTerm'])
            similarity.append(((data_2['synonyms'])[0])['similarity'])

    for i in range(len(entry_word)):
        a = (entry_word[i], sim_word[i], similarity[i])
        helper.insert(sql, *a)
        print(a)


for each_word in list1[1:]:
    get = get_json_data('https://tuna.thesaurus.com/relatedWords', each_word)


print("done")
