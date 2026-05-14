<h2 id="목차">목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B6%84%EC%84%9D-%EB%AA%A9%EC%A0%81">분석 목적</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8D%B0%EC%9D%B4%ED%84%B0-%EB%B6%88%EB%9F%AC%EC%98%A4%EA%B8%B0-%EB%B0%8F-%ED%83%90%EC%83%89">데이터 불러오기 및 탐색</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%A0%84%EC%B2%98%EB%A6%AC">데이터 전처리</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B6%84%EC%84%9D-%EB%8B%A8%EA%B3%84">분석 단계</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%9C%EA%B0%81%ED%99%94">시각화</a></li>
</ul>
<hr />
<h2 id="분석-목적">분석 목적</h2>
<p>서울시 각 구별로 2018년 한 해 동안 <strong>미세먼지(PM10) 지수가 70 이상인 날(나쁨 일수)이 몇 일인지</strong> 파악하고, 가장 많은 구를 찾는 것이 목표입니다.</p>
<p>분석 흐름은 아래와 같습니다.</p>
<blockquote>
<p><strong>데이터 수집 → 전처리 → groupby 집계 → 정렬 → 시각화</strong></p>
</blockquote>
<hr />
<h2 id="데이터-불러오기-및-탐색">데이터 불러오기 및 탐색</h2>
<p>사용 데이터는 에어코리아에서 제공하는 서울시 대기 측정 데이터(<code>2018_PM.xlsx</code>)입니다. 컬럼 구성은 지역, 측정소코드, 측정소명, 측정일시, SO2, CO, O3, NO2, PM10, PM25, 주소입니다.</p>
<pre><code class="language-python">import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 한글 폰트 적용

# 엑셀 파일 불러오기
df = pd.read_excel(&quot;2018_PM.xlsx&quot;)

df.head()     # 상위 5개 확인
df.tail(10)   # 하위 10개 확인
df.shape      # 전체 데이터 크기
df.info()     # 컬럼별 타입·결측치 개수 요약</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0f04e5ad-b32d-46e7-acfa-e7571a6e6cf5/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/da7f8016-b393-49da-9265-044d3c0f3e86/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bf8e3195-7ac3-4a73-a9cf-5e1835fc14f2/image.png" /></p>
<hr />
<h2 id="데이터-전처리">데이터 전처리</h2>
<h3 id="필요한-컬럼만-추출">필요한 컬럼만 추출</h3>
<p>분석에 필요한 컬럼은 <code>지역</code>, <code>측정일시</code>, <code>PM10</code> 세 가지입니다. 불필요한 컬럼을 제거하는 방법은 두 가지입니다.</p>
<pre><code class="language-python"># 방법 1 — 필요한 컬럼만 선택 (권장)
df1 = df[[&quot;지역&quot;, &quot;측정일시&quot;, &quot;PM10&quot;]].copy()

# 방법 2 — 불필요한 컬럼 삭제
# df1 = df.drop(columns=[&quot;측정소코드&quot;,&quot;측정소명&quot;,&quot;SO2&quot;,&quot;CO&quot;,&quot;O3&quot;,&quot;NO2&quot;,&quot;PM25&quot;,&quot;주소&quot;])</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/41df0492-8774-459b-8e7a-ba65b38329d2/image.png" /></p>
<h3 id="결측치-처리">결측치 처리</h3>
<pre><code class="language-python"># 결측치 개수 확인
df1.isnull().sum()

# PM10 평균값으로 결측치 채우기
PM10_mean = df1[&quot;PM10&quot;].mean()
df1[&quot;PM10&quot;] = df1[&quot;PM10&quot;].fillna(PM10_mean)

# 결측치 제거 확인
df1.isnull().sum()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3a33fa61-fa74-4af0-a282-471ab13d6874/image.png" /></p>
<blockquote>
<p>결측치를 삭제하면 해당 일자·지역 데이터 자체가 사라집니다. 이 분석에서는 전체 평균으로 채워 데이터 손실을 최소화했습니다.</p>
</blockquote>
<hr />
<h2 id="분석-단계">분석 단계</h2>
<h3 id="astype--데이터-타입-변환">astype() — 데이터 타입 변환</h3>
<p>측정일시 컬럼은 정수형으로 저장되어 있습니다. 날짜 기준으로 그룹화하려면 <strong>문자열로 변환 후 날짜(8자리)만 잘라내야</strong> 합니다.</p>
<pre><code class="language-python">df1.info()  # 측정일시가 int64 타입임을 확인

