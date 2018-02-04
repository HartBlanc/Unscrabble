with open('dict_2.txt') as f:
    content = f.readlines()
    all_words = [x.strip() for x in content]


length = [(word,len(word)) for word in all_words]
length.sort(key=lambda x:x[1], reverse=True)

print(length[0])

build_dict = [x for x in all_words if len(x)<= 11]
#
# with open('dict_2.txt', 'w') as f:
#     for item in new_dict:
#         f.write("%s\n" % item)
