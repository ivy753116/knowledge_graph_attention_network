from collections import defaultdict
from multiprocessing import Process


def load_data(data_name):
    item_list = []
    user_list = []
    train_dict = defaultdict(list)
    negative_dict = defaultdict(list)
    # Load trian data ; return train_dict[user id]: item id on movielens, negative_dict[user id]: item id on movielens, item_list(raw item id), user_list(raw user id)
    with open("./"+data_name+"/raw_data/train.dat") as f:
        for line in f:
            line = line.split()
            if (int(line[2].strip())>=4): # user's score of movie >=4
                train_dict[line[0]].append(line[1].strip())
            else:
                negative_dict[line[0]].append(line[1].strip())
            item_list.append( str(line[1].strip().strip()) )
            user_list.append( str(line[0].strip().strip()) )

    with open("./"+data_name+"/raw_data/valid.dat") as f:
        for line in f:
            line = line.split()
            if (int(line[2].strip())>=4):
                train_dict[line[0]].append(line[1].strip())
            else:
                negative_dict[line[0]].append(line[1].strip())
            item_list.append( str(line[1].strip().strip()) )
            user_list.append( str(line[0].strip().strip()) )

    # Load test data ; return test_dict[user id]: item id on movielens, negative_dict[user id]: item id on movielens, item_list(raw item id), user_list(raw user id)
    test_dict = defaultdict(list)
    with open("./"+data_name+"/raw_data/test.dat") as f:
        for line in f:
            line = line.split()
            if (int(line[2].strip())>=4):
                test_dict[line[0]].append(line[1].strip())
            else:
                negative_dict[line[0]].append(line[1].strip())
            item_list.append( str(line[1].strip().strip()) )
            user_list.append( str(line[0].strip().strip()) )

    #Load item to kg map data; return item_dict[item link on dbpedia]: item id on movielens
    item_dict = defaultdict(list)
    with open("./"+data_name+"/raw_data/i2kg_map.tsv") as f:
        for line in f:
            line = line.split()
            item_dict[line[-1]].append(line[0].strip())

    #Load kg relation map data; return relation_dict[relation link on dbpedia]: relation id
    relation_dict = defaultdict(list)
    with open("./"+data_name+"/raw_data/kg/r_map.dat") as f:
        for line in f:
            line = line.split()
            relation_dict[line[0]].append(line[1].strip())

    #Load kg entity map data; return entity_dict[entity link on dbpedia]: entity id in dbpedia
    entity_dict = defaultdict(list)
    with open("./"+data_name+"/raw_data/kg/e_map.dat") as f:
        for line in f:
            line = line.split()
            entity_dict[line[-1]].append(line[0].strip())

    # Load kg test data; return movie_list(entity of item id on dbpedia), entity_list(entity of others id on dbpedia), relation_list(relation id on dbpedia)
    entity_1_list = []
    entity_2_list = []
    relation_list = []
    with open("./"+data_name+"/raw_data/kg/test.dat") as f:
        for line in f:
            line = line.split()
            if len(line) == 3:
                entity_1_list.append(line[0])
                entity_2_list.append(line[1])
                relation_list.append(line[2])

    # Load kg train data; same as above
    with open("./"+data_name+"/raw_data/kg/train.dat") as f:
        for line in f:
            line = line.split()
            if len(line) == 3:
                entity_1_list.append(line[0])
                entity_2_list.append(line[1])
                relation_list.append(line[2])

    # Load kg valid data; same as above
    with open("./"+data_name+"/raw_data/kg/valid.dat") as f:
        for line in f:
            line = line.split()
            if len(line) == 3:
                entity_1_list.append(line[0])
                entity_2_list.append(line[1])
                relation_list.append(line[2])

    return train_dict, test_dict, negative_dict, entity_dict, user_list, item_list, entity_1_list, entity_2_list, relation_dict, relation_list, item_dict


