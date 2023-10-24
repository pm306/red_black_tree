from bottle import Bottle, request, run
from graphviz import Digraph
from rbt.base_tree import ThreadSafeRedBlackTreeDeletion, RED, BLACK
import json
import random

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
    return dot.pipe(format='svg').decode()


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
    new_key = random.randint(1, 100)
    return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Red-Black Tree Visualization</title>
            <script src="https://cdn.jsdelivr.net/npm/vue@2"></script>
            <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
        </head>
        <body>
            <div id="app">
                <input type="text" v-model="key" placeholder="Enter a number" :value="{new_key}" required>
                <button @click="updateTree('insert')">Insert</button>
                <button @click="updateTree('delete')">Delete</button>
                <button @click="resetTree">Reset</button>
                <div v-html="svg"></div>
            </div>
            <script src="app.js"></script>
        </body>
        </html>
    '''


@app.route('/update_tree', method='POST')
def update_tree():
    action = request.forms.get('action')
    key = request.forms.get('key')
    message = ''
    if key.isdigit():
        key = int(key)
        if action == 'insert':
            ts_rbt.insert(key)
            message = f'Inserted {key}'
        elif action == 'delete':
            ts_rbt.delete(key)
            message = f'Deleted {key}'
    svg = get_svg()
    new_key = random.randint(1, 100)
    return json.dumps({'svg': svg, 'message': message, 'new_key': new_key})


@app.route('/reset_tree', method='POST')
def reset_tree():
    global ts_rbt
    ts_rbt = ThreadSafeRedBlackTreeDeletion()
    svg = get_svg()
    return svg


if __name__ == '__main__':
    run(app, host='localhost', port=8080)