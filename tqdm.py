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

        print(f'\rRunning iteration number {self.index}, ', end='')
        self.index += 1

        elapsed_seconds = time.time() - self.start_time
        print(f'Elapsed time: {elapsed_seconds:10.4} seconds, ', end='')

        iterations_per_second = self.index / elapsed_seconds
        print(f'Iterations per second: {iterations_per_second:10.4}', end='')

        self._print_progress()

        return next_val

    def _print_progress(self):
        print('[', end='')
        for index in range(self.iter_length):
            value = '#' if index < self.index else '.'
            print(value, end='')
        print('], ', end='')
        percentage = (self.index / self.iter_length) * 100
        print(f'Completed Percentage: {percentage}%, ', end='', flush=True)


if __name__ == '__main__':
    for i in Tqdm(range(10)):
        time.sleep(1)
        # print(i)
