<h3 id="커널-모듈-빌드-및-실행">커널 모듈 빌드 및 실행</h3>
<p>일반 애플리케이션은 <code>gcc -o</code>로 컴파일하지만, 커널 모듈은 커널 빌드 시스템(kbuild)을 통해 컴파일해야 합니다. <code>Makefile</code>을 만들고 <code>make</code> 명령어로 빌드하면 <code>.ko</code> (Kernel Object) 파일이 생성됩니다.</p>
<hr />
<h3 id="1-준비-커널-헤더-설치">1. 준비: 커널 헤더 설치</h3>
<p>현재 실행 중인 커널 버전에 맞는 헤더 파일이 필요합니다.</p>
<pre><code class="language-bash"># 우분투 / 라즈비안 (Debian 계열)
sudo apt-get update
sudo apt-get install build-essential linux-headers-$(uname -r)</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2ae67330-f689-4b3b-bb54-a82dc6d2db50/image.png" /></p>
<h3 id="wsl2에서는-안-되는-이유">WSL2에서는 안 되는 이유</h3>
<p>WSL2는 일반 리눅스 커널이 아니라 마이크로소프트가 개조한 전용 커널을 씁니다.</p>
<ul>
<li>일반 리눅스: <code>apt install linux-headers-$(uname -r)</code>로 설치 가능</li>
<li>WSL2: <code>uname -r</code> 결과가 <code>5.15.90.1-microsoft-standard-WSL2</code> 이런 식으로 나오는데, 이 버전에 맞는 헤더가 우분투 저장소(apt)에 없습니다</li>
</ul>
<p>따라서 WSL에서는 커널 모듈 개발이 까다롭습니다.</p>
<hr />
<h3 id="2-소스-코드-작성">2. 소스 코드 작성</h3>
<p><code>kernel_task_check.c</code> 파일을 만듭니다:</p>
<pre><code class="language-c">#include &lt;linux/module.h&gt;
#include &lt;linux/kernel.h&gt;
#include &lt;linux/sched.h&gt;

int init_module(void) {
    struct task_struct *task = current;
    printk(KERN_INFO &quot;[Kernel] Module Loaded.\n&quot;);
    printk(KERN_INFO &quot;[Kernel] Current PID: %d, Comm: %s\n&quot;, task-&gt;pid, task-&gt;comm);
    return 0;
}

void cleanup_module(void) {
    printk(KERN_INFO &quot;[Kernel] Module Removed.\n&quot;);
}

MODULE_LICENSE(&quot;GPL&quot;);</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/416a3837-4b29-4789-b4a4-edb10cab5895/image.png" /></p>
<hr />
<h3 id="3-makefile-작성">3. Makefile 작성</h3>
<p>같은 폴더에 <code>Makefile</code> (대소문자 주의)을 만들고 아래 내용을 입력합니다.</p>
<p>중요: <code>make</code> 구문의 들여쓰기는 반드시 Tab 키를 사용해야 합니다 (스페이스 안 됨).</p>
<pre><code class="language-makefile">obj-m += kernel_task_check.o

all:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f057b1b0-387a-469c-a7ae-4da6ff2a3cd3/image.png" /></p>
<hr />
<h3 id="4-실행-및-확인">4. 실행 및 확인</h3>
<h4 id="①-컴파일">① 컴파일</h4>
<pre><code class="language-bash">make</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3972a95e-d652-4c24-9735-d1d003b67f46/image.png" /></p>
<p>실수로 홈 디렉토리에 파일 만들고 빌드해서.. 소스 코드만 원하는 폴더로 옮기고 re-build 해주었습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ac85eae4-52cb-4698-bda8-7abff933f5b1/image.png" /></p>
<p>성공하면 <code>kernel_task_check.ko</code> 파일이 생성됩니다.</p>
<hr />
<h4 id="②-모듈-적재-load">② 모듈 적재 (Load)</h4>
<p>커널 영역에 모듈을 로드합니다 (root 권한 필요):</p>
<pre><code class="language-bash">sudo insmod kernel_task_check.ko</code></pre>
<hr />
<h4 id="③-결과-확인">③ 결과 확인</h4>
<p><code>printf</code>가 아니라 <code>printk</code>를 사용했기 때문에 출력이 터미널이 아닌 커널 로그 버퍼에 찍힙니다.</p>
<pre><code class="language-bash">sudo dmesg | tail</code></pre>
<p>출력 예시:</p>
<pre><code>[Kernel] Module Loaded.
[Kernel] Current PID: 1234, Comm: insmod</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/37af8023-b436-4c8e-acef-2597518f0865/image.png" /></p>
<p><code>[479830.297782] kernel_task_check: loading out-of-tree module taints kernel.</code> 오류</p>
<ul>
<li>kernel_task_check: 모듈 이름</li>
<li>loading out-of-tree module: &quot;커널 외부 모듈을 로딩 중&quot;</li>
<li>taints kernel: 커널을 &quot;오염(taint)&quot;시킨다는 경고</li>
</ul>
<p>왜 오염? -&gt; 공식 커널이 아닌 외부에서 만든 코드니까 안정성을 보장할 수 없다는 뜻이다.</p>
<hr />
<h4 id="④-모듈-제거-unload">④ 모듈 제거 (Unload)</h4>
<pre><code class="language-bash">sudo rmmod kernel_task_check</code></pre>
<p>다시 <code>sudo dmesg | tail</code>로 확인하면 <code>[Kernel] Module Removed.</code> 메시지를 볼 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b235110f-c2b4-4919-b72d-92f31844b181/image.png" /></p>