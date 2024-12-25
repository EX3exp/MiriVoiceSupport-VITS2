import gradio as gr
import torch
from torch import nn
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np
from pathlib import Path
import subprocess
import zipfile
import os
import librosa
import soundfile as sf
import utils
import torch.multiprocessing as mp

MODEL_URLS = {
    "Miri": "https://github.com/EX3exp/MiriVoiceSupport-VITS2/releases/latest/download/Base_Miri.zip",
    "Rivo": "https://github.com/EX3exp/MiriVoiceSupport-VITS2/releases/latest/download/Base_Rivo.zip"
}
def setup_workspace():
    # 필요한 디렉토리 생성
    directories = [
        "voicer",
        "checkpoints",
        "train",
        "train/dataset",
        "train/logs",
        "train/logs/train",
        "train/logs/val",
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # monotonic_align 설치
    try:
        subprocess.run(
            ["python", "setup.py", "build_ext", "--inplace"],
            cwd="monotonic_align",
            check=True
        )
        return "작업 공간 설정 완료!"
    except subprocess.CalledProcessError as e:
        return f"monotonic_align 설치 중 오류 발생: {str(e)}"
    except Exception as e:
        return f"예기치 않은 오류 발생: {str(e)}"

def download_model(model, progress=gr.Progress()):
    progress(0, desc="다운로드 준비 중...")
    cmd = f"aria2c -x 16 -s 16 {MODEL_URLS[model]} -d models/"

    process = subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    while True:
        line = process.stderr.readline()
        if not line:
            break
        if "%" in line:
            try:
                percent = float(line.split("%")[0].split()[-1])
                progress(percent/100)
            except:
                continue

    # 다운로드 완료 후 압축 해제
    progress(0.95, desc="압축 해제 중...")
    zip_path = f"models/Base_{model}.zip"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('checkpoints')

    # 압축 파일 삭제
    os.remove(zip_path)

    progress(1.0, desc="완료")
    return f"{model} 다운로드 및 압축 해제 완료!"

def unzip_dataset(file):
    if file is None:
        return "데이터셋 파일을 선택해주세요."

    try:
        # 압축 해제 진행
        with zipfile.ZipFile(file.name, 'r') as zip_ref:
            # train/dataset 디렉토리에 압축 해제
            zip_ref.extractall('train')

        # 압축 파일 정리
        os.remove(file.name)

        return "데이터셋 압축 해제 완료!"

    except Exception as e:
        return f"오류 발생: {str(e)}"

def process_folder(folder_path, folder_name, progress=gr.Progress()):
    wav_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    total = len(wav_files)

    progress(0, desc=f"[{folder_name}] {total}개 파일 44100Hz로 다운샘플링 중...")

    for i, filename in enumerate(wav_files):
        file_path = os.path.join(folder_path, filename)

        y, sr = librosa.load(file_path, sr=None)
        y = librosa.util.normalize(y)
        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=44100)

        output_file_path = os.path.join(folder_path, filename)
        sf.write(output_file_path, y_resampled, 44100)

        progress((i + 1) / total)

    return f"{folder_name} 처리 완료"

def preprocess_audio(progress=gr.Progress()):
    folder_tr_path = 'train/train'
    folder_vl_path = 'train/validation'

    train_result = process_folder(folder_tr_path, "학습 데이터셋", progress)
    valid_result = process_folder(folder_vl_path, "검증 데이터셋", progress)

    return f"{train_result}\n{valid_result}"

def start_training():
    import train

    if not torch.cuda.is_available():
        return "CPU 학습은 지원하지 않습니다. GPU가 필요합니다."

    try:
        # 환경 변수 설정
        os.environ["MASTER_ADDR"] = "localhost"
        os.environ["MASTER_PORT"] = "6060"

        # 하이퍼파라미터 로드
        hps = utils.get_hparams_from_file(os.path.join('configs', config_path))

        # 학습 시작
        mp.spawn(train.run, nprocs=torch.cuda.device_count(),
                args=(torch.cuda.device_count(), hps))

        return "학습이 시작되었습니다."

    except Exception as e:
        return f"학습 중 오류 발생: {str(e)}"

def create_training_interface():
    with gr.Blocks() as training_app:
        gr.Markdown("# VITS2 모델 학습 인터페이스")
        with gr.Tab("Training"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("## 파인튜닝 모델")
                    gr.Markdown("### 모델 선택")
                    model_name = gr.Dropdown(label="모델 선택", choices=["Miri", "Rivo"])
                    btn_model_ready = gr.Button("모델 준비")

                    btn_model_ready.click(
                        fn=download_model,
                        inputs=[model_name],
                        outputs=[gr.Text(label="상태")]
                    )
                with gr.Column():
                    gr.Markdown("## 데이터셋 준비")
                    gr.Markdown("### 데이터셋 선택")
                    dataset_file = gr.File(label="데이터셋 업로드 (.zip)", file_types=[".zip"])
                    btn_dataset_ready = gr.Button("데이터셋 압축 해제")

                    btn_dataset_ready.click(
                        fn=unzip_dataset,
                        inputs=[dataset_file],
                        outputs=[gr.Text(label="상태")]
                    )

                    btn_preprocess_audio = gr.Button("데이터셋 전처리")
                    btn_preprocess_audio.click(
                        fn=preprocess_audio,
                        inputs=[],
                        outputs=[gr.Text(label="상태")]
                    )
                with gr.Column():
                    gr.Markdown("## 학습 시작")
                    gr.Markdown("### 학습 설정")

                    config_path = gr.Dropdown(label="config 파일", choices=os.listdir('configs'), interactive=True)

                    # CUDA 사용 가능 여부 확인
                    cuda_available = gr.Text(label="CUDA 상태", value="CUDA " + ("사용 가능" if torch.cuda.is_available() else "사용 불가"))

                    # GPU 개수 표시
                    n_gpus = gr.Number(label="사용 가능한 GPU 수", value=torch.cuda.device_count())

                    # 학습 시작 버튼
                    btn_train = gr.Button("학습 시작")

                    btn_train.click(
                        fn=start_training,
                        inputs=[],
                        outputs=[gr.Text(label="상태")]
                    )

                    gr.Markdown("## 텐서보드")
                    gr.Markdown("### 학습 모니터링")
                    btn_tensorboard = gr.Button("텐서보드 열기")

                    def launch_tensorboard():
                        try:
                            subprocess.Popen(["tensorboard", "--logdir=train/logs", "--port=6006"])
                            return "텐서보드가 시작되었습니다. http://localhost:6006 에서 확인하세요."
                        except Exception as e:
                            return f"텐서보드 실행 중 오류 발생: {str(e)}"

                    btn_tensorboard.click(
                        fn=launch_tensorboard,
                        inputs=[],
                        outputs=[gr.Text(label="상태")]
                    )

    return training_app

# 인터페이스 실행
if __name__ == "__main__":
    print(setup_workspace())
    app = create_training_interface()
    app.launch()
