import collections
import time
import math


class Tqdm(collections.Iterator):
    """
    Tqdm class will receive a given iterator and will wrap and analyze it's execution with aditional metadata such as
    running time and progress status
    """

    def __init__(self, func, length=None):
        self.func = func
        self.index = 0
        self.iter_length = length

    def __iter__(self):
        if hasattr(self.func, '__len__'):
            self.iter_length = len(self.func)

        self.iter = iter(self.func)
        self.start_time = time.time()
        return self

    def __next__(self):
        next_val = next(self.iter)

        self.index += 1
        output = f'Running iteration number {self.index}, '
        elapsed_seconds = time.time() - self.start_time
        output += f'Elapsed time: {elapsed_seconds:10.4} seconds, '

        iterations_per_second = self.index / elapsed_seconds
        output += f'Iterations per second: {iterations_per_second:10.4}, '

        output += self._calculate_progress()

        print(f'\r{output}', flush=True, end='')

        return next_val

    def _calculate_progress(self):
        if self.iter_length is None:
            return ''
        percentage = (self.index / self.iter_length) * 100
        progress_percentage = math.floor(percentage)
        max_progress = self.iter_length
        current_progress = self.index
        if self.iter_length > 100:
            max_progress = 100
            current_progress = math.floor(progress_percentage)

        output = '['
        for index in range(max_progress):
            value = '#' if index < current_progress else '.'
            output += value
        output += '], '

        output += f'Completed Percentage: {percentage}%, '
        return output


if __name__ == '__main__':
    for i in Tqdm(range(200)):
        time.sleep(1)
        # print(i)

    another_list = [1, 2, 3, 4]
    for i in Tqdm(another_list):
        time.sleep(1)
