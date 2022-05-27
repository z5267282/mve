def printer(a, b):
    print(f'first: {a}')
    print(f'second: {b}')

def main():
    x = ['one', 'two']
    printer(*x)

if __name__ == '__main__':
    main()
