"""
>>> from todoist import TodoistAPI
>>> with open("api_token.txt") as f:
>>>    token = f.read()

>>> api = TodoistAPI(token=token)
>>> api.sync()

# Add new project
>>> proj = api.projects.add("test")
>>> api.commit()

# Add new item
>>> task1 = api.items.add("test item", project_id=proj['id'])
>>> api.commit()

# Updating due time

>>> task1.update(content='NewTask1', due={'string': 'tomorrow at 10:00'})

# Adding and deleting items
>>> task1.complete()
>>> task2 = api.items.add("test item", project_id=proj['id'])
>>> task2.delete()


>>> project = api.projects.get_by_id(128501815)
>>> project.update(name='foo')
>>> api.commit()

>>> section = api.sections.add('Section1', project_id=39982)
>>> api.commit()

>>> date = {
>>>    "date": "2016-12-01",
>>>    "timezone": None,
>>>    "string": "every day",
>>>    "lang": "en",
>>>    "is_recurring": True
>>>}

>>> api.quick.add('Task1 @Label1 #Project1 +ExampleUser')

"""