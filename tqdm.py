import collections
import time
import copy


class Tqdm(collections.Iterator):

    def __init__(self, func):
        original_iter = iter(func)
        copied_iter = copy.copy(original_iter)
        self.iter = original_iter
        self.iter_length = len(list(copied_iter))
        self.index = 0
        self.start_time = time.time()

    def __iter__(self):
        return self

    def __next__(self):
        next_val = next(self.iter)
        print('-------------------------')
        print(f'Running iteration number {self.index}')
        self.index += 1

        elapsed_seconds = time.time() - self.start_time
        print(f'Elapsed time: {elapsed_seconds:10.4} seconds')

        iterations_per_second = self.index / elapsed_seconds
        print(f'Iterations per second: {iterations_per_second:10.4}')

        self.__print_progress()

        print('-------------------------')

        return next_val

    def __print_progress(self):
        print('[', end='')
        for index in range(self.iter_length):
            value = '#' if index < self.index else '.'
            print(value, end='')
        print(']')
        percentage = (self.index / self.iter_length) * 100
        print(f'Completed Percentage: {percentage}%')


if __name__ == '__main__':
    for i in Tqdm(range(10)):
        # time.sleep(1)
        print(i)
