<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5f52a998-52fd-4d1c-a746-4010ab5c55c0/image.png" /></p>
<h2 id="개념">개념</h2>
<ul>
<li><p><strong>풀업 저항(Pull-up Resistor)</strong>: 디지털 회로에서 입력 신호가 <strong>안정적으로 논리 1(HIGH)</strong> 상태를 유지하도록 전원(VCC)에 연결된 저항으로, 외부 신호가 없는 상태에서 입력이 불확실해지는 것을 방지한다.</p>
</li>
<li><p><strong>풀다운 저항(Pull-down Resistor)</strong>: 입력 신호가 <strong>안정적으로 논리 0(LOW)</strong> 상태를 유지하도록 접지(GND)에 연결된 저항으로, 외부 입력이 없을 때 값이 무작위로 변하는 것을 막는 역할을 한다.</p>
</li>
</ul>
<h2 id="사용하는-이유">사용하는 이유</h2>
<ul>
<li>입력 핀이 어떤 값(0 또는 1)으로 정해지지 않고 <strong>불확실한 상태(플로팅, Floating)</strong> 가 되는 것을 방지하는 역할을 한다. 플로팅 상태에서는 노이즈로 인해 입력 값이 예기치 않게 변할 수 있어 회로 동작에 문제가 생길 수 있다..</li>
<li>풀업/풀다운 저항은 <strong>디지털 회로, 마이크로컨트롤러(MCU), 스위치 회로 등</strong>에서 입력의 논리 상태를 명확히 하여 안정적으로 신호를 처리하게 만드는 역할을 한다.</li>
</ul>
<h2 id="동작-원리">동작 원리</h2>
<table>
<thead>
<tr>
<th>종류</th>
<th>저항 연결 위치</th>
<th>입력의 기본 상태</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td>풀업</td>
<td>VCC(전원)와 입력핀 사이</td>
<td>HIGH(1)</td>
<td>신호가 없는 경우에도 입력이 항상 1, 스위치 눌리면 0으로 바뀜</td>
</tr>
<tr>
<td>풀다운</td>
<td>GND(접지)와 입력핀 사이</td>
<td>LOW(0)</td>
<td>신호가 없는 경우에도 입력이 항상 0, 스위치 누르면 1로 바뀜</td>
</tr>
</tbody></table>
<h2 id="실무-예시">실무 예시</h2>
<ul>
<li><strong>스위치 입력 회로</strong>에서 사용:<ul>
<li>스위치가 열렸을 때 입력이 플로팅 되지 않고, 원하는 상태(HIGH/LOW)가 유지됨.</li>
</ul>
</li>
<li><strong>MCU(예: 아두이노)</strong> 입력에서:<ul>
<li>버튼이 눌리지 않은 상태의 값을 명확히 유지하기 위해 풀업 또는 풀다운 저항을 사용함.</li>
</ul>
</li>
</ul>
<h2 id="참고사항">참고사항</h2>
<ul>
<li><strong>노이즈 특성상 풀업 저항이 더 널리 사용</strong>되는 경우가 많으며, 저항값은 일반적으로 10kΩ 정도가 많이 쓰입니다.</li>
<li>저항 없이 연결할 경우 과전류나 회로 오동작(합선 등)이 발생할 수 있으므로, 반드시 저항을 사용해야 합니다.</li>
</ul>
<h2 id="요약">요약</h2>
<ul>
<li><strong>풀업 저항</strong>: 논리 1을, <strong>풀다운 저항</strong>: 논리 0을 기본 상태로 유지</li>
<li>주로 <strong>플로팅 방지</strong>와 <strong>회로의 안정성 확보</strong>에 사용됨</li>
<li>디지털 신호 입력이 불확실해지는 것을 차단하는 <strong>기본적인 회로 설계 요소</strong>임</li>
</ul>
<h2 id="reference">Reference</h2>
<ol>
<li><a href="https://k96-ozon.tistory.com/59">https://k96-ozon.tistory.com/59</a></li>
<li><a href="https://analog-circuit-design.tistory.com/entry/11-%ED%92%80%EC%97%85-%ED%92%80%EB%8B%A4%EC%9A%B4-%EC%A0%80%ED%95%AD%EC%9D%84-%EC%89%BD%EA%B2%8C-%EC%9D%B4%ED%95%B4%ED%95%B4%EB%B3%B4%EC%9E%90">https://analog-circuit-design.tistory.com/entry/11-%ED%92%80%EC%97%85-%ED%92%80%EB%8B%A4%EC%9A%B4-%EC%A0%80%ED%95%AD%EC%9D%84-%EC%89%BD%EA%B2%8C-%EC%9D%B4%ED%95%B4%ED%95%B4%EB%B3%B4%EC%9E%90</a></li>
<li><a href="https://njh208804.tistory.com/49">https://njh208804.tistory.com/49</a></li>
<li><a href="https://shek.tistory.com/47">https://shek.tistory.com/47</a></li>
<li><a href="https://inho-han.tistory.com/9">https://inho-han.tistory.com/9</a></li>
<li><a href="https://wowon.tistory.com/234">https://wowon.tistory.com/234</a></li>
<li><a href="https://www.y-ic.kr/blog/pull-up-and-pull-down-resistors.html">https://www.y-ic.kr/blog/pull-up-and-pull-down-resistors.html</a></li>
<li><a href="https://kocoafab.cc/tutorial/view/526">https://kocoafab.cc/tutorial/view/526</a></li>
</ol>