import profile

if __name__ == '__main__':
    with open(r'C:\dev\ChipProduction\scripts\main.py', 'r') as file:
        content = file.read()

    profile.run(content, sort=2)
