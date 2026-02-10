<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6e8c4c68-33dc-461b-82e0-4ac4d9a14889/image.png" /></p>
<p>TCP는 연결 지향형(Connection-oriented) 프로토콜로서, 신뢰성을 보장하는 1:1 통신이라는 특징이 있어 은행 창구에 방문하는 고객이라는 아이디어를 구상해보았습니다.</p>
<hr />
<ul>
<li>서버(은행) : 메인 스레드 + 워커 스레드(창구들)</li>
<li>클라이언트 : 고객</li>
</ul>
<hr />
<ol>
<li>클라이언트가 서버(은행)에 요청 : 클라이언트 → <code>connect()</code>  호출</li>
<li>메인 스레드(은행)이 어느 창구가 비었는지 확인 후 번호표를 나눠줌 : <code>listen()</code> </li>
<li>클라이언트와 해당 쓰레드가 연결되어 상담 (통신) : <code>accept()</code>  통해 연결</li>
<li>상담이 끝나면 쓰레드 반환 후 재할당 : <code>close()</code> 이후 <code>listen()</code> 으로 돌아감</li>
</ol>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fe8a98bf-21bd-4162-bcd7-57003b76ebe3/image.png" /></p>