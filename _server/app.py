from bottle import Bottle, request
from graphviz import Digraph
from rbt.base_tree import ThreadSafeRedBlackTreeDeletion, RED, BLACK

app = Bottle()
ts_rbt = ThreadSafeRedBlackTreeDeletion()


def get_svg():
    dot = Digraph(comment='The Red-Black Tree')

    def add_nodes_edges(tree, dot=None):
        if tree == ts_rbt.NIL_LEAF:
            return dot

        if dot is None:
            dot = Digraph(comment='The Red-Black Tree')
            dot.node(name=str(tree.key), color='red' if tree.color == RED else 'black')

        for child, position in zip([tree.left, tree.right], ['left', 'right']):
            if child != ts_rbt.NIL_LEAF:
                dot.node(name=str(child.key), color='red' if child.color == RED else 'black')
                dot.edge(str(tree.key), str(child.key), position)
                dot = add_nodes_edges(child, dot)

        return dot

    dot = add_nodes_edges(ts_rbt.root, dot)
    return dot.pipe(format='svg').decode()  # SVGデータをデコード


@app.route('/', method=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.forms.get('action')
        key = request.forms.get('key')
        if key.isdigit():
            key = int(key)
            if action == 'insert':
                ts_rbt.insert(key)
            elif action == 'delete':
                ts_rbt.delete(key)
    svg = get_svg()
    return f'''
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/vue@2"></script>
            <script>
                function setRandomNumber() {{
                    const randomNumber = Math.floor(Math.random() * 100) + 1;  // 1から100までのランダムな数字を生成
                    document.getElementById('key').value = randomNumber;
                }}

                async function updateTree(action) {{
                    const key = document.getElementById('key').value;
                    if (isNaN(key)) {{
                        alert("Invalid input. Please enter a valid number.");
                        return;
                    }}
                    const response = await fetch('/update_tree', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }},
                        body: `action=${{action}}&key=${{key}}`
                    }});
                    const svg = await response.text();
                    document.getElementById('tree').innerHTML = svg;
                    if (action === 'insert') {{
                        setRandomNumber();  // Insertアクションの後に新しいランダムな数字をセット
                    }}
                }}

                window.onload = setRandomNumber;  // ページがロードされたときにランダムな数字をセット
            </script>
        </head>
        <body>
            <input type="text" id="key" placeholder="Enter a number" required>
            <button onclick="updateTree('insert')">Insert</button>
            <button onclick="updateTree('delete')">Delete</button>
            <button onclick="resetTree()">Reset</button>
            <div id="tree">{svg}</div>
        </body>
        </html>
    '''


@app.route('/update_tree', method='POST')
def update_tree():
    action = request.forms.get('action')
    key = request.forms.get('key')
    if key.isdigit():
        key = int(key)
        if action == 'insert':
            ts_rbt.insert(key)
        elif action == 'delete':
            ts_rbt.delete(key)
    svg = get_svg()
    return svg


@app.route('/insert/<key:int>')
def insert_key(key):
    ts_rbt.insert(key)
    return {"message": f"Inserted {key}"}


@app.route('/delete/<key:int>')
def delete_key(key):
    ts_rbt.delete(key)
    return {"message": f"Deleted {key}"}


@app.route('/update_tree', method='POST')
def update_tree():
    action = request.forms.get('action')
    key = request.forms.get('key')
    if key.isdigit():
        key = int(key)
        if action == 'insert':
            ts_rbt.insert(key)
        elif action == 'delete':
            ts_rbt.delete(key)
    return get_svg()


@app.route('/reset_tree', method='POST')
def reset_tree():
    global ts_rbt  # グローバル変数ts_rbtにアクセス
    ts_rbt = ThreadSafeRedBlackTreeDeletion()  # 新しい空の赤黒木を作成
    svg = get_svg()  # 新しいSVGデータを取得
    return svg


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
