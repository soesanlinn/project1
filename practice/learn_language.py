import random
jp_char =   ['a','i','u','e','o',
            'ka','ki','ku','ke','ko',
            'sa','shi','su','se','so',
            'ta','chi','tsu','te','to',
            'na','ni','nu','ne','no',
            'ha','hi','fu','he','ho',
            'ma','mi','mu','me','mo',
            'ya','yu','yo',
            'ra','ri','ru','re','ro',
            'wa','wo','n'
            ]
hiragana =  ['あ','い','う','え','お',
            'か','き','く','け','こ',
            'さ','し','す','せ','そ',
            'た','ち','つ','て','と',
            'な','に','ぬ','ね','の',
            'は','ひ','ふ','へ','ほ',
            'ま','み','む','め','も',
            'や','ゆ','よ',
            'ら','り','る','れ','ろ',
            'わ','を','ん',
            ]
katagana =  ['ア','イ','ウ','エ','オ',
            'カ','キ','ク','ケ','コ',
            'サ','シ','ス','セ','ソ',
            'タ','チ','ツ','テ','ト',
            'ナ','ニ','ヌ','ネ','ノ',
            'ハ','ヒ','フ','ヘ','ホ',
            'マ','ミ','ム','メ','モ',
            'ヤ','ユ','ヨ',
            'ラ','リ','ル','レ','ロ',
            'ワ','ヲ','ン',
            ]
used_char = []
def practice(char_list):
    char_count = len(char_list)
    jpcharlist = tuple(char_list)
    index_chosen_char = -1
    while len(used_char) != char_count:
        input('\nPress Enter to generate a character.')
        if index_chosen_char != -1:
            print('Previous answers for ' + chosen_char + ' are "' + hiragana[index_chosen_char] + ' ' + katagana[index_chosen_char] + '".')
        chosen_char = random.choice(char_list)
        index_chosen_char = jpcharlist.index(chosen_char)
        used_char.append(chosen_char)
        char_list.remove(chosen_char)
        print('New character: ' + chosen_char + '. The practiced character list: ')
        print(*used_char, sep= ', ')
    input('\nPress Enter reveal the final answers.')
    print('Previous answers for ' + chosen_char + ' are "' + hiragana[index_chosen_char] + ' ' + katagana[index_chosen_char] + '".')
    print('Congrats! you have finished the exercise.')
practice(jp_char)