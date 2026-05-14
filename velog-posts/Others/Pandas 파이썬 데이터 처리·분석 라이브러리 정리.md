<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c42d4352-3d1b-45b8-85e7-40ab359dd272/image.png" /></p>
<h2 id="목차">목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#pandas%EB%9E%80">Pandas란</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%84%A4%EC%B9%98-%EB%B0%8F-%EB%B6%88%EB%9F%AC%EC%98%A4%EA%B8%B0">설치 및 불러오기</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%9C%EB%A6%AC%EC%A6%88series">시리즈(Series)</a><ul>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%9C%EB%A6%AC%EC%A6%88-%EC%83%9D%EC%84%B1">시리즈 생성</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%9C%EB%A6%AC%EC%A6%88-%ED%99%95%EC%9D%B8">시리즈 확인</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%9C%EB%A6%AC%EC%A6%88-%EC%9D%B8%EB%8D%B1%EC%8A%A4-%EC%A7%80%EC%A0%95">시리즈 인덱스 지정</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%9C%EB%A6%AC%EC%A6%88-%EC%9D%B8%EB%8D%B1%EC%8B%B1">시리즈 인덱싱</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%9C%EB%A6%AC%EC%A6%88-%EC%8A%AC%EB%9D%BC%EC%9D%B4%EC%8B%B1">시리즈 슬라이싱</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%9C%EB%A6%AC%EC%A6%88-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%B1%EC%8B%A0%EC%B6%94%EA%B0%80%EC%82%AD%EC%A0%9C">시리즈 데이터 갱신·추가·삭제</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%94%95%EC%85%94%EB%84%88%EB%A6%AC%EB%A1%9C-%EC%8B%9C%EB%A6%AC%EC%A6%88-%EC%83%9D%EC%84%B1">딕셔너리로 시리즈 생성</a></li>
</ul>
</li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%84%EB%A0%88%EC%9E%84dataframe">데이터프레임(DataFrame)</a><ul>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%84%EB%A0%88%EC%9E%84-%EC%83%9D%EC%84%B1">데이터프레임 생성</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%84%EB%A0%88%EC%9E%84-%EA%B8%B0%EB%B3%B8-%EC%86%8D%EC%84%B1">데이터프레임 기본 속성</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%97%B4-%EC%84%A0%ED%83%9D%EC%B6%94%EA%B0%80%EC%82%AD%EC%A0%9C">열 선택·추가·삭제</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%9D%B8%EB%8D%B1%EC%8B%B1--loc--iloc">인덱싱 — loc / iloc</a></li>
<li><a href="https://api.velog.io/rss/@mommers#boolean-%EC%9D%B8%EB%8D%B1%EC%8B%B1">Boolean 인덱싱</a></li>
</ul>
</li>
<li><a href="https://api.velog.io/rss/@mommers#%EA%B2%B0%EC%B8%A1%EC%B9%98-%EB%8B%A4%EB%A3%A8%EA%B8%B0">결측치 다루기</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%9E%85%EC%B6%9C%EB%A0%A5">데이터 입출력</a></li>
</ul>
<hr />
<h2 id="pandas란">Pandas란</h2>
<p>Pandas는 계량 경제학 용어인 <strong>panel data</strong>와 <strong>analysis</strong>의 합성어입니다. 금융회사에 재직 중이던 Wes McKinney가 금융 데이터 분석을 위해 2008년 설계했으며, 현재는 데이터 과학 전반에서 가장 널리 쓰이는 라이브러리입니다.</p>
<p>Pandas의 핵심은 두 가지 자료구조입니다. 
<strong>Series</strong>는 1차원 배열에 인덱스를 붙인 구조이고, 
<strong>DataFrame</strong>은 엑셀 스프레드시트와 같은 2차원 표 형태의 구조입니다. 구조화된 데이터를 빠르고 다양한 형식으로 가공할 수 있는 풍부한 함수를 제공합니다.</p>
<blockquote>
<p>Pandas는 내부적으로 NumPy를 기반으로 동작합니다. NumPy가 수치 배열 연산에 집중한다면, Pandas는 그 위에서 고수준 데이터 분석 기능을 제공합니다.</p>
</blockquote>
<hr />
<h2 id="설치-및-불러오기">설치 및 불러오기</h2>
<pre><code class="language-python"># 설치
pip install pandas

