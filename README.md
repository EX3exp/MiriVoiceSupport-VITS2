# VITS2: Improving Quality and Efficiency of Single-Stage Text-to-Speech with Adversarial Learning and Architecture Design
### Jungil Kong, Jihoon Park, Beomjeong Kim, Jeongmin Kim, Dohee Kong, Sangjin Kim 
Unofficial implementation of the [VITS2 paper](https://arxiv.org/abs/2307.16430), sequel to [VITS paper](https://arxiv.org/abs/2106.06103). (thanks to the authors for their work!)

![Alt text](resources/image.png)

Single-stage text-to-speech models have been actively studied recently, and their results have outperformed two-stage pipeline systems. Although the previous single-stage model has made great progress, there is room for improvement in terms of its intermittent unnaturalness, computational efficiency, and strong dependence on phoneme conversion. In this work, we introduce VITS2, a single-stage text-to-speech model that efficiently synthesizes a more natural speech by improving several aspects of the previous work. We propose improved structures and training mechanisms and present that the proposed methods are effective in improving naturalness, similarity of speech characteristics in a multi-speaker model, and efficiency of training and inference. Furthermore, we demonstrate that the strong dependence on phoneme conversion in previous works can be significantly reduced with our method, which allows a fully end-toend single-stage approach.

## Notes
[<img src="https://colab.research.google.com/assets/colab-badge.svg">](https://colab.research.google.com/github/EX3exp/MiriVoiceSupport-VITS2/blob/main/VITS2_MiriVoice_Support.ipynb)
- Supports 44100kHz.
- No Language barrier between models - Uses [almost all IPA Phonemes](https://github.com/AdamSteffanick/ipa-data/blob/master/guid-o-matic/ipa-data/ipa-data.csv) as Input.
## Prerequisites
1. Python >= 3.10
2. Tested on Pytorch version 1.13.1 with Google Colab and LambdaLabs cloud.
3. Clone this repository
4. Install python requirements. Please refer [requirements.txt](requirements.txt)
    1. You may need to install espeak first: `apt-get install espeak`

  
## Special mentions
- [@erogol](https://github.com/erogol) for quick feedback and guidance. (Please check his awesome [CoquiTTS](https://github.com/coqui-ai/TTS) repo).
- [@lexkoro](https://github.com/lexkoro) for discussions and help with the prototype training.
- [@manmay-nakhashi](https://github.com/manmay-nakhashi) for discussions and help with the code.
- [@athenasaurav](https://github.com/athenasaurav) for offering GPU support for training.
- [@w11wo](https://github.com/w11wo) for ONNX support.
- [@Subarasheese](https://github.com/Subarasheese) for Gradio UI.
