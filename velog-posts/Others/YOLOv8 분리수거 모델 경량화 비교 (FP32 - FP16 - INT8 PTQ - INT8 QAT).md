<p>이력서, 자소서, 포폴 등 작성하고 시험 준비, 경진대회 준비하면서 수업 정리할 시간이 계속 없었네요. 시간 순서대로 쓰고싶었으나 오늘 내용은 오늘 정리하는게 맞을거같아서 써야할 글이 산더미지만 오늘 수업내용 먼저 정리해보겠습니다.</p>
<hr />
<blockquote>
<p>🔗 <a href="https://github.com/kyoung-mo/yolov8-recycle-quantization">kyoung-mo / yolov8-recycle-quantization</a></p>
</blockquote>
<p>수업시간에 엣지 환경에 AI 모델을 올리는 실습을 진행했습니다. 주제는 자유롭게 정할 수 있었고 시간은 10시부터 20시까지 진행하였습니다.</p>
<p><a href="https://universe.roboflow.com/final-kuqrl/recycle-0mpfl">Roboflow</a>에서 Dataset을 구하기 위해 흔하고 뻔한 주제가 좋다고 생각했고, 분리수거 쪽으로 정했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/902b7bc0-e9ba-4417-849a-027ed50dd325/image.png" /></p>
<hr />
<h2 id="데이터셋">데이터셋</h2>
<ul>
<li><strong>출처</strong>: Roboflow Universe - recycle-0mpfl</li>
<li><strong>클래스 (5개)</strong>: <code>can</code>, <code>glass</code>, <code>null</code>, <code>paperpack</code>, <code>plastic</code></li>
<li><strong>구성</strong>: train 2,768장 / valid 791장 / test 395장</li>
</ul>
<p><code>best.pt</code> 가중치 파일을 만들고, <code>.tflite</code>로 바로 변환하면 오류가 나는 경우가 많아서 아래 과정을 통해 변환했습니다.</p>
<pre><code>.pt → .onnx → .tflite</code></pre><hr />
<h2 id="진행-배경">진행 배경</h2>
<p>원래 팀 단위로 하기로 했었는데, 이력서·자소서 1차 제출 시기가 다가와서 저희 조 6명 중 조퇴가 꽤 많은 상태로 진행했습니다.</p>
<p>FP32, FP16, INT8-PTQ, INT8-QAT로 모델 변환 후 컴퓨터와 라즈베리파이 환경에서 각각 측정 가능한 성능 지표를 정리하는 게 팀 목표였습니다. 저는 라즈베리파이 환경에서 사용할 성능 평가 코드를 맡았고, 모델 변환을 팀원들이 진행하고 있었으나 점심 이후 다들 사라져서 모델 변환부터 다시 진행했습니다.</p>
<p><code>.pt</code> 파일까지는 팀원이 만들어주고 갔고, FP32/FP16/PTQ는 해당 파일 기반으로 변환을 진행했습니다. QAT는 fine-tuning을 포함한 별도 과정이 필요해 처음부터 진행했습니다.</p>
<hr />
<h2 id="모델-변환-흐름">모델 변환 흐름</h2>
<pre><code>best.pt (YOLOv8n FP32)
├── → ONNX → TFLite FP32
├── → ONNX → TFLite FP16
├── → ONNX → TFLite INT8 (PTQ, 캘리브레이션: valid 791장)
└── QAT fine-tuning (5 epoch) → ONNX → TFLite INT8 (QAT)</code></pre><hr />
<h2 id="실험-환경">실험 환경</h2>
<table>
<thead>
<tr>
<th>구분</th>
<th>사양</th>
</tr>
</thead>
<tbody><tr>
<td>학습 PC</td>
<td>Python 3.11.15 / PyTorch 2.5.1+CUDA / NVIDIA RTX 4060</td>
</tr>
<tr>
<td>경량화 변환</td>
<td>Ultralytics 8.4.51 / TensorFlow 2.19.0</td>
</tr>
<tr>
<td>엣지 디바이스</td>
<td>Raspberry Pi 5 / Debian GNU/Linux 13 (trixie) / Python 3.13.5</td>
</tr>
</tbody></table>
<hr />
<h2 id="컴퓨터-환경-성능-평가">컴퓨터 환경 성능 평가</h2>
<p>베이스 모델인 FP32와, FP16, 양자화를 거친 INT8(PTQ), INT8(QAT)의 모델 성능 지표를 비교했습니다.</p>
<h3 id="step-1-결과-json-로드">STEP 1. 결과 JSON 로드</h3>
<pre><code class="language-python">import json, os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

