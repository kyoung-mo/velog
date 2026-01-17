<h2 id="데이터-시트">데이터 시트</h2>
<p><a href="https://cdn.sparkfun.com/assets/f/f/a/5/0/DS-16038.pdf">4x4 Key Module DataSheet.pdf</a></p>
<hr />
<h2 id="기본-정보">기본 정보</h2>
<ul>
<li><strong>구성</strong>: 4행 × 4열 총 16개의 버튼</li>
<li><strong>인터페이스</strong>: 총 8핀</li>
<li><strong>동작 방식</strong>: 매트릭스 구조로 각 버튼이 하나의 행과 열 사이에 위치</li>
</ul>
<h2 id="전기적-특성">전기적 특성</h2>
<ul>
<li><strong>최대 동작 전압</strong>: 24V DC</li>
<li><strong>최대 동작 전류</strong>: 30mA (버튼 1개 기준)</li>
<li><strong>접촉 저항(Contact resistance)</strong>: 100Ω 이하</li>
<li><strong>절연 저항</strong>: 100MΩ 이상 (at 100V DC)</li>
<li><strong>키 수명</strong>: 약 1,000,000번 이상</li>
<li><strong>디바운스 시간</strong>: 5ms 이하 //보안</li>
<li>디바운스 시간이 5ms 이하 라는 뜻은 해당 키패드 모듈의 하드웨어 접점 특성상 버튼을 눌렀을 때 발생하는 '튀는 시간(불안정한 신호)'이 최대 5ms 정도로 짧다는 의미입니다. 쉽게 설명하자면  이 튐의 길이가 최대 5ms 이하라는 뜻이에요. 즉, 5ms만 지나면 안정된 신호가 들어온다는 뜻입니다.</li>
</ul>
<h2 id="기계적-특성">기계적 특성</h2>
<ul>
<li><strong>작동 압력</strong>: 160 ~ 180g</li>
<li><strong>작동 온도 범위</strong>: 0°C ~ 50°C</li>
<li><strong>외형 크기</strong>: 약 69mm × 76mm (막형 타입 기준)</li>
</ul>
<hr />
<h2 id="회로도연결도">회로도,연결도</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e01731e0-06bb-4c81-917d-c86ef8c47cf0/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f648ea51-f412-4862-82d3-fc1c4dedfd1a/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bb5ee07a-fb46-4aca-b09f-6dd59e67de9a/image.png" /></p>
<hr />
<h2 id="4x4-key-모듈-예제">4x4 Key 모듈 예제</h2>
<table>
<thead>
<tr>
<th><strong>아두이노</strong></th>
<th><strong>키패드 모듈</strong></th>
<th><strong>부저</strong></th>
<th><strong>서보모터</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>D2</strong></td>
<td>PIN 1</td>
<td>/</td>
<td>/</td>
</tr>
<tr>
<td><strong>D3</strong></td>
<td>PIN 2</td>
<td>/</td>
<td>/</td>
</tr>
<tr>
<td><strong>D4</strong></td>
<td>PIN 3</td>
<td>/</td>
<td>/</td>
</tr>
<tr>
<td><strong>D5</strong></td>
<td>PIN 4</td>
<td>/</td>
<td>/</td>
</tr>
<tr>
<td><strong>D6</strong></td>
<td>PIN 5</td>
<td>/</td>
<td>/</td>
</tr>
<tr>
<td><strong>D7</strong></td>
<td>PIN 6</td>
<td>/</td>
<td>/</td>
</tr>
<tr>
<td><strong>D8</strong></td>
<td>PIN 7</td>
<td>/</td>
<td>/</td>
</tr>
<tr>
<td><strong>D9</strong></td>
<td>PIN 8</td>
<td>/</td>
<td>/</td>
</tr>
<tr>
<td><strong>D10</strong></td>
<td>/</td>
<td>/</td>
<td>Data Pin</td>
</tr>
<tr>
<td><strong>D12</strong></td>
<td>/</td>
<td>PIN +</td>
<td>/</td>
</tr>
<tr>
<td><strong>GND</strong></td>
<td>/</td>
<td>PIN -</td>
<td>/</td>
</tr>
<tr>
<td><strong>GND</strong></td>
<td>/</td>
<td>/</td>
<td>PIN -</td>
</tr>
<tr>
<td><strong>5V</strong></td>
<td>/</td>
<td>/</td>
<td>PIN +</td>
</tr>
</tbody></table>
<pre><code class="language-c">#include &lt;Arduino.h&gt;

//  핀 배치: 실제 키패드 기준에 맞게 수정
const int colPins[4] = {5, 4, 3, 2};  // C1~C4 → S2, S6, S10, S14
const int rowPins[4] = {6, 7, 8, 9};  // R1~R4 → S1, S5, S9, S13

//  키 매핑은 그대로 사용 가능
char keymap[4][4] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
;                                                                           
unsigned long lastPress = 0;
const int debounceDelay = 200;

void setup() {
  Serial.begin(9600);

  // 열 핀 입력 풀업
  for (int c = 0; c &lt; 4; c++) {
    pinMode(colPins[c], INPUT_PULLUP);
  }

  // 행 핀 출력 HIGH 초기화
  for (int r = 0; r &lt; 4; r++) {
    pinMode(rowPins[r], OUTPUT);
    digitalWrite(rowPins[r], HIGH);
  }
}

void loop() {
  for (int r = 0; r &lt; 4; r++) {
    // 모든 행 HIGH로 초기화
    for (int i = 0; i &lt; 4; i++) {
      digitalWrite(rowPins[i], HIGH);
    }
    digitalWrite(rowPins[r], LOW);  // 현재 행만 LOW로 설정

    // 열 핀 읽기
    for (int c = 0; c &lt; 4; c++) {
      if (digitalRead(colPins[c]) == LOW) {
        if (millis() - lastPress &gt; debounceDelay) {
          Serial.print(&quot;입력된 키: &quot;);
          Serial.println(keymap[r][c]);
          lastPress = millis();
        }
      }
    }
  }
}
</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/37e06462-264f-4c2d-af55-e3e4e75c40da/image.png" /></p>