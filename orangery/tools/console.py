from __future__ import annotations

from typing import Union

def integer_prompt(low: int, high: int, label: Union[None, str] = None) -> int:
    prompt = 'Enter an integer number between {0} and {1}: '.format(low, high)
    err = 'Input must be an integer number between {0} and {1}.'.format(low, high)

    if label:
        print(label)

    while True:
        try:
            n = int(input(prompt))
            if low <= n <= high:
                return n
            else:
                print(err)
        except ValueError:
            print(err)


def double_prompt(low: float, high: float, label: Union[None, str] = None) -> float:
    prompt = 'Enter a decimal number between {0} and {1}: '.format(low, high)
    err = 'Input must be a decimal number between {0} and {1}.'.format(low, high)
    if label:
        print(label)

    while True:
        try:
            n = float(input(prompt))
            if low <= n <= high:
                return n
            else:
                print(err)
        except ValueError:
            print(err)


def string_prompt(label: Union[None, str] = None) -> str:
    prompt = 'Enter a text string: '
    err = 'String must be at least one character length.'

    if label:
        print(label)

    while True:
        try:
            s = input(prompt)
            if len(s) > 0:
                return s
            else:
                print(err)
        except ValueError:
            print(err)


def choice_prompt(choices: dict, label: Union[None, str] = None) -> str:
    low = 0
    high = low + len(choices) - 1

    prompt = 'Enter a number for choice: '
    err = 'Choice must be between {0} and {1}'.format(low, high)

    if label:
        print(label)

    for i, choice in enumerate(choices):
        print(i, '. ', choice)

    while True:
        try:
            n = int(input(prompt))
            if low <= n <= high:
                return choices[n]
            else:
                print(err)
        except ValueError:
            print(err)
