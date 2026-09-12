import os
from flask import Flask
app = Flask(__name__)

# ... 你的其他代码 ...

if __name__ == '__main__':
    # Render 会自动分配 PORT 环境变量
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)