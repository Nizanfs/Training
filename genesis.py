def file_gen(filename):
    file = open(filename, 'r')
    for line in file:
        yield line


def read_words(filename):
    gen = file_gen(filename)

    def find_next_match(search_value):
        next_val = next(gen)
        while not next_val.startswith(search_value):
            next_val = next(gen)

        return next_val



    try:
        val = next(gen)
        while True:
            val = (yield val)
            if val is not None:

                try:
                    gen = file_gen(filename)
                    next_val = find_next_match(val)
                    val = next_val
                except StopIteration:
                    gen = file_gen(filename)
                    first_letter = val.lower()[0]
                    val = find_next_match(chr(ord(first_letter) + 1))

            else:
                val = next(gen)

    except StopIteration:
        pass


if __name__ == '__main__':
    words = read_words('../words')
    print(next(words))
    print(next(words))
    print(next(words))
    print(words.send('Be'))
    print(next(words))
    print(words.send('asdasdasd'))
    print(next(words))
