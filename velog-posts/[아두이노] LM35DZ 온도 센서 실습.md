<ul>
<li><a href="https://www.ti.com/lit/ds/symlink/lm35.pdf">LM35DZ 온도 센서_Data_Sheet</a></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0bbeba4b-2a70-4ede-b9ff-2e8a2020c093/image.png" /></p>
<hr />
<h3 id="description">Description</h3>
<ol>
<li>LM35 시리즈는 Output 전압과 섭씨 온도가 선형적으로 비례하는 집적-회로 온도 장치이다.</li>
<li>LM35는 켈빈(K) 기준으로 보정된 온도 센서와 달리,
섭씨 온도를 얻기 위해 큰 기준 전압을 빼줄 필요가 없다는 장점이 있다.</li>
<li>LM35는 외부 보정이나 미세 조정(trimming) 없이도
실온에서 ±0.25°C,</li>
</ol>
<p>-55°C ~ 150°C 전체 범위에서 ±0.75°C의 일반적인 정확도를 제공한다.
4. 웨이퍼 단계에서 트리밍과 보정을 수행하기 때문에
제조 비용이 절감되어 저렴한 가격이 보장된다.
5. LM35는출력 임피던스가 낮고, 출력이 선형적이며, 내부적으로 정확하게 보정되어 있어 측정 장치나 제어 회로와 연결하기가 매우 쉽다.
6. 이 장치는 단일 전원에서도 사용할 수 있고, ± 전원 방식에서도 사용할 수 있다.
7. LM35는 전원에서 단 60μA만 소비하므로 공기 흐름이 없는 환경에서도 자체 발열이 0.1°C 미만으로 매우 작다.
8. LM35는 -55°C ~ 150°C 범위에서 동작하도록 설계되었으며, LM35C는 -40°C ~ 110°C 범위에서 동작하도록 설계되었다 (특히 -10°C 부근에서 정확도가 더 향상됨).
9. LM35 시리즈는 기밀 금속 TO 트랜지스터 패키지로 제공되며, LM35C, LM35CA, LM35D는 플라스틱 TO-92 트랜지스터 패키지로 제공된다.
10. LM35D는 8핀 SMD 소형 패키지와 플라스틱 TO-220 패키지 형태로도 제공된다.</p>
<hr />
<h3 id="온도-센서-실습">온도 센서 실습</h3>
<pre><code class="language-c">#include &lt;Arduino.h&gt;

float temperature;       // 계산된 온도 값을 저장할 변수 (단위: °C)
int reading;             // 아날로그 값(0~1023)을 저장할 변수
int lm35Pin = A0;        // LM35 센서가 연결된 아날로그 핀 번호 (A0에 연결)

void setup()  
{
    analogReference(INTERNAL);  // 아날로그 기준 전압을 1.1V 내부 기준으로 설정 (더 정밀한 측정 가능)
    delay(10);                  // 내부 기준 전압 안정화 시간
    Serial.begin(9600);         // 시리얼 통신 시작 (전송속도: 9600bps)
}

void loop()  
{
    reading = analogRead(lm35Pin);  // LM35에서 아날로그 값을 읽어옴 (0~1023 범위)

    // 읽은 값을 실제 온도(°C)로 변환
    // 내부 기준 전압 1.1V 사용 시, ADC 분해능: 1.1V / 1024 ≈ 0.00107V (1비트당)
    // LM35는 10mV/°C → 온도 = (ADC값 × 1.1) / 1024 / 0.01 = ADC값 / 9.31
    temperature = reading / 9.31;

    Serial.println(temperature);    // 온도를 시리얼 모니터에 출력
    delay(1000);                    // 1초 간격으로 반복
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/598c1508-7f43-4c35-a756-e23e210df1b4/image.png" /></p>
<ul>
<li>정확한 값이 출력 안됐는데, DataSheet를 봐도 문제를 못 찾은 이유 + 수업 진도 나가기도 해야하니 넘어가기로 했습니다..</li>
</ul>