from todoist import TodoistAPI


def main():
    with open("../data/api_token.txt") as f:
        token = f.read()

    api = TodoistAPI(token=token)
    api.sync()

    # Get all projects
    for proj in api.state['projects']:
        print(proj['name'])

    api.quick.add('Aldi Bananas #AutoShoppingList')


if __name__ == '__main__':
    main()