def gen_kgat(data_name, train_dict, test_dict, negative_dict, entity_dict, user_list, item_list, entity_1_list, entity_2_list, relation_dict, relation_list, item_dict):
    user_index_dict = {}
    item_index_dict = {}
    entity_index_dict = {}

    item_entity_dict = {}
    entity_item_dict = {}
    item_entity_list = []
    item_entity_list.append([])
    item_entity_list.append([])

    # map item id with entity id and make dictionary
    for i in item_dict.keys():
        for j in entity_dict.keys():
            if i == j:
                item = str(''.join(str(s) for s in item_dict[i]))
                entity = str(''.join(str(s) for s in entity_dict[j]))
                item_entity_dict[entity] = item
                entity_item_dict[item] = entity

    with open('./'+data_name+'/item_entity_list.txt', 'w') as f:
        f.write("org_id freebase_id\n")
        for entity in item_entity_dict:
            item_entity_list[0].append(item_entity_dict[entity])
            item_entity_list[1].append(entity)
            f.write(item_entity_dict[entity]+" "+entity+"\n")

    with open('./'+data_name+'/user_list.txt', 'w') as f:
        user_list = list(set(user_list))
        f.write("org_id remap_id\n")
        for user_index, i in enumerate(user_list):
            user_index_dict[i] = str(user_index)
            f.write(i+" "+str(user_index)+"\n")

    with open('./'+data_name+'/item_list.txt', 'w') as f:
        item_list_ = list(set(item_list))
        entity_1_list_ = list(set(entity_1_list))
        f.write("org_id remap_id freebase_id\n")
        for index_item, i in enumerate(item_list_):
            item_index_dict[i] = str(index_item)
            if i in entity_item_dict.keys():
                f.write(i+" "+str(index_item)+" "+entity_item_dict[i]+'\n')

    with open('./'+data_name+'/entity_list.txt', 'w') as f:
        entity_1_list_ = list(set(entity_1_list))
        entity_2_list_ = list(set(entity_2_list))
        f.write("org_id remap_id\n")
        for index_item, i in enumerate(item_list_):
            if i in entity_item_dict.keys():
                entity_index_dict[entity_item_dict[i]] = str(index_item)
                f.write("e"+entity_item_dict[i]+" "+str(index_item)+'\n')
        for index_entity, e in enumerate(entity_1_list_):
            if e in entity_index_dict.keys():
                continue
            else:
                entity_index_dict[e] = str(index_entity+len(item_list_))
                f.write("e"+e+" "+str(index_entity+len(item_list_))+'\n')
        for index_entity, e in enumerate(entity_2_list_):
            if e in entity_index_dict.keys():
                continue
            else:
                entity_index_dict[e] = str(index_entity+len(item_list_))
                f.write("e"+e+" "+str(index_entity+len(item_list_)+len(entity_1_list_))+'\n')

    with open('./'+data_name+'/relation_list.txt', 'w') as f:
        f.write("freebase_id remap_id\n")
        for i in relation_dict.keys():
            relation = ''.join(str(s) for s in relation_dict[i])
            f.write(relation+" "+i+"\n")

    with open('./'+data_name+'/kg_final.txt', 'w') as f:
        for i in range(len(entity_1_list)):
            entity_1 = entity_index_dict[entity_1_list[i]]
            entity_2 = entity_index_dict[entity_2_list[i]]
            f.write( entity_1+" "+relation_list[i]+" "+ entity_2+"\n" )

    with open('./'+data_name+'/train.txt', 'w') as f:
        for i in train_dict.keys():
            f.write(user_index_dict[i]+" "+" ".join([item_index_dict[j] for j in train_dict[i]])+"\n")


    with open('./'+data_name+'/test.txt', 'w') as f:
        for i in test_dict.keys():
            f.write(user_index_dict[i]+" "+" ".join([item_index_dict[j] for j in test_dict[i]])+"\n")

    with open('./'+data_name+'/negative.txt', 'w') as f:
        for i in negative_dict.keys():
            f.write(user_index_dict[i]+" "+" ".join([item_index_dict[j] for j in negative_dict[i]])+"\n")

if __name__ == '__main__':
    data_name = 'ml1m'
    train_dict, test_dict, negative_dict, entity_dict, user_list, item_list, entity_1_list, entity_2_list, relation_dict, relation_list, item_dict = load_data(data_name) # data loader
    gen_kgat(data_name, train_dict, test_dict, negative_dict, entity_dict, user_list, item_list, entity_1_list, entity_2_list, relation_dict, relation_list, item_dict)
