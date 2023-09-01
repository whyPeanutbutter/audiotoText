import whisper
import threading
import time
import soundfile as sf
import librosa
import os
import subprocess

def handleAudio(audioName, outputFolder):

    # print(audioName + "音频重采样开始!!")
    # data, sample_rate = librosa.load(audioName, sr=None)
    # new_sample_rate = 22050
    # resampled_data = librosa.resample(data, orig_sr=sample_rate, target_sr=new_sample_rate)
    
    # new_audio_name = os.path.basename(audioName)
    # new_audio_name = 'new_' + new_audio_name[:-4] + '.wav'
    # new_audio_path = os.path.join(outputFolder, new_audio_name)
    
    # sf.write(new_audio_path, resampled_data, new_sample_rate)
    # print(new_audio_name + "音频重采样结束!!")
    #  'cpu': 使用CPU来运行Whisper模型。
# 'cuda': 使用GPU来运行模型。这可以利用GPU的并行计算性能来加速Whisper的语音识别。
# 'auto': 自动选择一个可用的硬件设备,会首先查找GPU,如果没有再使用CPU。这是默认设置。
# 'mps': 在Mac上使用Apple的机器学习框架Metal来运行模型。
# Whisper的load_model()函数除了device


    new_audio_path = audioName
    new_audio_name = os.path.basename(audioName)


    vocabulary = ' '.join(["吴小宇","北北",'薛一凡'])
    model = whisper.load_model("small")
    result = model.transcribe(new_audio_path,fp16=False,initial_prompt=vocabulary)
    
    # audio = whisper.load_audio(audioName)
    # audio = whisper.pad_or_trim(audio)
    # mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")
    # options = whisper.DecodingOptions(fp16=False)
    # print(options)
    # result = whisper.decode(model, mel, options)
    # print(result)


    outputName = new_audio_name[:-4] + '.txt'
    output_path = os.path.join(outputFolder, outputName)
    
    with open(output_path, 'a', encoding='utf-8') as f:    # print(result)
        f.write('#################################################################' + '\n')
        for segment in result['segments']:
            start = round(segment['start'], 2)
            end = round(segment['end'], 2)
            text = segment['text']
            formatted_string = f"[{start: >7.2f} ---{end: >7.2f}]      {text}"
            print(formatted_string)
            f.write(formatted_string + '\n')
    # command = f'whisper {new_audio_path} --output_dir audioOutput --threads 3 --fp16 False --model small'
    # print(command)
    # subprocess.run(command.split())


def long_running_task(inputFolder, outputFolder):
    audio_files = [os.path.join(inputFolder, f) for f in os.listdir(inputFolder) if f.endswith('.m4a')]
    print(audio_files)
    for audio_file in audio_files:
        handleAudio(audio_file, outputFolder)

def print_progress():
    elapsed_time = 0
    while True:
        time.sleep(10)
        elapsed_time += 10
        print(f"处理中，已处理{elapsed_time}秒。。。请稍后")

if __name__ == "__main__":
    inputFolder = 'audioInput'
    outputFolder = 'audioOutput'

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    task_thread = threading.Thread(target=long_running_task, args=(inputFolder, outputFolder))
    print("处理开始!!")
    task_thread.start()

    progress_thread = threading.Thread(target=print_progress)
    progress_thread.daemon = True
    progress_thread.start()

    task_thread.join()
    print("任务完成！")
