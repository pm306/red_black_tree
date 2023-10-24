<!DOCTYPE html>
<html>
<head>
    <script>
        function setRandomNumber() {
            const randomNumber = Math.floor(Math.random() * 100) + 1;
            document.getElementById('key').value = randomNumber;
        }

        async function updateTree(action) {
            const key = document.getElementById('key').value;
            if (isNaN(key)) {
                alert("Invalid input. Please enter a valid number.");
                return;
            }
            const response = await fetch('/update_tree', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `action=${action}&key=${key}`
            });
            const svg = await response.text();
            document.getElementById('tree').innerHTML = svg;
            if (action === 'insert') {
                setRandomNumber();  // Insertアクションの後に新しいランダムな数字をセット
            }
        }

        async function resetTree() {
            const response = await fetch('/reset_tree', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            const svg = await response.text();
            document.getElementById('tree').innerHTML = svg;
        }

        async function undoAction() {
            const response = await fetch('/undo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            const svg = await response.text();
            document.getElementById('tree').innerHTML = svg;
        }

        window.onload = setRandomNumber;  // ページがロードされたときにランダムな数字をセット
    </script>
</head>
<body>
    <input type="text" id="key" placeholder="Enter a number" required>
    <button onclick="updateTree('insert')">Insert</button>
    <button onclick="undoAction()">1つ前に戻る</button>
    <button onclick="updateTree('delete')">Delete</button>
    <button onclick="resetTree()">Reset</button>
    <div><img id="tree" src="{{svg_path}}" alt="Red-Black Tree Visualization"></div>
</body>
</html>
