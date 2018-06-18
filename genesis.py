def file_gen(filename):
    file = open(filename, 'r')
    for line in file:
        yield line


def read_words(filename):
    file_gen_wrapper = type('', (object,), {})()

    def init_file_gen():
        file_gen_wrapper.file_gen = file_gen(filename)

    init_file_gen()

    def find_next_match(search_value):
        matched_result = next(file_gen_wrapper.file_gen)
        while not matched_result.startswith(search_value):
            matched_result = next(file_gen_wrapper.file_gen)

        return matched_result

    try:
        val = next(file_gen_wrapper.file_gen)
        while True:
            val = (yield val)
            if val is not None:

                try:
                    init_file_gen()
                    next_val = find_next_match(val)
                    val = next_val
                except StopIteration:
                    init_file_gen()
                    first_letter = val.lower()[0]
                    # Skipping to the next relevant letter.
                    next_letter = chr(ord(first_letter) + 1)
                    val = find_next_match(next_letter)

            else:
                val = next(file_gen_wrapper.file_gen)

    except StopIteration:
        pass


if __name__ == '__main__':
    words = read_words('./words')
    print(next(words))
    print(next(words))
    print(next(words))
    print(words.send('Be'))
    print(next(words))
    print(words.send('asdasdasd'))
    print(next(words))
