key_a = [1, 2, 3]
key_b = [1, 2, 3]

m = {key_a: 4}

# Exception has occurred: TypeError
# unhashable type: 'list'

print(m[key_b]) # これはそもそも実行されない