# 불러오기 — pd라는 별칭(alias) 사용이 관례입니다
import pandas as pd
import numpy as np  # Pandas와 함께 자주 사용합니다</code></pre>
<hr />
<h2 id="시리즈series">시리즈(Series)</h2>
<p>Series는 1차원 데이터에 <strong>인덱스(index)</strong> 를 붙인 자료구조입니다. NumPy 배열과 달리 각 원소에 라벨을 지정할 수 있어 딕셔너리와 유사하게 동작합니다.</p>
<h3 id="시리즈-생성">시리즈 생성</h3>
<p>리스트를 <code>pd.Series()</code>에 넣으면 자동으로 0부터 시작하는 정수 인덱스가 부여됩니다.</p>
<pre><code class="language-python">obj = pd.Series([4, 5, -2, 8])
obj
# 출력:
# 0    4
# 1    5
# 2   -2
# 3    8
# dtype: int64</code></pre>
<h3 id="시리즈-확인">시리즈 확인</h3>
<table>
<thead>
<tr>
<th>속성/메서드</th>
<th>설명</th>
<th>예시 결과</th>
</tr>
</thead>
<tbody><tr>
<td><code>.values</code></td>
<td>값만 배열로 반환</td>
<td><code>array([ 4,  5, -2,  8])</code></td>
</tr>
<tr>
<td><code>.index</code></td>
<td>인덱스 반환</td>
<td><code>RangeIndex(start=0, stop=4, step=1)</code></td>
</tr>
<tr>
<td><code>.dtypes</code></td>
<td>데이터 타입 반환</td>
<td><code>dtype('int64')</code></td>
</tr>
</tbody></table>
<pre><code class="language-python">obj.values   # array([ 4,  5, -2,  8])
obj.index    # RangeIndex(start=0, stop=4, step=1)
obj.dtypes   # dtype('int64')</code></pre>
<h3 id="시리즈-인덱스-지정">시리즈 인덱스 지정</h3>
<p>생성 시 <code>index</code> 인수로 라벨을 직접 지정할 수 있습니다.</p>
<pre><code class="language-python">obj1 = pd.Series([5, 8, -1, 9], index=[&quot;a&quot;, &quot;b&quot;, &quot;c&quot;, &quot;d&quot;])
obj1
# 출력:
# a    5
# b    8
# c   -1
# d    9
# dtype: int64</code></pre>
<h3 id="시리즈-인덱싱">시리즈 인덱싱</h3>
<p>시리즈는 <strong>위치 기반 인덱싱(<code>iloc</code>)</strong> 과 <strong>라벨 기반 인덱싱(<code>loc</code>)</strong> 을 모두 지원합니다.</p>
<pre><code class="language-python">a = pd.Series([1024, 2048, 3096, 6192],
              index=[&quot;서울&quot;, &quot;부산&quot;, &quot;인천&quot;, &quot;대구&quot;])

a.iloc[1]       # 2048  — 위치(정수) 기반
a.loc[&quot;부산&quot;]   # 2048  — 라벨 기반</code></pre>
<p>여러 라벨을 리스트로 전달하면 원하는 순서로 데이터를 선택할 수 있습니다.</p>
<pre><code class="language-python">a[[&quot;서울&quot;, &quot;대구&quot;, &quot;부산&quot;]]
# 출력:
# 서울    1024
# 대구    6192
# 부산    2048
# dtype: int64</code></pre>
<blockquote>
<p><code>iloc</code>은 순서(정수)를 기준으로, <code>loc</code>은 라벨을 기준으로 인덱싱합니다. 이 구분은 DataFrame에서도 동일하게 적용됩니다.</p>
</blockquote>
<h3 id="시리즈-슬라이싱">시리즈 슬라이싱</h3>
<p>정수 인덱스로 슬라이싱할 때는 끝 인덱스가 <strong>포함되지 않고</strong>, 라벨로 슬라이싱할 때는 끝 라벨이 <strong>포함됩니다.</strong></p>
<pre><code class="language-python">a[1:3]            # 정수 슬라이싱 — 끝 미포함
# 부산    2048
# 인천    3096

