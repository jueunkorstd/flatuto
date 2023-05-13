# 플라스크, 리퀘스트, 리다이렉트 모듈 임포트
from flask import Flask, request, redirect

app = Flask (__name__)


nextId = 4
# dictioanry list
topics = [
    {'id' : 1, 'title' : 'html', 'body' : 'html is ...'},
    {'id' : 2, 'title' : 'css', 'body' : 'css is ...'},
    {'id' : 3, 'title' : 'javascript', 'body' : 'javascript is ...'},
]


def templete(contents, content, id=None):
    contextUI = '' #id가 있을때만 update를 보여줌
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f''' <!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>     
        </body>
    </html> 
    '''


def getContents():
    #반복문으로 topics 내용을 넣어줌
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</li>'
    return liTags


@app.route('/')
def index():
    return templete(getContents(), '<h2>Welcome</h2>Hello, WEB!')


@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return templete(getContents(), f'<h2>{title}</h2>{body}', id)

#create
@app.route('/create/', methods=['GET', 'POST'])
def create():
    print('request.method', request.method)
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return templete(getContents(), content)
    elif(request.method == 'POST'):
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id' : nextId, 'title' : title, 'body' : body}
        topics.append(newTopic)
        url = '/read/' + str(nextId) + '/'
        nextId = nextId + 1
        return redirect(url)

#update
@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    print('request.method', request.method)
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body" placeholder="body" value="{body}"></textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return templete(getContents(), content)
    elif(request.method == 'POST'):
        global nextId
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/' + str(id) + '/'
        return redirect(url)

#delete
@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')


app.run(port = 5001, debug = True)