<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bf87dc21-e700-4cf8-b05b-66c37ecb52ec/image.png" /></p>
<h2 id="목차">목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#matplotlib%EC%9D%B4%EB%9E%80">Matplotlib이란</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%84%A4%EC%B9%98-%EB%B0%8F-%EB%B6%88%EB%9F%AC%EC%98%A4%EA%B8%B0">설치 및 불러오기</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%95%9C%EA%B8%80-%ED%8F%B0%ED%8A%B8-%EC%84%A4%EC%A0%95">한글 폰트 설정</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EA%B3%B5%ED%86%B5-%EA%B8%B0%EB%B3%B8-%EB%AC%B8%EB%B2%95">공통 기본 문법</a></li>
<li><a href="https://api.velog.io/rss/@mommers#matplotlib-%EA%B7%B8%EB%9E%98%ED%94%84-%EC%A2%85%EB%A5%98">Matplotlib 그래프 종류</a><ul>
<li><a href="https://api.velog.io/rss/@mommers#%EB%9D%BC%EC%9D%B8-%ED%94%8C%EB%A1%AF-line-plot">라인 플롯</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B0%94-%EC%B0%A8%ED%8A%B8-bar-chart">바 차트</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%9E%88%EC%8A%A4%ED%86%A0%EA%B7%B8%EB%9E%A8-histogram">히스토그램</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8A%A4%EC%BA%90%ED%84%B0-%ED%94%8C%EB%A1%AF-scatter-plot">스캐터 플롯</a></li>
</ul>
</li>
<li><a href="https://api.velog.io/rss/@mommers#seaborn%EC%9D%B4%EB%9E%80">Seaborn이란</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%84%A4%EC%B9%98-%EB%B0%8F-%EC%8A%A4%ED%83%80%EC%9D%BC-%EC%84%A4%EC%A0%95">설치 및 스타일 설정</a></li>
<li><a href="https://api.velog.io/rss/@mommers#seaborn-%EA%B7%B8%EB%9E%98%ED%94%84-%EC%A2%85%EB%A5%98">Seaborn 그래프 종류</a><ul>
<li><a href="https://api.velog.io/rss/@mommers#%EC%82%B0%EC%A0%90%EB%8F%84-scatter">산점도 (scatterplot / lmplot)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%9E%88%EC%8A%A4%ED%86%A0%EA%B7%B8%EB%9E%A8-displot">히스토그램 · 밀도 분포 (displot / KDE)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B0%95%EC%8A%A4%ED%94%8C%EB%A1%AF-boxplot">박스플롯 · pairplot</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%A7%89%EB%8C%80%EA%B7%B8%EB%9E%98%ED%94%84-bar--count">막대그래프 (countplot / barplot)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%84%A0%EA%B7%B8%EB%9E%98%ED%94%84-line">선그래프 (lineplot)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%9E%88%ED%8A%B8%EB%A7%B5-heatmap">히트맵 (heatmap)</a></li>
</ul>
</li>
</ul>
<hr />
<h2 id="matplotlib이란">Matplotlib이란</h2>
<p>Matplotlib은 파이썬에서 데이터를 차트(chart)나 플롯(plot)으로 시각화하는 가장 기본적인 라이브러리입니다. 2002년 John D. Hunter가 개발했으며, 현재 파이썬 시각화 생태계의 기반을 이루고 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/620468a7-5220-4cce-a508-552d9b7c35f1/image.png" /></p>
<p>지원하는 주요 그래프 종류는 라인 플롯, 스캐터 플롯, 컨투어 플롯, 서피스 플롯, 바 차트, 히스토그램, 박스 플롯 등 다양합니다. 커스터마이징이 매우 자유롭지만, 그만큼 코드가 길고 복잡해질 수 있다는 단점이 있습니다.</p>
<blockquote>
<p>Matplotlib은 시각화의 기본 엔진 역할을 하며, Seaborn은 Matplotlib 위에서 더 쉽고 아름다운 시각화를 제공하는 고수준 래퍼(wrapper)입니다. 실무에서는 두 라이브러리를 함께 사용하는 경우가 많습니다.</p>
</blockquote>
<hr />
<h2 id="설치-및-불러오기">설치 및 불러오기</h2>
<pre><code class="language-python"># 설치
pip install matplotlib