a[&quot;부산&quot;:&quot;대구&quot;]   # 라벨 슬라이싱 — 끝 포함
# 부산    2048
# 인천    3096
# 대구    6192</code></pre>
<h3 id="시리즈-데이터-갱신·추가·삭제">시리즈 데이터 갱신·추가·삭제</h3>
<pre><code class="language-python"># 값 갱신 — 라벨로 지정
a[&quot;부산&quot;] = 1234

# 새 항목 추가 — 없는 라벨을 지정하면 추가됨
a[3] = 6543

# 항목 삭제
del a[&quot;서울&quot;]</code></pre>
<h3 id="딕셔너리로-시리즈-생성">딕셔너리로 시리즈 생성</h3>
<p>딕셔너리를 <code>pd.Series()</code>에 넣으면 키가 인덱스, 값이 데이터로 변환됩니다. <code>.name</code>과 <code>.index.name</code>으로 시리즈와 인덱스에 이름을 부여할 수 있습니다.</p>
<pre><code class="language-python">data = {&quot;Kim&quot;: 35000, &quot;Park&quot;: 67000, &quot;Joon&quot;: 12000, &quot;Choi&quot;: 4000}
obj2 = pd.Series(data)

obj2.name = &quot;Salary&quot;
obj2.index.name = &quot;Full Names&quot;

obj2
# 출력:
# Full Names
# Kim     35000
# Park    67000
# Joon    12000
# Choi     4000
# Name: Salary, dtype: int64</code></pre>
<hr />
<h2 id="데이터프레임dataframe">데이터프레임(DataFrame)</h2>
<p>DataFrame은 Series가 여러 개 묶인 2차원 표 형태의 자료구조입니다. 행 인덱스(row index)와 열 인덱스(column index)를 모두 가지며, 엑셀 스프레드시트와 가장 유사한 구조입니다.</p>
<h3 id="데이터프레임-생성">데이터프레임 생성</h3>
<p><strong>방법 1 — 딕셔너리로 생성</strong></p>
<p>딕셔너리의 각 키가 열 이름이 되고, 값(리스트)이 열 데이터가 됩니다.</p>
<pre><code class="language-python">data = {
    &quot;name&quot;  : [&quot;Choi&quot;, &quot;Choi&quot;, &quot;Choi&quot;, &quot;Kim&quot;, &quot;Park&quot;],
    &quot;year&quot;  : [2013, 2014, 2015, 2016, 2017],
    &quot;points&quot;: [1.5, 1.7, 3.6, 2.4, 2.9]
}
df = pd.DataFrame(data)
df
# 출력:
#    name  year  points
# 0  Choi  2013     1.5
# 1  Choi  2014     1.7
# 2  Choi  2015     3.6
# 3   Kim  2016     2.4
# 4  Park  2017     2.9</code></pre>
<p><code>columns</code>와 <code>index</code> 인수로 열 순서와 행 라벨을 지정할 수 있습니다. 데이터에 없는 열을 <code>columns</code>에 추가하면 해당 열은 <code>NaN</code>으로 채워집니다.</p>
<pre><code class="language-python">df = pd.DataFrame(data,
                  columns=[&quot;year&quot;, &quot;name&quot;, &quot;points&quot;, &quot;penalty&quot;],
                  index=[&quot;one&quot;, &quot;two&quot;, &quot;three&quot;, &quot;four&quot;, &quot;five&quot;])
df
# 출력:
#        year  name  points penalty
# one    2013  Choi     1.5     NaN
# two    2014  Choi     1.7     NaN
# ...</code></pre>
<p><strong>방법 2 — NumPy 배열로 생성</strong></p>
<pre><code class="language-python">df0 = pd.DataFrame(np.arange(12).reshape(3, 4))
# 열과 행 인덱스가 자동으로 정수로 부여됩니다</code></pre>
<h3 id="데이터프레임-기본-속성">데이터프레임 기본 속성</h3>
<pre><code class="language-python">df.index    # RangeIndex(start=0, stop=5, step=1) — 행 인덱스
df.columns  # Index(['name', 'year', 'points'], ...) — 열 인덱스
df.values   # 2차원 numpy array 형태로 반환

