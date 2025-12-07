
import cv2





class VideoCamera(object):
    def __init__(self,id):
        self.camid=id
        self.video = cv2.VideoCapture(id,cv2.CAP_V4L2)

        self.video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # → CPU激減
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 340)
        self.video.set(cv2.CAP_PROP_FPS, 30)

        
		# Opencvのカメラをセットします。(0)はノートパソコンならば組み込まれているカメラ

    def __del__(self):
        print("デストラクタ")
        if self.video is not None:
            self.video.release()

    def get_frame(self):
        if self.video is not None:
            success, image = self.video.read()
            if not success or image is None:
                return None

            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        
        return None
 

        

cameras=[]


def cam_restart():
    global cameras
    cameras=[]

    for i in range(10):
        camera=VideoCamera(i)
        if camera.video.isOpened():
            print(camera.camid)
            cameras.append(camera)
    print(cameras)

# cam_restart()