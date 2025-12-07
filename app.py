
# main.py

from flask import Flask, render_template, Response, redirect,url_for

import camera

app = Flask(__name__)

@app.route('/')
def index():
    print(f"{len(camera.cameras)=}")
    return render_template('index.html',len=len(camera.cameras))

	# "/" を呼び出したときには、indexが表示される。

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue   # 空なら飛ばす
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
# returnではなくジェネレーターのyieldで逐次出力。
# Generatorとして働くためにgenとの関数名にしている
# Content-Type（送り返すファイルの種類として）multipart/x-mixed-replace を利用。
# HTTP応答によりサーバーが任意のタイミングで複数の文書を返し、紙芝居的にレンダリングを切り替えさせるもの。
# （※以下に解説参照あり）

@app.route('/video/<int:index>')
def video(index):
    return Response(gen(camera.cameras[index]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/cam_restart", methods=["POST"])
def cam_restart():
    print("カメラ更新", flush=True)
    camera.cam_restart()
    print(f"{camera.cameras}", flush=True)
    return redirect(url_for("index"))



if __name__ == '__main__':
    print(camera.cameras)
    app.run(host='0.0.0.0', debug=False)