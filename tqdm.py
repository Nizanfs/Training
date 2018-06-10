import collections
import time
import copy


class Tqdm(collections.Iterator):
    """
    Tqdm class will receive a given iterator and will wrap and analyze it's execution with aditional metadata such as
    running time and progress status
    """
    def __init__(self, func):
        original_iter = iter(func)
        self.iter = original_iter
        self.index = 0

    def __iter__(self):
        copied_iter = copy.copy(self.iter)
        self.iter_length = len(list(copied_iter))
        self.start_time = time.time()
        return self

    def __next__(self):
        next_val = next(self.iter)

        self.index += 1
        output = ''
        output += f'Running iteration number {self.index}, '
        elapsed_seconds = time.time() - self.start_time
        output += f'Elapsed time: {elapsed_seconds:10.4} seconds, '

        iterations_per_second = self.index / elapsed_seconds
        output += f'Iterations per second: {iterations_per_second:10.4}, '

        output += self._print_progress()

        print(f'\r{output}', flush=True, end='')

        return next_val

    def _print_progress(self):
        output = '['
        for index in range(self.iter_length):
            value = '#' if index < self.index else '.'
            output += value
        output += '], '
        percentage = (self.index / self.iter_length) * 100
        output += f'Completed Percentage: {percentage}%, '
        return output


if __name__ == '__main__':
    for i in Tqdm(range(10)):
        time.sleep(1)
        # print(i)
