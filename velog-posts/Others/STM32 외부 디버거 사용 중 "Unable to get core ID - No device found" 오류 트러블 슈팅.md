<p>최종 프젝중에 front-ecu를 담당하신 팀원분께서 아래 오류로 블루필 보드(STMF103)을 바꿔야할 것 같다고 하셨다.</p>
<p>블루필 보드... 사놓고 한번도 못 쓰다가 이번 프젝에서 써보려한건데 지금까지 프젝하면서 MCU 디버깅을 하며 비슷한 상황을 겪었던 기억이 있어서 한번 보드 받아서 해결해보고자 했습니다.</p>
<blockquote>
<p>처음에 펌웨어는 잘 올라갔으나, 그 뒤로 외부 디버거가 연결되지 않는 문제</p>
</blockquote>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/27ef7bf4-42a9-40a0-b7cf-aa7202377a04/image.png" /></p>
<hr />
<p>보드 사놓고 못 쓰는건 너무 아깝잖아요.</p>
<p>일단 블루필 보드는 내부 ST-Link가 없어서 <strong>외부 ST-Link를 사용</strong>해야합니다.</p>
<p>저 같은 경우에는 센터에서 기본적으로 제공받았던 STMF411RE-NUCLEO Board를 외부 ST-Link로 써본 경험이 있어서 그렇게 진행을 했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5c794abf-0c2b-4c8d-a59d-9689e97e7035/image.png" /></p>
<p>데이터시트와 같이 ST-Link쪽(CN2)의 점퍼캡 두개를 제거해주면 아래쪽 보드와 위쪽 ST-Link 디버거가 분리됩니다.</p>
<p>이후에 CN4라고 써져있는 Pin1번부터 6번을 내부 ST-Link가 없는 보드랑 연결해서 사용하면 됩니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b1563471-b043-4afc-b6bc-ff66473a2e09/image.png" /></p>
<p>블루필 보드의 경우 NRST가 따로 핀으로 안나와있고 버튼으로 있어요. </p>
<p>사진 기준으로 두 개의 버튼이 붙어있는 부분에서 아래쪽이 NRST, 위쪽이 BOOT 버튼입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8a5924be-499d-4344-b56f-6a32557de584/image.png" /></p>
<p>그 외에 CN4 핀과 블루필 보드의 연결은 다음과 같습니다.</p>
<table>
<thead>
<tr>
<th>F411RE CN4 핀</th>
<th>신호</th>
<th>블루필 연결 위치</th>
</tr>
</thead>
<tbody><tr>
<td>Pin 1</td>
<td>VDD_TARGET</td>
<td>4핀 헤더 <code>3V3</code></td>
</tr>
<tr>
<td>Pin 2</td>
<td>SWCLK</td>
<td>4핀 헤더 <code>SWCLK(A14)</code></td>
</tr>
<tr>
<td>Pin 3</td>
<td>GND</td>
<td>4핀 헤더 <code>GND</code></td>
</tr>
<tr>
<td>Pin 4</td>
<td>SWDIO</td>
<td>4핀 헤더 <code>SWDIO(A13)</code></td>
</tr>
<tr>
<td>Pin 5</td>
<td>NRST</td>
<td>옆면 헤더 <code>R</code> (← 4핀 헤더에 없음)</td>
</tr>
<tr>
<td>Pin 6</td>
<td>SWO</td>
<td>사용 안 함</td>
</tr>
</tbody></table>
<blockquote>
<p>컴퓨터 - 외부 ST-Link - 블루필</p>
</blockquote>
<p>위와같이 하드웨어 배선을 해주고, 펌웨어를 올려봅니다.</p>
<ul>
<li><p>오류 1 (보드 연결시 FAIL 보임)</p>
<ul>
<li>The interface firmware FAILED to reset/halt the target MCU
<img alt="" src="https://velog.velcdn.com/images/mommers/post/00f525c9-4b2a-4c44-aef7-2d8410faf014/image.png" /></li>
</ul>
</li>
<li><p>오류 2 (No ST-LINK detected! Please connect ST-LINK and restart the debug session)</p>
<ul>
<li>해결 방법 : CubeIDE 외에 디버깅을 하면서 CubeProgrammer가 점유 했던 문제. 종료하고 해결
<img alt="" src="https://velog.velcdn.com/images/mommers/post/392177b2-6455-4586-8e28-b801e2a3b3ff/image.png" /></li>
</ul>
</li>
<li><p>오류 3 (loaclhost:61234: Connection timed out.)</p>
<ul>
<li>해결 방법 : 아래 사진 참고
<img alt="" src="https://velog.velcdn.com/images/mommers/post/b2b35df0-42cb-45d4-bc46-2e0c464094ae/image.png" /></li>
</ul>
</li>
</ul>
<p>등등 .. 이것저것 만져보면서 많은 오류가 있었습니다.</p>
<hr />
<h3 id="해결-방법">해결 방법</h3>
<p>일단 해결 방법 먼저 말씀 드리면 아래 두 사진 설정 위주로 해주시면 될 것 같습니다.</p>
<ul>
<li><p>1.STM32CubeProgrammer와 연결
<img alt="" src="https://velog.velcdn.com/images/mommers/post/cf129fc8-3b41-400e-9bf8-8921791c712d/image.png" /></p>
</li>
<li><p>2.Full chip erase
<img alt="" src="https://velog.velcdn.com/images/mommers/post/1bec249c-d056-4eba-a922-4593112c54d7/image.png" /></p>
</li>
<li><p>3.CubeMX 설정 -&gt; SYS -&gt; Debug : Serial Wire로 설정
<img alt="" src="https://velog.velcdn.com/images/mommers/post/afaa95e5-12de-4af8-941c-ae511a6724ff/image.png" /></p>
</li>
</ul>
<ul>
<li><p>4.Run Configurations -&gt; 아래 설정 확인
<img alt="" src="https://velog.velcdn.com/images/mommers/post/bbc01a48-a998-4d94-9477-a1bef7320051/image.png" /></p>
</li>
<li><p>5.flash
<img alt="" src="https://velog.velcdn.com/images/mommers/post/5132312e-e920-4ed8-95ae-6559bb21c6e5/image.png" /></p>
</li>
</ul>
<hr />
<h3 id="흐름-정리">흐름 정리</h3>
<p>처음에 펌웨어는 잘 올라갔으나, 그 뒤로 외부 디버거가 연결되지 않는 문제였다.</p>
<p>칩에 펌웨어가 올라가자마자 SWD핀을 디버그 용도에서 떼어내는것이 문제였고,</p>
<p>STM32CubeProgrammer에서 칩을 초기화해주어 다시 외부 디버거랑 연결이 가능한 상태로 만들고,</p>
<p>CubeMX 설정에서는 SWD 핀 2개(SWDIO, SWCLK)를 디버깅 용도로 사용하게 핀 배정 해주고, Code 생성.</p>
<p>이후 펌웨어 올리는 과정을 거쳤습니다.</p>