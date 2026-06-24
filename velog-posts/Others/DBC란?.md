<p>최종 프로젝트를 진행하며 DBC를 기준으로 CAN 통신을 짜보기로 해서 DBC 개념과, 현재까지 어떤 구조로 만들어놨는지 정리해보겠습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6636fc26-8f8f-4200-9074-5c8c82d9b347/image.png" /></p>
<hr />
<h2 id="1-dbc란">1. DBC란?</h2>
<p>CAN 버스 위를 실제로 흐르는 데이터는 메시지 ID(숫자) + 데이터 바이트(최대 8개)로 이루어지며, 필드 이름이 없다.</p>
<pre><code class="language-bash">ID = 256, Data = [2C 01 00 00 01 00 00 00]</code></pre>
<p>메세지를 받는 노드에서는 각 비트마다 잘라서 어떻게 해서 어떻게 해석해야할지 정해야하고, 송신 쪽과 수신 쪽이 자르는 규칙이 1 비트라도 다르면 값을 잘못 읽는다.</p>
<p>따라서 DBC를 통해 분할 규칙을 정의하여 텍스트 파일로 만들어둔다.</p>
<blockquote>
<p>메세지마다 ID, 길이, 송신 노드, 그리고 각 데이터 칸(신호)의 시작 비트, 길이, 스케일, 단위, 수신노드 등 모든 정보를 적어둔다.</p>
</blockquote>
<p>모든 노드가 이 파일을 기준으로 인코딩/디코딩 코드를 만들기 때문에, 송수신이 같은 방식으로 바이트를 나눈다.</p>
<hr />
<h2 id="2-vector-candb">2. Vector CANdb++</h2>
<p>이번 프로젝트에서 Vector CANdb++ 툴을 이용하여 DBC를 작성하기로 했다.</p>
<ul>
<li>노드 목록(<code>BU_</code>) : 버스에 존재하는 노드<ul>
<li>HMI_Controller</li>
<li>Central_Supervisor</li>
<li>Front_Zone_ECU</li>
<li>Rear_Zone_ECU</li>
<li>Drive_ECU</li>
</ul>
</li>
<li>메시지(<code>BO_</code>)<pre><code class="language-bash">BO_ 256 Drive_Cmd: 8 Central_Supervisor
   │     │       │       └ 송신 노드
   │     │       └ 길이 8바이트
   │     └ 이름
   └ ID 256(0x100). 값이 작을수록 우선순위 높음</code></pre>
</li>
<li>신호(<code>SG_</code>) : 메시지 안의 한 칸<pre><code class="language-bash">SG_ Target_Velocity : 0|16@1+ (0.1,0) [0|300] &quot;RPM&quot; Drive_ECU
        │             │  │      │       │      │      └ 수신 노드
        │             │  │      │       │      └ 단위
        │             │  │      │       └ 값 범위
        │             │  │      └ 스케일·오프셋: 버스값 ×0.1 = 실제 RPM
        │             │  └ @1=인텔 바이트오더, +=부호없음
        │             └ 시작 0비트, 길이 16비트
        └ 신호 이름</code></pre>
</li>
</ul>
<p>Vector CANdb++로 작성한 <code>.dbc</code> 파일을 cantools에 넣으면 C코드(<code>.c</code>/<code>.h</code>)가 자동 생성된다.</p>
<p>메세지마다 <code>_pack()</code>, <code>_unpack()</code> 함수가 들어있다.</p>
<ul>
<li><code>_pack()</code> : 구조체 -&gt; 바이트</li>
<li><code>_unpack()</code> : 바이트 -&gt; 구조체</li>
</ul>
<p>각 노드는 헤더를 include하고, 함수를 호출하여 사용하면 된다. </p>
<p>기존에 프로젝트 할 때는 각 비트마다 어떤 데이터일지를 배열 메모리마다 코딩해줘야 했지만, <code>.dbc</code> 파일 하나만 있으면 단일 인터페이스로 정의할 수 있다!</p>