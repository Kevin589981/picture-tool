[app]
title = GridRemover
package.name = gridremover
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv
requirements = python3,kivy,opencv-python,plyer
ios.kivy_ios_url = https://github.com/kivy/kivy-ios.git
ios.codesign.allowed = false   # 仅本地 Debug，不签名
[buildozer]
log_level = 2