import os
from moviepy.editor import VideoFileClip

# 定义输入和输出文件夹的路径
input_folder = "videoInput"
output_folder = "videoAudioOutput"

# 指定输出音频的采样率
sample_rate = 22050  # 44100 Hz

# 如果输出文件夹不存在，创建一个
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder):
	if filename.endswith(('.mp4', '.mkv', '.flv', '.avi')):  # 添加你想支持的视频格式
		print(filename)
       # 完整的输入路径
		input_path = os.path.join(input_folder, filename)
        
        # 完整的输出路径
		output_filename = os.path.splitext(filename)[0] + ".mp3"  # 更改文件扩展名为.mp3
		output_path = os.path.join(output_folder, output_filename)
        
        # 读取视频，提取音频
		video = VideoFileClip(input_path)
		audio = video.audio
        
        # 保存音频
		audio.write_audiofile(output_path,fps=sample_rate)

print("音频提取完成！")
