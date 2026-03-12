<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7ac7e20a-43b2-4d2f-8c48-ddbadfa1db4f/image.png" /></p>
<h3 id="putty-설명"><a href="https://velog.io/@mommers/putty%EB%9E%80-%ED%95%A8%EA%BB%98-%EC%84%A4%EC%B9%98%EB%90%98%EB%8A%94-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8-%EC%9A%A9%EB%8F%84-%EC%A0%95%EB%A6%AC">Putty 설명</a></h3>
<hr />
<p>Putty를 사용하면 가상환경에 우분투 운영체제를 설치해주고 나서, putty를 통해 윈도우 환경에서 putty를 통해 Ubuntu와 라즈베리파이 개발을 할 수 있다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4631d097-e5f4-48db-aea0-e5212625c059/image.png" /></p>
<p>그 전에 Ubuntu에서 ssh를 활성화 해줘야하는데.. 캡쳐 떠둔게 없기 때문에 코드만 올려두겠습니다.</p>
<pre><code class="language-c">// ssh server 설치
$sudo apt install openssh-server
// 윈도우즈에서 putty 설치 및 원격 접속</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f4968b00-aa95-4198-aeb9-841f6035f96b/image.png" /></p>
<p>putty에서 ip주소 + ssh 기본 포트인 22 입력 후 접속 가능한 것을 확인할 수 있다.</p>
<p>+ raspberry pi도 고정 ip 설정 + ssh 설정 켜주고, putty로 접속 가능합니다.</p>
<h2 id="라즈베리파이-고정-ip-설정법">라즈베리파이 고정 ip 설정법</h2>
<pre><code class="language-bash">sudo nmtui &lt;&lt; gui 환경 모사하여 설정 가능</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5bd42b27-33cc-4f4f-b588-e918ce2d2933/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ca5a5c8a-829c-44f9-b48c-906d8e3696cc/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/40720c06-7d6d-487c-b516-128c8720b34c/image.png" /></p>
<p>위와 같이 설정 -&gt; <code>sudo reboot</code> 하면 적용 완료</p>
<hr />
<p>그 뒤에는 교수님 Ubuntu -&gt; 내 Ubuntu로 마운트
내 Ubuntu -&gt; 내 Raspberrypi로 마운트 하는 과정을 정리해보겠습니다.</p>
<p><a href="https://velog.io/@mommers/%EA%B0%80%EC%83%81-%ED%99%98%EA%B2%BD%EC%9D%84-%ED%86%B5%ED%95%9C-Ubuntu-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EA%B5%AC%EC%B6%953-NFS">[다음 글 : 가상 환경을 통한 Ubuntu 개발환경 구축(3) - NFS]</a></p>