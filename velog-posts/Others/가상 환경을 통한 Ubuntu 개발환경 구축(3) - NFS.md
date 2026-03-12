<p><a href="https://velog.io/@mommers/%EA%B0%80%EC%83%81-%ED%99%98%EA%B2%BD%EC%9D%84-%ED%86%B5%ED%95%9C-Ubuntu-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EA%B5%AC%EC%B6%952-Putty">[이전 글] : 가상 환경을 통한 Ubuntu 개발환경 구축(2) - Putty</a></p>
<hr />
<ul>
<li>일단 부팅 시 --- 표시가 뜨던 것을 먼저 수정</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e8f8a4a2-e321-4417-96cb-011495805177/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4c0cf3bd-6811-4c75-b34d-f475eadf354a/image.png" /></p>
<pre><code>sudo vi /mnt/mount.sh</code></pre><p>안에 코드와 ---를 같이 넣어줬어서 출력됐었습니다.</p>
<p>폰트 다운받아서 적용해 준 후, oh-my-bash에서 powerline 적용 시 글자 깨짐 문제 해결</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8a88360f-e53f-43af-b426-7bf0ae76fccc/image.png" /></p>
<p>잘 나오는것을 확인할 수 있습니다.</p>
<hr />
<h2 id="nfs-설정">NFS 설정</h2>
<p>교수님 Ubuntu -&gt; 내 Ubuntu로 마운트,
내 Ubuntu -&gt; 내 RaspberryPi로 마운트를 해주려 합니다.</p>
<p>전자의 과정으로 NFC Client
후자의 과정으로 NFC Server에 대한 과정을 정리해보겠습니다.</p>
<hr />
<h3 id="nfs-server">NFS Server</h3>
<p>제 Ubuntu에서 라즈베리파이로 NFS 서버를 열어주기 위해 아래와 같은 과정을 거칩니다.</p>
<pre><code class="language-bash">$ sudo apt-get install nfs-common nfs-kernel-server rpcbind -y    #패키지 설치
$ sudo mkdir /srv/nfs                    #공유할 디렉토리 생성
$ sudo chmod 777 /srv/nfs</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/77db5700-9d1a-4b17-aeae-5ec378ee64fa/image.png" /></p>
<pre><code class="language-bash">$ sudo vi /etc/exports                    #nfs 환경 설정에 아래 내용 추가

/srv/nfs        10.10.16.0/24(rw,sync)</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a0e9f3de-0ec1-425c-896d-d2d9df6a1ad6/image.png" /></p>
<pre><code class="language-bash">sudo systemctl restart nfs-kernel-server        #nfs 재시작
sudo exportfs                #공유된 디렉토리 확인

# 결과 : /srv/nfs        10.10.16.0/24</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/05daa72d-1404-443c-80aa-f6d15693f3bf/image.png" /></p>
<p>이제 <code>/srv/nfs</code> 로 공유할 파일들을 옮겨주면 공유가 가능합니다.</p>
<hr />
<h3 id="nfs-client">NFS Client</h3>
<pre><code class="language-bash">$ cd /mnt
$ sudo mkdir nfs                #마운트 포인트 디렉토리생성    
$ sudo chmod 777 nfs                #접근 권한 설정
$ sudo mount -t nfs 10.10.16.XX:/srv/nfs nfs      #nfs 서버 연결 (XX : 서버주소)
$ df                                    #연결 확인
10.10.16.XX:/srv/nfs 153188352 12944384 132389888    9% /mnt/nfs
</code></pre>
<p>라즈베리파이 환경에서 아래와 같이 <code>/mnt/nfs</code> 디렉토리를 추가하고, nfs에 일단 확인용으로 <code>sudo chmod 777 nfs</code>로 모든 권한을 부여해줍니다.</p>
<p>이후 Ubuntu의 IP주소인 <code>10.10.16.35:/srv/nfs</code> 폴더에 마운트해주면 </p>
<ul>
<li>라즈베리파이의 <code>/mnt/nfs</code> 디렉토리와 </li>
<li>Ubuntu의 <code>/srv/nfs</code> 디렉토리가 공유됩니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e05db474-f4c6-4461-bc40-62db87fd3471/image.png" /></p>
<pre><code class="language-bash">$ cd /mnt/nfs
$ touch aa.txt                    #파일 생성 확인</code></pre>
<p>테스트용으로 라즈베리파이에서 <code>touch aa.txt</code>를 이용해 파일을 만들고, Ubuntu의 <code>/srv/nfs</code> 디렉토리에서 폴더 목록을 확인</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c20dcd8c-8e48-49aa-8635-718c8329abbd/image.png" /></p>
<p><code>aa.txt</code> 가 추가된 것을 확인할 수 있습니다.</p>
<pre><code class="language-bash">$ sudo umount /mnt/nfs            #마운트 해제
$ df                             #마운트 해제 확인

nfs mount 자동화 쉘 프로그램 작성</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a15f8d68-e18a-45c0-ac0b-31e0e67f0c8e/image.png" /></p>
<pre><code class="language-bash">$ vi ~/.profile        #제일 아래 추가
-----------------------------------------
if [ -f /mnt/mount.sh ]; then
        . /mnt/mount.sh
fi
-----------------------------------------</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/752cc817-54b4-4df4-9d87-b70b8d4c8776/image.png" /></p>
<pre><code class="language-bash">$ sudo vi /mnt/mount.sh 아래내용 복사
-----------------------------------------
#!/bin/bash
SERVIP=10.10.16.XX                   #XX : ubuntu nfs host ip
if ! df | grep nfs &gt; /dev/null ; then
        ping -c 1 $SERVIP &gt; /dev/null
        if [ $? -eq 0 ] ; then
                sudo mount -t nfs $SERVIP:/srv/nfs /mnt/nfs
                df | grep nfs
        fi
fi
-----------------------------------------</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/dad28c74-db0e-4b22-a1e9-f33542208f32/image.png" /></p>
<pre><code class="language-bash">$sudo vi /etc/sudoers.d/01_ubuntu_nopasswd   #sudo 명령 암호 입력  생략 환경 설정
-----------------------------------------
ubuntu    ALL=(ALL) NOPASSWD:/usr/bin/mount
-----------------------------------------</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3d6008f4-ae48-47de-9a91-50b8a9376998/image.png" /></p>
<pre><code class="language-bash">putty로 로그인시 자동 nfs 마운트 확인
$ df 
10.10.16.XX:/srv/nfs  30267392 118908  42% /mnt/nfs</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/010940f5-9cc2-432c-a0e5-333a370a9bd4/image.png" /></p>
<pre><code class="language-bash"># C프로그램  ctags 파일 만들기
$ sudo apt-cache search ctag       # 검색 ctag 문자열 포함된 패키지 목록 보기
$ sudo apt install universal-ctags vim    #패키지 설치
$ cd /usr/include/
패키지 설치
$ sudo ctags -R            #tags 파일 생성
$ ls -l tags
-rw-r--r--  1 root root 12990677  7월  3 11:35 tags

$vi ~/.vimrc    #아래 내용 추가
=================
set tags+=/usr/include/tags
=================</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/553147df-7874-45cf-b72b-abdeec49c528/image.png" /></p>