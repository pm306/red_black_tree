from bottle import Bottle, request, static_file, template
from graphviz import Digraph
from rbt.base_tree import ThreadSafeRedBlackTree, RED, BLACK
from copy import deepcopy

app = Bottle()
ts_rbt = ThreadSafeRedBlackTree()

# 履歴を保存するスタック
history_stack = []


def save_to_history(tree):
    history_stack.append(deepcopy(tree))


def get_svg_path():
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
    dot.render(filename='static/svg/rb_tree', format='svg')
    return '/static/svg/rb_tree.svg'  # SVGファイルのパスを返す


@app.route('/')
def index():
    svg_path = get_svg_path()
    return template('index_template', svg_path=svg_path)


@app.route('/update_tree', method='POST')
def update_tree():
    action = request.forms.get('action')
    key = request.forms.get('key')
    if key.isdigit():
        key = int(key)
        # 状態を保存
        save_to_history(ts_rbt)
        if action == 'insert':
            ts_rbt.insert(key)
        elif action == 'delete':
            ts_rbt.delete(key)
    svg_path = get_svg_path()
    return svg_path


@app.route('/undo', method='POST')
def undo():
    global ts_rbt
    if history_stack:
        ts_rbt = history_stack.pop()  # 最後の状態を取り出す
    svg_path = get_svg_path()
    return svg_path


@app.route('/reset_tree', method='POST')
def reset_tree():
    global ts_rbt  # グローバル変数ts_rbtにアクセス
    ts_rbt = ThreadSafeRedBlackTree()  # 新しい空の赤黒木を作成
    svg_path = get_svg_path()  # 新しいSVGファイルのパスを取得
    return svg_path


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')  # Bottleが静的ファイルを提供できるようにする
