# ## voir à déplacer dans un autre fichier ?
def get_file_lst(lang, line, file_name, as_string=True):
    """ renvoie une liste de chaîne de caractères séparées par '|' lorsque
    `line` est spécifiée, sinon elle renvoie la liste de toutes les chaînes
    du fichier texte spécifiés dans le répertoire `lang` contenu dans le
    répertoire "game_string", portant le nom `file_name`, `as_string` s'il
    vaut True convertit la liste en un string avec pour séparateur, le saut
    de ligne """
    # voir à enlever partie si non string en commun
    if lang == '/':
        file = open(f'others/game_string/{file_name}.txt', 'r', encoding='utf-8')
    else:
        path = 'others/game_string/{}/{}.txt'.format(lang, file_name)
        file = open(path, 'r', encoding='utf-8')
    file_as_list = list(file)
    file.close()
    try:
        list_element_line = file_as_list[line-1][:-1].split('|')
        if as_string:
            text = ''
            for element in list_element_line:
                text += element
                text += '\n'
            return text[:-1]
        return list_element_line
    except TypeError:
        return file_as_list


def get_str(lang, file_name, line=None):
    """permet d'obtenir la chaîne de caractère voulue spécifiée par la ligne
    `line` dans le fichier `file_name`."""
    file = get_file_lst(lang, None, file_name)
    return file[line-1][:-1]
