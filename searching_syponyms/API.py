
from urllib.request import urlopen
import json
import test_connect as tc

helper = tc.DBHelper('127.0.0.1','root', '1234','3306','baitap')
# helper.connectMysql()
# helper.connectDatabase()
print("correctlt connect")

f = open('3000words.txt', 'r')
list1 = f.read()
list1 = list1.split()


def search_item(item):
    # item = input("enter the word u want to find: ")
    if item in list1:
        return item
    else:
        print("wrong word, please enter the other word! ")


def get_json_data(url,path_variable):
    response = urlopen(url+"/"+ path_variable)  #response = urlopen(url+"/"+path_variable+"?limit="+request_param)
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
    get = get_json_data('https://tuna.thesaurus.com/relatedWords', each_word) # entry_word, sim_word[...], similarity_level[...]


print("done")
# get_json_data('https://tuna.thesaurus.com/relatedWords', search_item("hello"))
#