# 불러오기
import matplotlib.pylab as plt

# 주피터 노트북에서 그래프를 노트북 안에 표시하려면 아래 매직 커맨드 사용
%matplotlib inline       # 정적 이미지로 출력
%matplotlib notebook     # 인터랙티브 출력 (그래프 조작 가능)</code></pre>
<blockquote>
<p><code>pylab</code> 서브패키지는 MATLAB의 시각화 명령을 거의 그대로 사용할 수 있도록 Matplotlib의 하위 API를 포장(wrapping)한 명령어 집합입니다. 일반적으로 <code>import matplotlib.pyplot as plt</code>를 사용하지만 실습에서는 <code>pylab</code>을 많이 활용합니다.</p>
</blockquote>
<hr />
<h2 id="한글-폰트-설정">한글 폰트 설정</h2>
<p>Matplotlib은 기본적으로 한글을 지원하지 않습니다. 한글을 출력하려면 별도 설정이 필요합니다.</p>
<p><strong>방법 1 — 한글 지원 패키지 설치 (가장 간단)</strong></p>
<pre><code class="language-python">pip install koreanize-matplotlib

# 설치 후 임포트만 하면 자동으로 한글 폰트가 적용됩니다
import koreanize_matplotlib</code></pre>
<p><strong>방법 2 — Linux(Colab) 환경에서 나눔 폰트 설치</strong></p>
<pre><code class="language-bash">sudo apt-get install -y fonts-nanum
sudo fc-cache -fv
rm ~/.cache/matplotlib -rf
# 설치 후 런타임을 재시작해야 적용됩니다</code></pre>
<p>적용 후에는 아래와 같이 한글 제목과 라벨을 정상적으로 출력할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/23e84a65-d0d2-4ddd-ba37-40187928062c/image.png" /></p>
<pre><code class="language-python">plt.title('한글 제목')
plt.plot([10, 20, 30, 40], [1, 4, 9, 16])
plt.xlabel(&quot;엑스축 라벨&quot;)
plt.ylabel(&quot;와이축 라벨&quot;)
plt.show()</code></pre>
<hr />
<h2 id="공통-기본-문법">공통 기본 문법</h2>
<p>Matplotlib과 Seaborn을 함께 사용할 때의 표준적인 코드 구조입니다.</p>
<pre><code class="language-python">import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(가로, 세로))          # 그래프 크기 설정
sns.xxxplot(data=df, x='열이름', y='열이름', hue='범례 열')
plt.title('제목')
plt.xlabel('x축 라벨')
plt.ylabel('y축 라벨')
plt.legend(loc='upper left')             # 범례 위치
plt.xticks(rotation=45)                  # x축 눈금 각도
plt.yticks(rotation=0)
plt.show()                               # 그래프 출력</code></pre>
<hr />
<h2 id="라인-플롯-line-plot">라인 플롯 (Line Plot)</h2>
<p>데이터가 시간이나 순서에 따라 어떻게 변화하는지 보여주는 그래프입니다. <code>plt.plot()</code> 명령을 사용합니다.</p>
<h3 id="기본-사용법">기본 사용법</h3>
<pre><code class="language-python"># y값만 지정 — x축은 자동으로 0, 1, 2, 3 ...
plt.title('Plot')
plt.plot([1, 4, 9, 16])
plt.show()

