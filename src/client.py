import requests

urlt = "http://localhost:5000/%s"

def get(endpoint, **params):
    resp = requests.get(urlt % endpoint, params=params)
    assert resp.status_code == 200
    return resp.json()

def post(endpoint, **data):
    resp = requests.post(urlt % endpoint, data=data)
    assert resp.status_code in [201, 204]
    return resp.json()['id']

def delete(endpoint, id):
    resp = requests.delete(urlt % endpoint + '/%d' % id)
    assert resp.status_code == 204

def main():
    testData = {
        'Jeremy': ['Wake', 'Watch', 'Wonder'],
        'Joshua': ['Frameshift', 'Flashforward'],
        'Jeffrey': ['The Terminal Experiment'],
    }
    personIds = []
    bookIds = []
    ownsIds = []

    for personName, titles in testData.items():
        personId = post('person', name=personName)
        personIds.append(personId)

        for title in titles:
            bookId = post('book', title=title, publisher='Sawyer')
            bookIds.append(bookId)
            ownsIds.append(post('person_owns_book', personId=personId, bookId=bookId))

        result = get('findBooksByPersonName', name=personName)

        gotTitles = [r['title'] for r in result]
        assert len(gotTitles) == len(titles)
        for t in titles:
            assert t in gotTitles
        for t in gotTitles:
            assert t in titles

    for ownsId in ownsIds:
        delete('person_owns_book', ownsId)
    for bookId in bookIds:
        delete('book', bookId)
    for personId in personIds:
        delete('person', personId)

if __name__ == '__main__':
    main()
