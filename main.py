# main.py
import os, cv2, numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from plyer import filechooser            # 跨平台文件/照片选择
from kivy.utils import platform

KV = '''
<Root>:
    orientation: 'vertical'
    padding: 20
    spacing: 10
    Image:
        id: img
        source: root.im_path
        allow_stretch: True
        keep_ratio: True
    Button:
        text: '选照片'
        on_release: root.pick_image()
    Button:
        text: '去水平网格'
        on_release: root.denoise('h')
    Button:
        text: '去垂直网格'
        on_release: root.denoise('v')
'''

class Root(BoxLayout):
    im_path = StringProperty('')

    def __init__(self, **kw):
        super().__init__(**kw)
        Builder.load_string(KV)

    def pick_image(self):
        # iOS 会弹出系统相册/文件 App
        path = filechooser.open_file(title='选一张图片',
                                     filters=[('Image', '*.png;*.jpg;*.jpeg')])
        if path:
            self.im_path = path[0]

    def denoise(self, mode):
        if not self.im_path:
            return
        img = cv2.imread(self.im_path)
        if img is None:
            return
        # 统一调用一个函数，模式 h / v
        out = self._remove_grid(img, mode)
        out_path = os.path.join(App.get_running_app().user_data_dir,
                                'output.jpg')
        cv2.imwrite(out_path, out)
        self.im_path = out_path

    @staticmethod
    def _remove_grid(img, mode):
        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = (gray < 2)        # 黑色网格点
        if mode == 'h':
            # 逐行处理
            for y in range(1, h-1, 2):
                img[y, mask[y]] = ((img[y-1, mask[y]].astype(np.int16) +
                                    img[y+1, mask[y]].astype(np.int16))//2).astype(np.uint8)
                anti = ~mask[y]
                img[y, anti] = np.minimum(img[y-1, anti], img[y+1, anti])
        else:
            # 逐列处理
            for x in range(1, w-1, 2):
                img[mask[:, x], x] = ((img[mask[:, x], x-1].astype(np.int16) +
                                       img[mask[:, x], x+1].astype(np.int16))//2).astype(np.uint8)
                anti = ~mask[:, x]
                img[anti, x] = np.minimum(img[anti, x-1], img[anti, x+1])
        return cv2.medianBlur(img, 3)


class GridRemoveApp(App):
    def build(self):
        return Root()

if __name__ == '__main__':
    GridRemoveApp().run()