# 문자열로 변환 후 연월일 8자리만 추출
# 예: 2018010101 → &quot;20180101&quot;
df1[&quot;측정일시&quot;] = df1[&quot;측정일시&quot;].astype(&quot;str&quot;)
df1[&quot;측정일시&quot;] = df1[&quot;측정일시&quot;].str[0:8]</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/323750b0-c957-4a9d-aa2e-83a84bae7a52/image.png" /></p>
<h3 id="groupby--지역·일자별-최댓값-집계">groupby() — 지역·일자별 최댓값 집계</h3>
<p>하루에 같은 지역에서 측정한 값이 여러 개 존재합니다. 일자와 지역을 기준으로 그룹화하여 <strong>하루 최대 PM10 값</strong>을 구합니다.</p>
<pre><code class="language-python"># 측정일시·지역 기준으로 PM10 최댓값 집계
df2 = df1.groupby([&quot;측정일시&quot;, &quot;지역&quot;])[&quot;PM10&quot;].max()
df2.head(40)</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/38b89c9c-b7d6-4808-8b1a-ae85750dde02/image.png" /></p>
<h3 id="나쁨-일수-추출-및-지역별-합계">나쁨 일수 추출 및 지역별 합계</h3>
<p>PM10이 70 이상인 날은 <code>True</code>, 미만인 날은 <code>False</code>로 표시됩니다. <code>True</code>는 합산 시 1로 계산되므로 지역별 합계가 곧 나쁨 일수가 됩니다.</p>
<pre><code class="language-python"># PM10 &gt;= 70인 날 추출 (True/False 시리즈)
df3 = (df2 &gt;= 70)

# 지역별로 True 합계 = 나쁨 일수
result = df3.groupby(level=&quot;지역&quot;).sum()

# 내림차순 정렬
result_sort = result.sort_values(ascending=False)
result_sort</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f51edc89-2f18-4ba6-8388-53161974a85c/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/165cf57a-6a3b-43a7-9eb0-f23e5883a1a4/image.png" /></p>
<blockquote>
<p><code>groupby(level=&quot;지역&quot;)</code>에서 <code>level=</code> 인수는 MultiIndex(측정일시·지역 두 기준)에서 특정 레벨 기준으로 다시 집계할 때 사용합니다.</p>
</blockquote>
<hr />
<h2 id="시각화">시각화</h2>
<p>세 가지 방법으로 동일한 결과를 시각화합니다.</p>
<h3 id="방법-1--pandas-내장-plot">방법 1 — Pandas 내장 plot</h3>
<pre><code class="language-python">result_sort.plot(kind=&quot;barh&quot;, figsize=(7, 10))
plt.title(&quot;각 지역별 미세먼지 PM10 지수가 70이상인 나쁨 일수&quot;)
plt.xlabel(&quot;미세먼지 나쁨 일수&quot;)
plt.ylabel(&quot;지역&quot;)
plt.grid(True)
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3a367416-3a6c-47db-8911-8d54f741297e/image.png" /></p>
<h3 id="방법-2--matplotlib">방법 2 — Matplotlib</h3>
<pre><code class="language-python">plt.figure(figsize=(7, 10))
plt.barh(result_sort.index, result_sort.values)
plt.title(&quot;각 지역별 미세먼지 PM10 지수가 70이상인 나쁨 일수&quot;)
plt.xlabel(&quot;미세먼지 나쁨 일수&quot;)
plt.ylabel(&quot;지역&quot;)
plt.grid(True)
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1503960d-9ed8-4e19-bac4-6838c09145ad/image.png" /></p>
<h3 id="방법-3--seaborn">방법 3 — Seaborn</h3>
<pre><code class="language-python">import seaborn as sns

plt.figure(figsize=(7, 10))
sns.barplot(x=result_sort.values, y=result_sort.index, orient=&quot;h&quot;)
plt.title(&quot;각 지역별 미세먼지 PM10 지수가 70이상인 나쁨 일수&quot;)
plt.xlabel(&quot;미세먼지 나쁨 일수&quot;)
plt.ylabel(&quot;지역&quot;)
plt.grid(True)
plt.show()</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/50566683-9cec-427b-9214-b2fe23472ce5/image.png" /></p>
<p><strong>시각화 방법 비교</strong></p>
<table>
<thead>
<tr>
<th>방법</th>
<th>특징</th>
</tr>
</thead>
<tbody><tr>
<td><code>df.plot()</code></td>
<td>코드 가장 간결, 추가 임포트 불필요</td>
</tr>
<tr>
<td><code>matplotlib</code></td>
<td>세밀한 커스터마이징 가능</td>
</tr>
<tr>
<td><code>seaborn</code></td>
<td>기본 스타일이 깔끔, 추가 옵션 풍부</td>
</tr>
</tbody></table>
<blockquote>
<p>세 방법 모두 동일한 결과를 출력합니다. 간단한 확인용이라면 <code>df.plot()</code>을, 발표용 고품질 그래프가 필요하다면 <code>seaborn</code>을 활용하는 것이 좋습니다.</p>
</blockquote>