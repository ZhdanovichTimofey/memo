from src.utils.exceptions import NotValidExtentionException

def get_fileid_and_ext(data):
    '''
    Gets extention from json
    return False if unknown extention
    '''
    if 'text' in data['message']:
        return False, 'txt'
    
    if 'voice' in data['message']:
        _, ext = data['message']['voice']['mime_type'].split('/')
        file_id = data['message']['voice']['file_id']

        if ext == 'mpeg':
            ext = 'mp3'
        
        return file_id, ext
    
    types_ = ['document', 'audio', 'video']

    for type_ in types_:
        if type_ in data['message']:
            ext = data['message'][type_]['file_name'].split('.')[-1]
            file_id = data['message'][type_]['file_id']
            return file_id, ext    

    return False, False

def get_text(data):
    '''
    Gets text. Note that data MUST be from text message 
    '''
    try:
        return data['message']['text']
    except KeyError:
        raise NotValidExtentionException('txt', get_fileid_and_ext(data)[1])