# x값, y값 모두 지정
plt.plot([10, 20, 30, 40], [1, 4, 9, 16])
plt.show()</code></pre>
<h3 id="스타일-지정">스타일 지정</h3>
<p>색상, 마커, 선 스타일을 조합하여 그래프 외형을 커스터마이징할 수 있습니다.</p>
<p><strong>색상(color)</strong></p>
<table>
<thead>
<tr>
<th>약자</th>
<th>색상</th>
</tr>
</thead>
<tbody><tr>
<td><code>b</code></td>
<td>파랑(blue)</td>
</tr>
<tr>
<td><code>g</code></td>
<td>초록(green)</td>
</tr>
<tr>
<td><code>r</code></td>
<td>빨강(red)</td>
</tr>
<tr>
<td><code>k</code></td>
<td>검정(black)</td>
</tr>
<tr>
<td><code>w</code></td>
<td>흰색(white)</td>
</tr>
</tbody></table>
<p>RGB 코드(<code>#FF5733</code> 형식)도 사용할 수 있습니다.</p>
<p><strong>마커(marker)</strong></p>
<table>
<thead>
<tr>
<th>기호</th>
<th>마커</th>
</tr>
</thead>
<tbody><tr>
<td><code>*</code></td>
<td>스타</td>
</tr>
<tr>
<td><code>+</code></td>
<td>플러스</td>
</tr>
<tr>
<td><code>o</code></td>
<td>원</td>
</tr>
<tr>
<td><code>s</code></td>
<td>사각형</td>
</tr>
</tbody></table>
<p><strong>선 스타일(line style)</strong></p>
<table>
<thead>
<tr>
<th>기호</th>
<th>선 종류</th>
</tr>
</thead>
<tbody><tr>
<td><code>-</code></td>
<td>실선</td>
</tr>
<tr>
<td><code>--</code></td>
<td>대시선</td>
</tr>
<tr>
<td><code>-.</code></td>
<td>대시-점선</td>
</tr>
<tr>
<td><code>:</code></td>
<td>점선</td>
</tr>
</tbody></table>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f1fce40f-64fe-43a2-89e0-45e2632583dd/image.png" /></p>
<pre><code class="language-python">plt.plot([10, 20, 30, 40], [1, 4, 9, 16],
         c=&quot;b&quot;,        # 색상: 파랑
         lw=5,         # 선 굵기(linewidth)
         ls=&quot;--&quot;,      # 선 스타일: 대시선
         marker=&quot;o&quot;,   # 마커: 원
         ms=15,        # 마커 크기(markersize)
         mec=&quot;g&quot;,      # 마커 테두리 색(markeredgecolor)
         mew=5,        # 마커 테두리 굵기(markeredgewidth)
         mfc=&quot;r&quot;)      # 마커 내부 색(markerfacecolor)
plt.title(&quot;스타일 적용 예&quot;)
plt.show()</code></pre>
<h3 id="축-범위-지정">축 범위 지정</h3>
<p><code>xlim</code>과 <code>ylim</code>으로 x축, y축의 표시 범위를 수동으로 지정할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e1426b96-fff1-4e1a-855b-b4a039283e41/image.png" /></p>
<pre><code class="language-python">plt.plot([10, 20, 30, 40], [1, 4, 9, 16], c='b', lw=5, ls='--', marker='o')
plt.xlim(0, 50)    # x축: 0 ~ 50
plt.ylim(-10, 30)  # y축: -10 ~ 30
plt.grid(True)     # 격자 표시
plt.show()</code></pre>
<h3 id="여러-선-그리기">여러 선 그리기</h3>
<p><code>plot()</code> 에 <code>(x, y, 스타일)</code> 묶음을 반복하여 넘기면 여러 선을 한 번에 그릴 수 있습니다. 이때 x 데이터와 스타일 문자열을 <strong>생략할 수 없습니다.</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/83303606-8fae-4e29-8104-611604ec4274/image.png" /></p>
<pre><code class="language-python">import numpy as np

t = np.arange(0., 5., 0.5)
plt.title('라인 플롯에서 여러개 선 그리기')
plt.plot(t, t,          'r--',   # 빨강 대시선
         t, 0.5*t**2,   'bs:',   # 파랑 사각형 점선
         t, 0.2*t**3,   'g^-')   # 초록 삼각형 실선
plt.show()</code></pre>
<h3 id="범례-추가">범례 추가</h3>
<p>각 선이 어떤 데이터를 나타내는지 범례(legend)로 표시합니다. <code>label</code> 인수로 이름을 지정하고, <code>plt.legend()</code>로 출력합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6156a054-d57e-42fb-a189-6b3f712773b5/image.png" /></p>
<pre><code class="language-python">X = np.linspace(-np.pi, np.pi, 256)
C, S = np.cos(X), np.sin(X)

plt.plot(X, C, ls=&quot;--&quot;, label=&quot;cosine&quot;)
plt.plot(X, S, ls=&quot;:&quot;,  label=&quot;sine&quot;)
plt.legend(loc=2)   # 2 = upper left
plt.title(&quot;legend를 표시한 플롯&quot;)
plt.show()</code></pre>
<p><strong><code>loc</code> 위치 옵션</strong></p>
<table>
<thead>
<tr>
<th>값</th>
<th>위치</th>
</tr>
</thead>
<tbody><tr>
<td><code>0</code></td>
<td>best (자동)</td>
</tr>
<tr>
<td><code>1</code></td>
<td>upper right</td>
</tr>
<tr>
<td><code>2</code></td>
<td>upper left</td>
</tr>
<tr>
<td><code>3</code></td>
<td>lower left</td>
</tr>
<tr>
<td><code>4</code></td>
<td>lower right</td>
</tr>
</tbody></table>
<h3 id="축-라벨과-제목">축 라벨과 제목</h3>
<pre><code class="language-python">plt.xlabel(&quot;time&quot;)       # x축 라벨
plt.ylabel(&quot;amplitude&quot;)  # y축 라벨
plt.title(&quot;Cosine Plot&quot;) # 그래프 제목</code></pre>
<hr />
<h2 id="바-차트-bar-chart">바 차트 (Bar Chart)</h2>
<p>x 데이터가 카테고리 값(문자열 등)인 경우 <code>bar()</code> 명령으로 바 차트를 그립니다. 가로 방향은 <code>barh()</code>를 사용합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/30ba66a7-2283-47f9-8779-fcb370dbab7c/image.png" /></p>
<pre><code class="language-python">y = [2, 3, 1]
x = np.arange(len(y))
xlabel = ['가', '나', '다']

plt.title('바 차트')
plt.bar(x, y)
plt.xticks(x, xlabel)      # x축 눈금 라벨 지정
plt.yticks(sorted(y))      # y축 눈금 값 지정
plt.xlabel('가나다')
plt.ylabel('빈도수')
plt.grid(True)
plt.show()</code></pre>
<hr />
<h2 id="히스토그램-histogram">히스토그램 (Histogram)</h2>
<p>연속형 데이터의 분포를 구간으로 나눠 빈도를 시각화합니다. <code>bins</code> 인수로 구간 수를 지정합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/748d5efb-a948-4d87-9508-aef601828381/image.png" /></p>
<pre><code class="language-python">np.random.seed(0)
x = np.random.randn(1000)  # 표준정규분포에서 1000개 샘플

plt.title(&quot;Histogram&quot;)
arrays, bins, patches = plt.hist(x, bins=10)
plt.grid(True)
plt.show()</code></pre>
<blockquote>
<p><code>hist()</code>는 반환값으로 각 구간의 빈도수(<code>arrays</code>), 구간 경계값(<code>bins</code>), 막대 패치 객체(<code>patches</code>)를 함께 반환합니다.</p>
</blockquote>
<hr />
<h2 id="스캐터-플롯-scatter-plot">스캐터 플롯 (Scatter Plot)</h2>
<p>두 변수 사이의 상관관계를 점으로 시각화합니다. 점 하나가 데이터 하나의 (x, y) 값을 나타냅니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8aea22af-fcd5-47f1-aae8-8daeebe7a671/image.png" /></p>
<pre><code class="language-python">np.random.seed(0)
X = np.random.normal(0, 1, 100)
Y = np.random.normal(0, 1, 100)

plt.title(&quot;Scatter Plot&quot;)
plt.scatter(X, Y)
plt.show()</code></pre>
<hr />
<h2 id="seaborn이란">Seaborn이란</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0fcefa83-9a71-4a2a-a2d0-33e5f6883a2e/image.png" /></p>
<p>Seaborn은 Matplotlib을 기반으로 더 쉽고 아름다운 시각화를 제공하는 고수준 라이브러리입니다. Pandas DataFrame을 직접 인수로 받아 열 이름으로 축과 색상을 지정할 수 있어, Matplotlib보다 코드가 훨씬 간결합니다.</p>
<blockquote>
<p>Seaborn은 단독으로도 사용할 수 있지만, <code>plt.title()</code>, <code>plt.xlabel()</code> 등 세부 설정은 Matplotlib으로 처리하는 것이 일반적입니다. 두 라이브러리를 함께 임포트하여 사용합니다.</p>
</blockquote>
<hr />
<h2 id="설치-및-불러오기--seaborn">설치 및 불러오기 — Seaborn</h2>
<pre><code class="language-python">pip install seaborn

import seaborn as sns
import matplotlib.pyplot as plt</code></pre>
<p>Seaborn에는 학습용 내장 데이터셋이 제공됩니다. <code>sns.load_dataset('데이터셋이름')</code>으로 바로 불러올 수 있습니다.</p>
<pre><code class="language-python"># 펭귄 데이터셋 (species, island, bill_length_mm, body_mass_g 등)
penguin = sns.load_dataset('penguins')

# 타이타닉 데이터셋
titanic = sns.load_dataset('titanic')

# 항공 승객 데이터셋
flights = sns.load_dataset('flights')</code></pre>
<hr />
<h2 id="스타일-및-팔레트-설정">스타일 및 팔레트 설정</h2>
<p><code>sns.set_style()</code>과 <code>sns.set_palette()</code>로 전체 그래프의 스타일과 색상을 일괄 변경할 수 있습니다.</p>
<p><strong>스타일 종류</strong>: <code>darkgrid</code>, <code>whitegrid</code>, <code>dark</code>, <code>white</code></p>
<pre><code class="language-python">sns.set_style('darkgrid')   # 어두운 격자 배경
sns.set_style('white')      # 흰색 배경</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d1966839-e1c3-4a93-8708-f42466731abb/image.png" /></p>
<p><strong>팔레트 지정</strong></p>
<pre><code class="language-python">sns.set_palette('Set2')    # 부드러운 색상 세트
sns.set_palette('flare')   # 붉은 계열 그라데이션</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8c85007b-4322-42e4-a455-85499e1f584a/image.png" /></p>
<blockquote>
<p><a href="https://seaborn.pydata.org/tutorial/color_palettes.html">Seaborn 팔레트 목록</a>에서 다양한 팔레트를 확인할 수 있습니다.</p>
</blockquote>
<p><strong>고화질 출력 설정</strong></p>
<pre><code class="language-python">%config InlineBackend.figure_format = 'retina'</code></pre>
<hr />
<h2 id="산점도-scatter">산점도 (Scatter)</h2>
<p>두 연속형 변수 간의 관계를 점으로 나타냅니다. <code>hue</code> 인수로 카테고리별 색상을 구분할 수 있습니다.</p>
<pre><code class="language-python"># 기본 산점도
sns.scatterplot(data=penguin, x='bill_length_mm', y='bill_depth_mm')
plt.show()

# 성별(hue)로 색상 구분
sns.scatterplot(data=penguin, x='bill_length_mm', y='bill_depth_mm', hue='sex')
plt.show()

# style로 마커 모양, hue로 색상 동시 구분
sns.scatterplot(data=penguin, x='bill_length_mm', y='bill_depth_mm',
                style='sex', hue='island')
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/86924cee-57b9-4621-b399-2bc0651c0bdb/image.png" />
<strong>회귀선 포함 산점도 — <code>lmplot()</code></strong></p>
<pre><code class="language-python"># 회귀선 추가
sns.lmplot(data=penguin, x='bill_length_mm', y='bill_depth_mm')

# island별로 서브플롯 분리 + 성별 색상 구분
sns.lmplot(data=penguin, x='bill_length_mm', y='bill_depth_mm',
           hue='sex', col='island')
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5b168116-5874-4c68-bfbf-c5ad502f11d7/image.png" /></p>
<p><strong><code>col</code> 인수 — 서브플롯 분리</strong></p>
<p><code>col='열이름'</code>을 지정하면 해당 열의 카테고리별로 그래프를 가로로 나란히 출력합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/261ce128-ec42-4912-98eb-3c6fa00120ba/image.png" /></p>
<hr />
<h2 id="히스토그램-displot">히스토그램 (displot)</h2>
<p>Seaborn의 <code>displot()</code>은 히스토그램과 KDE를 함께 지원합니다.</p>
<pre><code class="language-python"># 기본 히스토그램
sns.displot(data=penguin, x='flipper_length_mm')
plt.show()

# KDE 곡선 함께 표시
sns.displot(data=penguin, x='flipper_length_mm', kde=True)
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4de3892a-6f16-43d8-8f0f-b896312d2f80/image.png" /></p>
<hr />
<h2 id="밀도-분포-kde">밀도 분포 (KDE)</h2>
<p><code>kind='kde'</code>로 지정하면 히스토그램 대신 연속적인 밀도 곡선을 그립니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1f5d9edd-1c76-4188-b72c-e050c48610fc/image.png" /></p>
<pre><code class="language-python"># 기본 KDE
sns.displot(data=penguin, x='flipper_length_mm', kind='kde')

# species별 KDE
sns.displot(data=penguin, x='flipper_length_mm', hue='species', kind='kde')

# island별 서브플롯 + species별 색상
sns.displot(data=penguin, x='flipper_length_mm',
            hue='species', col='sex', kind='kde')
plt.show()</code></pre>
<blockquote>
<p>KDE(Kernel Density Estimation, 커널 밀도 추정)는 데이터의 분포를 부드러운 곡선으로 표현합니다. 히스토그램보다 bin 크기의 영향을 받지 않아 분포 형태를 더 직관적으로 파악할 수 있습니다.</p>
</blockquote>
<hr />
<h2 id="박스플롯-boxplot">박스플롯 (Boxplot)</h2>
<p>데이터의 분포, 중앙값, 이상치를 한 눈에 볼 수 있는 그래프입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1faeaf40-41ca-4aeb-8def-4c06a77cad8e/image.png" /></p>
<p>박스플롯의 각 구성 요소는 다음과 같습니다.</p>
<ul>
<li><strong>박스 아래 끝</strong> — 1사분위수(Q1, 25%)</li>
<li><strong>박스 가운데 선</strong> — 중앙값(Q2, 50%)</li>
<li><strong>박스 위 끝</strong> — 3사분위수(Q3, 75%)</li>
<li><strong>수염(whisker)</strong> — Q1 - 1.5×IQR ~ Q3 + 1.5×IQR 범위</li>
<li><strong>점</strong> — 수염 밖의 이상치(outlier)</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/289bd624-1596-469c-b2b3-674233f6827c/image.png" /></p>
<pre><code class="language-python"># 단일 변수 박스플롯
sns.boxplot(data=penguin, x='body_mass_g')
plt.show()

# 종별·성별 박스플롯
sns.boxplot(data=penguin, x='body_mass_g', y='species', hue='sex')
plt.show()</code></pre>
<p><strong>pairplot — 여러 변수 간 관계 한번에 보기</strong></p>
<pre><code class="language-python"># 모든 수치형 변수 조합의 산점도 + 히스토그램
sns.pairplot(data=penguin)

# species별 색상 구분
sns.pairplot(data=penguin, hue='species')
plt.show()</code></pre>
<blockquote>
<p><code>pairplot()</code>은 데이터셋의 변수 수가 많아질수록 출력이 느려집니다. 탐색적 데이터 분석(EDA) 초기 단계에서 변수 간 관계를 빠르게 파악할 때 유용합니다.</p>
</blockquote>
<hr />
<h2 id="막대그래프-bar--count">막대그래프 (Bar / Count)</h2>
<p><strong><code>countplot()</code> — 범주별 행 개수 집계</strong></p>
<pre><code class="language-python"># 등급별 생존 여부 카운트
sns.countplot(data=titanic, x='class', hue='alive')
plt.show()

# 성별 생존 여부 카운트
sns.countplot(data=titanic, x='sex', hue='alive')
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/05dd2c9e-4302-439a-aa09-774f2e570e0d/image.png" /></p>
<p><strong><code>barplot()</code> — 범주별 수치 집계 (기본: 평균)</strong></p>
<pre><code class="language-python"># 등급별·성별 생존율 막대그래프
sns.barplot(data=titanic, x='class', y='survived', hue='sex')
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4f894ddd-a5f4-4358-b7ff-b0bacd7019f7/image.png" /></p>
<blockquote>
<p><code>countplot</code>은 행의 <strong>개수</strong>를, <code>barplot</code>은 수치 열의 <strong>평균(또는 집계값)</strong>을 시각화합니다.</p>
</blockquote>
<hr />
<h2 id="선그래프-line">선그래프 (Line)</h2>
<p>시간에 따른 추세를 표현할 때 사용합니다.</p>
<pre><code class="language-python">flights = sns.load_dataset('flights')

# 5월 항공 승객 수 추이
may_flights = flights.query(&quot;month == 'May'&quot;)
sns.lineplot(data=may_flights, x='year', y='passengers')
plt.show()

# 월별 색상 구분
sns.lineplot(data=flights, x='year', y='passengers', hue='month')
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/eafa9641-5715-4df3-b172-b550c1cb0273/image.png" /></p>
<hr />
<h2 id="히트맵-heatmap">히트맵 (Heatmap)</h2>
<p>2차원 행렬 데이터를 색상의 강도로 표현하는 그래프입니다. 상관관계 분석이나 피벗 테이블 시각화에 자주 사용됩니다.</p>
<p><strong>상관관계 히트맵</strong></p>
<pre><code class="language-python"># 수치형 열 간 상관계수 계산
titanic_corr = titanic[['survived', 'age', 'fare', 'sibsp', 'pclass']].corr()

sns.heatmap(data=titanic_corr,
            annot=True,       # 각 셀에 값 표시
            fmt='.2f',        # 소수점 2자리
            cmap='YlOrBr')    # 노랑→주황→갈색 컬러맵
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cd0bdcaa-17ca-4119-b755-9484f06641dd/image.png" /></p>
<p><strong>피벗 테이블 히트맵</strong></p>
<pre><code class="language-python"># 성별 × 등급별 생존율 피벗 테이블
titanic_pivot = pd.pivot_table(data=titanic,
                                index='sex',
                                columns='class',
                                values='survived',
                                aggfunc='mean')

sns.heatmap(data=titanic_pivot,
            annot=True,
            fmt='.2f',
            cmap='Purples')
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5a493404-e428-4eab-b789-a3da882a8481/image.png" /></p>
<blockquote>
<p><code>cmap</code>(컬러맵)은 값의 크기를 색상으로 표현하는 방식입니다. 단방향 데이터(0~1 범위 등)는 <code>YlOrBr</code>, <code>Blues</code>, <code>Purples</code>처럼 단색 계열을, 양방향 데이터(상관계수 등 음수 포함)는 <code>coolwarm</code>, <code>RdBu</code>처럼 두 색상이 대비되는 계열을 사용하는 것이 좋습니다.</p>
</blockquote>