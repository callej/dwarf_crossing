

def fibonacci_gen(num):
    if num > 0:
        yield 1
    if num > 1:
        yield 1
    previous = [1, 1]
    count = 2
    while count < num:
        yield sum(previous)
        previous = [previous[1], sum(previous)]
        count += 1


def fib_n(n):
    return None if n < 1 else 1 if n < 3 else fib_n(n-2) + fib_n(n-1)


def main():
    print(f'This program lists Fibonacci numbers')
    num = int(input(f'How many Fibonacci numbers do you want to see? '))
    for fib in fibonacci_gen(num):
        print(fib)

    print([f for f in fibonacci_gen(num)][-1])

    n = int(input(f'Which Fibonacci number do you want to know? '))
    print(fib_n(n))


if __name__ == '__main__':
    main()
