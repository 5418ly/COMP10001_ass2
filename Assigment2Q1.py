def zbini_attrs(type_id: int) -> tuple:
    '''
    Returns the attribute value of a given ID
    type_id: int
    return -> 
        tuple[hair, color, accessory, social_media]
    '''
    if not isinstance(type_id, int):
        return None
    if type_id not in range(0, 256):
        return None

    return (
        # color repeat with perioud of 256
        # hence is 7th and 8th binary digit on the right
        ['wavy', 'curly', 'beanie', 'cap'][type_id >> 6 & 0b11], 

        # color repeat with perioud of 64
        # hence is 5th and 6th binary digit on the right
        ['red', 'blue', 'yellow', 'green'][type_id >>  4& 0b11], 

        # accessory repeat with perioud of 16
        # hence is 3rd and 4th binary digit on the right
        ['sneakers', 'bowtie', 'sunglasses', 'scarf'][type_id >> 2 & 0b11], 

        # Social media repeat with perioud of 4
        # hence is 2 binary digit on the right
        ['tiktok', 'instagram', 'discord', 'snapchat'][type_id & 0b11]
    )

# def zbini_attrs(type_id):
    # return (['wavy','curly','beanie','cap'][type_id//16//4],['red','blue','yellow','green'][type_id//16%4],['sneakers','bowtie','sunglasses','scarf'][type_id%16%4],['tiktok','instagram','discord','snapchat'][type_id%16//4]) if (isinstance(type_id,int) and type_id in range(0,256)) else None
'''
string = '{'
for i in range(0,256):
    string = string + '{}:{}, '.format(i,zbini_attrs(i))
string = string + '}'
print(string)
'''

