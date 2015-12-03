from pictur.sql_model import sql_controller
import random
import string

def generate_comment(max_comment_length):
    result = []
    comment_length = 0
    #next_cache = {}
    #sum_cache = {}
    current_word = '[%'
    while current_word != '%]':
        next_words = None
        total = None
        '''if current_word not in sum_cache:'''
        next_words = sql_controller.get_next_for_word(current_word)
        total = sql_controller.get_total_for_word(current_word)['count']
        '''next_cache[current_word] = next_words
        sum_cache[current_word] = total
        else:
        next_words = next_cache[current_word]
        total = sum_cache[current_word]'''
        
        sum = 0
        target = total * random.random()
        
        next_word = ''
        
        for potential in next_words:
            sum += potential['count']
            if sum > target:
                next_word = potential['next_word']
                break
                
        if next_word is '':
            #something went wrong
            result += ['....']
            break
            
        if next_word != '%]':
            result += [next_word]
        current_word = next_word
        comment_length += 1
        
        if comment_length > max_comment_length:
            result += [' ...']
            break
        
    result = ' '.join(result)
    return result
    
def insert_comment(comment):
    current_word = '[%'
    next_word = ''
    for word in comment.split(' '):
        if len(word) > 254:
            word = word[0:254]
        next_word = word
        sql_controller.increment_chain_count(current_word, next_word)
        current_word = next_word
    next_word = '%]'
    sql_controller.increment_chain_count(current_word, next_word)
    