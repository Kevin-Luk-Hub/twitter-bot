FILE_NAME = 'last_seen_id.txt'
FILE_NAME_MESSAGE = 'last_id_message.txt'


def retrieve_last_seen_id(file_name):
    file_read = open(file_name, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    file_write = open(file_name, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return


def retrieve_last_message_id(file_name):
    file_read = open(file_name, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id


def store_last_message_id(last_seen_id, file_name):
    file_write = open(file_name, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return
