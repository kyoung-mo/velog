<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/70929198-d89b-4e3f-9f18-13078a89aba8/image.png" /></p>
<p>터틀봇의 라즈베리파이4에 <code>/etc/netplan</code> 에 <code>50-cloud-init-yaml</code> 넣어주는 과정에서 조금 헤맸었습니다.</p>
<p>이제 환경세팅이 끝났다 싶을때 쯤 우분투에 SSH로 접속을 하려 하는데 평소에 접속하던 IP로 접속이 안되는 문제가 있었습니다. 그래서 SSH 설정을 확인해봤으나 SSH는 Activate로 문제가 없었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cf566551-cf3d-4cc2-8a75-6937bd45c01d/image.png" /></p>
<p>이후 네트워크 연결을 확인해봤는데 이더넷 연결이 되지 않았습니다. 윈도우는 이더넷을 통해 인터넷이 잘 되는 상황이였는데 우분투만 접속이 되지 않는 상황이라 의아했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5d7e78a4-d548-4476-9c06-21e75504037d/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/dc0cb04a-7079-45d4-aef1-9a9c3d8aacde/image.png" /></p>
<p>원래 정상적인 화면이라면 아래처럼 <code>유선</code> 이라는 칸 안에서 이더넷이 연결되어, 할당해준 고정IP로 연결이 되어야하는데 아예 유선 탭이 사라져있었습니다.</p>
<p>여러 설정들을 확인해봤으나, 크게 건드린게 없었어서 문제가 되지 않았습니다.</p>
<p><strong>virtualBox 네트워크 설정 확인</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5bc00017-bd3b-49ed-bf45-737d86292bce/image.png" /></p>
<p><strong>nmcli 명령어로 고정 IP 설정 시도</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e25f76ae-9a82-4c36-9061-b1549cb07821/image.png" /></p>
<p>** NetworkManager 설정 파일을 직접 확인/수정 시도**</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/38747716-3c34-495b-a9fc-50650eb81acf/image.png" /></p>
<p>그래도 문제는 해결되지 않았습니다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a362b725-b1b8-4f8f-ba43-2f23059f84d8/image.png" /></p>
<p>무지성으로 AI를 따라가다가 생각 정리를 끝내고 나니, 수업시간에 진행했던 내용이 라즈베리파이의 <code>/etc/netplan</code> 파일 수정, <code>OpenCV 4.12.0</code> 버전 빌드 말고는 없었기 때문에 <code>/etc/netplan</code> 디렉토리를 확인해보았습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/260dc339-c172-42e7-9484-2f9c2e2065a3/image.png" /></p>
<p>이 부분이 문제였습니다. 라즈베리파이 환경에 넣어줘야 할것을 헤매다가 우분투에 파일을 넣어준 것이 문제였습니다.</p>
<p>짝꿍은 이더넷이 문제없이 작동했기때문에 짝꿍의 <code>/etc/netplan</code>에 들어가있는 파일 이름, 내용을 똑깥이 수정했습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5ef75af2-13f7-4c9c-8bf3-7e0137155fa3/image.png" /></p>
<blockquote>
<p><code>renderer: NetworkManager</code> 이 부분이 핵심이였습니다.</p>
</blockquote>
<p>라즈베리파이4에 들어가야할 <code>50-cloud-init.yaml</code> 파일에서는 <code>renderer: networkd</code> 로 설정되어있었어서 <code>systemed-networkd</code>가 관리하게 설정되어있었습니다.</p>
<hr />
<h3 id="파일-이름-앞-숫자의-의미">파일 이름 앞 숫자의 의미</h3>
<pre><code class="language-bash">50-cloud-init.yaml
01-network-manager-all.yaml</code></pre>
<p>추가적으로, Netplan은 <code>/etc/netplan</code> 안의 파일을 숫자 오름차순으로 읽는다고 합니다.</p>
<p><code>01</code> 이 <code>50</code> 보다 먼저 읽히고, 같은 인터페이스 설정이 충돌하게 되면, 나중 파일을 덮어씁니다.</p>
<p>원래는 저도 <code>01-network-manager-all.yaml</code> 파일이 있었으나, <code>/etc/netplan</code> 설정을 진행할 때 원래는 아무 파일도 없어야하는데 뭔가 있길래 삭제했던 기억이 있습니다. 그게 우분투 환경에서 <code>01-network-manager-all.yaml</code> 이 파일을 삭제했던 것 같습니다.</p>
<hr />
<h2 id="정리">정리</h2>
<p>결국 이번 트러블슈팅의 근본적인 원인은 </p>
<p>&quot;라즈베리파이용 설정 파일을 Ubuntu에 넣었더니 renderer가 networkd로 바뀌어버려서 NetworkManager가 인터페이스를 관리하지 못하게 된 것&quot; 이었고, </p>
<p>renderer를 NetworkManager로 되돌리면서 해결되었습니다.</p>