MODEL_ORDER = [&quot;FP32&quot;, &quot;FP16&quot;, &quot;INT8-PTQ&quot;, &quot;INT8-QAT&quot;]
COLOR_MAP = {
    &quot;FP32&quot;:     &quot;#4C72B0&quot;,
    &quot;FP16&quot;:     &quot;#55A868&quot;,
    &quot;INT8-PTQ&quot;: &quot;#C44E52&quot;,
    &quot;INT8-QAT&quot;: &quot;#8172B2&quot;,
}

records = []
for tag in MODEL_ORDER:
    path = f&quot;outputs/{tag}_summary.json&quot;
    if os.path.exists(path):
        with open(path) as f:
            records.append(json.load(f))
        print(f&quot;✅ {tag} 로드&quot;)
    else:
        print(f&quot;❌ {tag} 없음&quot;)

df = pd.DataFrame(records).set_index(&quot;model_tag&quot;)
print(&quot;\n&quot;, df.to_string())</code></pre>
<pre><code>✅ FP32 로드
✅ FP16 로드
✅ INT8-PTQ 로드
✅ INT8-QAT 로드

           size_mb  mAP@50  mAP@50-95  Precision  Recall  F1
model_tag
FP32        11.714  0.9904     0.9833     0.9879  0.9832  0.9855
FP16         5.898  0.9904     0.9827     0.9861  0.9840  0.9851
INT8-PTQ     3.195  0.9881     0.9807     0.9844  0.9853  0.9848
INT8-QAT     3.195  0.9728     0.9543     0.9653  0.9351  0.9500</code></pre><h3 id="step-2-정확도-지표-비교">STEP 2. 정확도 지표 비교</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0685445f-a3e3-4906-b46f-ed6dce692a58/image.png" /></p>
<p>4개 모델의 mAP@50, mAP@50-95, Precision, Recall, F1을 바 차트로 비교했습니다.</p>
<p>FP32와 FP16은 거의 동일한 수준이며, INT8-PTQ도 소폭 하락에 그쳤습니다. INT8-QAT는 fine-tuning epoch이 짧아 다소 낮게 나왔습니다.</p>
<h3 id="step-3-모델-크기-비교">STEP 3. 모델 크기 비교</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/310b30ad-bb71-4e3c-b377-a53c6357482e/image.png" /></p>
<table>
<thead>
<tr>
<th>모델</th>
<th>크기 (MB)</th>
<th>FP32 대비</th>
</tr>
</thead>
<tbody><tr>
<td>FP32</td>
<td>11.714</td>
<td>×1.000</td>
</tr>
<tr>
<td>FP16</td>
<td>5.898</td>
<td>×0.504</td>
</tr>
<tr>
<td>INT8-PTQ</td>
<td>3.195</td>
<td>×0.273</td>
</tr>
<tr>
<td>INT8-QAT</td>
<td>3.195</td>
<td>×0.273</td>
</tr>
</tbody></table>
<p>INT8 계열은 FP32 대비 약 1/4 수준으로 줄었습니다.</p>
<h3 id="step-4-map-vs-모델-크기-트레이드오프">STEP 4. mAP vs 모델 크기 트레이드오프</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5c1bd8ed-f22d-41b6-95e7-36e62425dba2/image.png" /></p>
<p>모델 크기가 줄수록 mAP가 소폭 하락하는 트레이드오프 관계를 확인할 수 있었습니다. FP16은 크기가 절반이지만 mAP는 FP32와 동일하게 유지됐습니다.</p>
<h3 id="step-5-종합-요약">STEP 5. 종합 요약</h3>
<pre><code>           size_mb  mAP@50  mAP@50-95  Precision  Recall    F1  size_ratio
model_tag
FP32        11.714  0.9904     0.9833     0.9879  0.9832  0.9855       1.000
FP16         5.898  0.9904     0.9827     0.9861  0.9840  0.9851       0.504
INT8-PTQ     3.195  0.9881     0.9807     0.9844  0.9853  0.9848       0.273
INT8-QAT     3.195  0.9728     0.9543     0.9653  0.9351  0.9500       0.273</code></pre><hr />
<h2 id="raspberry-pi-5-벤치마크">Raspberry Pi 5 벤치마크</h2>
<h3 id="모델-전송">모델 전송</h3>
<pre><code class="language-bash">scp C:\tmp\best_float32.tflite pi@10.10.16.211:~/py_project/
scp C:\tmp\best_float16.tflite pi@10.10.16.211:~/py_project/
scp C:\tmp\best_int8_ptq.tflite pi@10.10.16.211:~/py_project/
scp &quot;C:\Users\...\best_saved_model\best_int8.tflite&quot; pi@10.10.16.211:~/py_project/best_int8_qat.tflite</code></pre>
<h3 id="실행-방법">실행 방법</h3>
<pre><code class="language-bash">source recycle/bin/activate
python rpi_inference.py --fp32
python rpi_inference.py --fp16
python rpi_inference.py --ptq
python rpi_inference.py --qat</code></pre>
<p>test 이미지 395장을 전부 추론하고, FPS / 추론시간 / CPU 사용률 / 메모리를 측정했습니다.</p>
<h3 id="rpi-벤치마크-결과">RPi 벤치마크 결과</h3>
<p><strong>1. FP32</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/77bdb54c-cbee-4812-906d-71fb49f912c3/image.png" /></p>
<p><strong>2. FP16</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d806dfdf-ce11-4a61-96e4-d84be09ac08e/image.png" /></p>
<p><strong>3. PTQ(INT8)</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e120b766-f249-4d8a-b909-ad760911f1ea/image.png" /></p>
<p><strong>4. QAT(INT8)</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f8e6721d-ce1e-4f60-8797-aa37c41abb51/image.png" /></p>
<table>
<thead>
<tr>
<th>모델</th>
<th>평균 FPS</th>
<th>평균 추론시간 (ms)</th>
<th>평균 CPU (%)</th>
<th>평균 메모리 (MB)</th>
</tr>
</thead>
<tbody><tr>
<td>FP32</td>
<td>8.58</td>
<td>116.59</td>
<td>93.1</td>
<td>267.2</td>
</tr>
<tr>
<td>FP16</td>
<td>8.49</td>
<td>117.80</td>
<td>93.3</td>
<td>261.7</td>
</tr>
<tr>
<td>INT8-PTQ</td>
<td>11.00</td>
<td>90.88</td>
<td>86.9</td>
<td>238.9</td>
</tr>
<tr>
<td>INT8-QAT</td>
<td>10.94</td>
<td>91.43</td>
<td>86.5</td>
<td>238.9</td>
</tr>
</tbody></table>
<hr />
<h2 id="결론">결론</h2>
<p><strong>FP32 vs FP16</strong>
모델 크기는 약 절반으로 줄었지만, RPi에서 FPS와 추론시간은 거의 동일했습니다. RPi는 ARM CPU 기반이라 FP16 연산을 하드웨어 수준에서 가속하지 못하고 FP32로 fallback되어 실행되기 때문입니다.</p>
<p><strong>INT8 (PTQ / QAT)</strong>
FP32 대비 모델 크기가 약 1/4로 줄었고, 추론 속도는 약 28% 향상됐습니다. CPU 사용률과 메모리도 감소했습니다.</p>
<p><strong>PTQ vs QAT</strong>
QAT가 PTQ보다 정확도가 높을 것이라 예상했지만, 이번 실험에서는 PTQ가 오히려 더 좋은 결과가 나왔습니다.</p>
<p>예상되는 이유는 세 가지입니다.</p>
<ol>
<li><strong>원래 모델 성능이 충분히 높았음</strong> — 베이스 mAP@50이 0.99 수준이라 PTQ 변환 후에도 정확도 손실이 거의 없었습니다.</li>
<li><strong>QAT fine-tuning이 5 epoch으로 짧았음</strong> — 일반적으로 원래 학습의 10~20% 수준의 재학습이 필요한데, 시간 제약으로 부족했습니다.</li>
<li><strong>데이터셋이 비교적 단순함</strong> — 5개 클래스가 시각적으로 명확히 구분돼 양자화 오차의 영향이 작았습니다.</li>
</ol>
<p>이번 비교를 통해 <strong>베이스 모델의 품질이 충분히 높으면 PTQ만으로도 QAT 수준의 성능을 달성할 수 있으며, 재학습 비용 없이 동일한 경량화 효과를 얻을 수 있다</strong>는 것을 확인했습니다.</p>