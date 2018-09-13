#! /bin/python
# 功能： 批量拼接兩個wav格式的語音，在此版本中，在一段語音前後新增了兩端500ms左右的靜音，靜音文件名：./sil.wav
#       生成的文件放置于wav文件夾中，原始語音文件夾必須命名為：wav_original
# 注：因爲主要處理語音識別AISHELL的語料庫，所以語音存放格式是一致的，如下：wav_original\train\wav\A1000\BAC009A1000W0001.wav
# 作者： Chen Jiang
# 日期： 2018-9-12
# 版本：v1.0, 後續：支持脚本傳參
# 已知问题： 如果执行过此脚本，生成了wav文件夹，再次运行此脚本，需要手动删除wav文件夹
#

import wave as we
import numpy as np
import os

# 创建转换后语音存放的路径，如果存在删除再创建 不存在则创建
if not os.path.exists("./wav"):
    os.makedirs("./wav")

# 读取静音wav文件的数据部分，并保存到数组sil_waveData中
sil_wav_filename = './sil.wav'

wav_sil = we.open(sil_wav_filename, 'rb')
sil_n_frames = wav_sil.getnframes()
sil_data = wav_sil.readframes(sil_n_frames)  # 读取音频，字符串格式
sil_waveData = np.fromstring(sil_data, dtype=np.int16)  # 将字符串转化为int
wav_sil.close()

# 循环遍历原始语音，同时在wav下创建对应的路径文件夹
for (root, dirs, files) in os.walk("./wav_original"):
        for file in files:
            abs_file_name = os.path.join(root, file)
            if abs_file_name.endswith(".wav"):  # 查找后缀为.wav的文件
                original_filename = abs_file_name
                wav_original = we.open(original_filename, 'rb')       # 以下获取原始语音的数据部分
                n_frames = wav_original.getnframes()
                strData = wav_original.readframes(n_frames)   # 读取音频，字符串格式
                original_wave_Data = np.fromstring(strData, dtype=np.int16)  # 将字符串转化为int
                wav_original.close()

                outfile = "./wav"+original_filename[14:]  # 创建wav目录下对应的路径文件夹比如：wav\train\wav\A1000\
                if not os.path.exists("./wav"+original_filename[14:][:-21]):
                    os.makedirs("./wav"+original_filename[14:][:-21])
                out_wave = we.open(outfile, 'wb') # 定义存储路径以及文件名

                n_channels = 1
                sample_width = 2
                fs = 16000
                frame_rate = int(fs)
                outData = np.hstack((sil_waveData, original_wave_Data, sil_waveData))    # outData = 兩端拼接了靜音值
                n_frames = len(outData)
                comp_type = "NONE"
                comp_name = "not compressed"
                out_wave.setparams((n_channels, sample_width, frame_rate, n_frames, comp_type, comp_name))      # 设置要生成新的语音的参数

                for v in outData:
                    out_wave.writeframes(v)      # 写入音频数据
                out_wave.close()
                print(abs_file_name + " process finished")

print("All process Done")
