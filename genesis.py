def file_gen(filename):
    file = open(filename, 'r')
    for line in file:
        yield line


def read_words(filename):
    gen = file_gen(filename)

    def find_next_match(search_value):
        matched_result = next(gen)
        while not matched_result.startswith(search_value):
            matched_result = next(gen)

        return matched_result

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
                    # Skipping to the next relevant letter.
                    next_letter = chr(ord(first_letter) + 1)
                    val = find_next_match(next_letter)

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