df.index.name   = &quot;Order&quot;   # 행 인덱스에 이름 부여
df.columns.name = &quot;Info&quot;    # 열 인덱스에 이름 부여</code></pre>
<p><strong>전치(Transpose)</strong></p>
<pre><code class="language-python">df.T  # 행과 열을 바꿉니다</code></pre>
<h3 id="열-선택·추가·삭제">열 선택·추가·삭제</h3>
<p><strong>열 선택</strong></p>
<pre><code class="language-python">df[&quot;year&quot;]           # 단일 열 → Series 반환
df[[&quot;year&quot;, &quot;name&quot;]] # 여러 열 → DataFrame 반환
df.year              # 속성 방식 (열 이름이 파이썬 식별자일 때만 사용 가능)</code></pre>
<p><strong>열 추가 및 갱신</strong></p>
<pre><code class="language-python"># 스칼라 값으로 전체 열 채우기
df[&quot;penalty&quot;] = 0.5

# 리스트로 행별 값 지정
df[&quot;penalty&quot;] = [0.1, 0.2, 0.3, 0.4, 0.5]

# NumPy 배열로 열 추가
df[&quot;zeros&quot;] = np.arange(5)

# 기존 열 계산으로 새 열 추가
df[&quot;net_points&quot;] = df[&quot;points&quot;] - df[&quot;penalty&quot;]

# 조건식으로 불리언 열 추가
df[&quot;high_points&quot;] = df[&quot;net_points&quot;] &gt; 2.0</code></pre>
<blockquote>
<p>Series를 열로 추가할 때, Series의 인덱스와 DataFrame의 인덱스가 일치하는 행에만 값이 채워지고 나머지는 <code>NaN</code>이 됩니다.</p>
</blockquote>
<pre><code class="language-python"># 인덱스가 일치하는 행에만 값이 들어가고, 나머지는 NaN
val = pd.Series([-1.2, -1.5, -1.7], index=[&quot;two&quot;, &quot;four&quot;, &quot;five&quot;])
df[&quot;debt&quot;] = val</code></pre>
<p><strong>열 삭제</strong></p>
<pre><code class="language-python">del df[&quot;high_points&quot;]          # del 키워드로 삭제
df.drop(&quot;F&quot;, axis=1)           # drop 메서드로 삭제 (axis=1: 열 방향)
df.drop(&quot;F&quot;, axis=1, inplace=True)  # inplace=True로 원본에 바로 반영</code></pre>
<h3 id="인덱싱--loc--iloc">인덱싱 — loc / iloc</h3>
<p>DataFrame의 고급 인덱싱은 <code>loc</code>과 <code>iloc</code> 두 가지 방식을 사용합니다.</p>
<p><strong><code>loc</code> — 라벨 기반 인덱싱</strong></p>
<pre><code class="language-python">df.loc[&quot;two&quot;]                    # &quot;two&quot; 행 전체 → Series
df.loc[&quot;two&quot;:&quot;four&quot;]             # &quot;two&quot;~&quot;four&quot; 행 슬라이싱 → 끝 포함
df.loc[&quot;two&quot;:&quot;four&quot;, &quot;points&quot;]   # 행 범위 + 특정 열
df.loc[:, &quot;year&quot;]                # 전체 행의 &quot;year&quot; 열
df.loc[&quot;three&quot;:&quot;five&quot;, &quot;year&quot;:&quot;penalty&quot;]  # 행·열 범위 동시 지정
df.loc[df.year &gt; 2015]           # 조건식으로 행 필터링

# 새 행 추가
df.loc[&quot;six&quot;, :] = [2013, &quot;Jun&quot;, 4.0, 0.1]</code></pre>
<p><strong><code>iloc</code> — 위치(정수) 기반 인덱싱</strong></p>
<pre><code class="language-python">df.iloc[3]           # 3번째 행 → Series
df.iloc[3:5, 0:2]    # 3~4행, 0~1열 슬라이싱
df.iloc[[0,1,3], [1,2]]  # 특정 행·열 리스트 지정
df.iloc[:, 1:4]      # 전체 행, 1~3열
df.iloc[1, 1]        # 단일 원소 접근</code></pre>
<table>
<thead>
<tr>
<th>구분</th>
<th>loc</th>
<th>iloc</th>
</tr>
</thead>
<tbody><tr>
<td>기준</td>
<td>라벨</td>
<td>정수 위치</td>
</tr>
<tr>
<td>슬라이싱 끝</td>
<td>포함</td>
<td>미포함</td>
</tr>
<tr>
<td>사용 시점</td>
<td>라벨을 알 때</td>
<td>순서를 알 때</td>
</tr>
</tbody></table>
<h3 id="boolean-인덱싱">Boolean 인덱싱</h3>
<p>조건식을 <code>loc</code>과 함께 사용하면 조건을 만족하는 행만 필터링할 수 있습니다.</p>
<pre><code class="language-python"># name이 &quot;Choi&quot;인 행의 name, points 열만 선택
df.loc[df[&quot;name&quot;] == &quot;Choi&quot;, [&quot;name&quot;, &quot;points&quot;]]

