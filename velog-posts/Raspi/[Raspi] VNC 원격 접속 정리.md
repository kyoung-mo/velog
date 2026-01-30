<p>라즈베리파이와, MobaXterm(window 환경)을 통해 VNC 접속이 가능하다.</p>
<ul>
<li><strong>VNC (Virtual Network Computing):</strong><ul>
<li>그래픽 기반(GUI) 원격 제어.</li>
<li>서버 설정: <code>raspi-config</code> → Interface Options → VNC Enable.</li>
<li>클라이언트: PC에 'RealVNC Viewer' 설치.</li>
<li>접속: IP 주소 입력 → 라즈베리 파이 화면 원격 조작.</li>
<li><strong>Troubleshooting:</strong> 화면 안 보일 시 <code>raspi-config</code>에서 해상도 강제 설정 필요.</li>
</ul>
</li>
</ul>
<hr />
<p>터미널을 열고</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/151ffefe-b60a-476c-803e-92816474d498/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bf2a4c79-babe-4c40-8c14-c46644c002a2/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fa548af5-baf3-40b2-9794-51923384fc18/image.png" /></p>
<p>서버(라즈베리파이)에서 VNC를 enable 해주고, 이제 윈도우에서 MobaXterm을 켜준다.</p>
<p>Session settings 에서 <code>VNC</code> 선택, IP 주소를 입력해준다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e6467664-acc6-48dc-bfd0-f859f7db7ef9/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5530ea1a-8e5f-4b69-ab1a-139594ee652c/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3db2a84f-a043-40cd-a051-bb2b30f1b4ae/image.png" /></p>
<p>비밀번호 입력 후, 다음 창에서 OK 하면 넘어가진다. 캡쳐가 안되서 패스</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b44b89e0-4270-41a3-97f0-0e5f31151b24/image.png" /></p>
<p>비밀번호가 약하면 설정을 다시 하라고 한다. 비밀번호 입력 후 OK 버튼 클릭</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/564020cd-f401-4238-8300-4d5f3e9b540c/image.png" /></p>
<p>접속이 완료된 모습</p>