# points가 2 초과 3 미만인 행 전체 선택
df.loc[(df[&quot;points&quot;] &gt; 2) &amp; (df[&quot;points&quot;] &lt; 3), :]</code></pre>
<blockquote>
<p><code>&amp;</code>(AND), <code>|</code>(OR) 연산자를 사용할 때는 각 조건을 반드시 괄호로 감싸야 합니다.</p>
</blockquote>
<hr />
<h2 id="결측치-다루기">결측치 다루기</h2>
<p>실제 데이터에는 누락된 값이 존재하는 경우가 종종 있습니다. Pandas는 이를 <code>nan</code>(Not a Number)으로 표현하며, 처리하는 방법은 크게 세 가지입니다.</p>
<p><strong><code>dropna()</code> — NaN이 있는 행/열 제거</strong></p>
<pre><code class="language-python">df.dropna(how=&quot;all&quot;)   # 행의 모든 값이 NaN인 경우에만 제거
df.dropna(how=&quot;any&quot;)   # 행에 NaN이 하나라도 있으면 제거</code></pre>
<p><strong><code>fillna()</code> — NaN을 특정 값으로 채우기</strong></p>
<pre><code class="language-python">df.fillna(value=0.5)   # NaN을 0.5로 채움
df.fillna(method=&quot;ffill&quot;)  # 앞의 값으로 채우기 (forward fill)</code></pre>
<p><strong><code>isna()</code> / <code>notna()</code> — NaN 여부 확인</strong></p>
<pre><code class="language-python">df.isna()    # NaN이면 True, 아니면 False인 DataFrame 반환
df.notna()   # 반대</code></pre>
<blockquote>
<p>결측치 처리는 데이터 전처리의 핵심입니다. 무조건 제거하기보다 데이터의 맥락에 맞게 채울지 제거할지 판단하는 것이 중요합니다.</p>
</blockquote>
<hr />
<h2 id="데이터-입출력">데이터 입출력</h2>
<p>Pandas는 CSV, Excel, JSON, SQL 등 다양한 형식의 파일을 읽고 쓸 수 있습니다.</p>
<p><strong>CSV 파일 읽기 — <code>read_csv()</code></strong></p>
<pre><code class="language-python"># 기본 읽기
pd.read_csv(&quot;sample.csv&quot;)

# 열 이름 직접 지정 (헤더가 없는 파일)
pd.read_csv(&quot;sample.csv&quot;, names=[&quot;c1&quot;, &quot;c2&quot;, &quot;c3&quot;])

# 특정 열을 행 인덱스로 지정
pd.read_csv(&quot;sample1.csv&quot;, index_col=&quot;c1&quot;)</code></pre>
<p><strong>CSV 파일 저장 — <code>to_csv()</code></strong></p>
<pre><code class="language-python">df.to_csv(&quot;output.csv&quot;)                              # 기본 저장
df.to_csv(&quot;output.csv&quot;, sep=&quot;,&quot;, index=False, header=False)
# index=False: 행 인덱스 미포함
# header=False: 열 이름 미포함</code></pre>
<p><strong>주요 입출력 함수 정리</strong></p>
<table>
<thead>
<tr>
<th>형식</th>
<th>읽기</th>
<th>쓰기</th>
</tr>
</thead>
<tbody><tr>
<td>CSV</td>
<td><code>pd.read_csv()</code></td>
<td><code>df.to_csv()</code></td>
</tr>
<tr>
<td>Excel</td>
<td><code>pd.read_excel()</code></td>
<td><code>df.to_excel()</code></td>
</tr>
<tr>
<td>JSON</td>
<td><code>pd.read_json()</code></td>
<td><code>df.to_json()</code></td>
</tr>
<tr>
<td>SQL</td>
<td><code>pd.read_sql()</code></td>
<td><code>df.to_sql()</code></td>
</tr>
</tbody></table>