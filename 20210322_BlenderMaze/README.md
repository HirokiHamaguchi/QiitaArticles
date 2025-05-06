# 概要

このようなゲームを作りました。基本的には迷路のゲームです。

[サイトのリンク](https://unityroom.com/games/hari_kagiyanomusume_maze)

![messageImage_1616335316395.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/9dedcf39-e999-9d9e-72a2-b48d81aa46c3.jpeg)
![messageImage_1616335318339.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/fa439106-1c26-d2cb-16d1-ea413bc7557e.jpeg)

本記事ではこのゲームの製作過程を掲載すると共に、きっと有益にな情報をまとめます。楽しんで頂けたら幸いです。

## Step0 前提

まず用語を整理します。

* **Blender** : 3DCG制作ソフト。Pythonによって操作が可能になっています。
* **Python** : 言わずと知れた有名プログラミング言語。
* **Unity** : ゲーム制作ソフト。スタート画面の表示やゲームオーバーの判定などをしてくれます。言語はC#です。

大まかな流れとしては、

* **Step1.** Blenderで3Dオブジェクトを作成
* **Step2.** Pythonでそれを迷路に組み立てる
* **Step3.** Unityでゲームとして完成させる

という風になっています。

コードに関しては、読みやすさも考え記事中においては一部抜粋に留めています。もし全体のコードを知りたい場合はプルダウン内をご覧ください。そこに掲載してあります。

さて、記事本編に入る前に少しだけ前置きを。そもそも私がこの迷路を作ろうと思ったのは、昨年の夏頃にエッシャーの相対性という作品を3Dで作成したことがきっかけです。このような世界観に似たものを独自に作ろうと思ったのが前提としてあります。

![イラスト.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/b72e5491-e928-8a6f-062d-91463177c001.jpeg)

本ゲームが、重力があいまいで、階段や橋などで各所が連結され、色がモノクロに統一されているなどといった特徴を有しているのは、そういった事情からとなっています。

## Step1 3Dオブジェクトの作成

まず最初に大枠として、球を内に含む立方体のようなものを作成します。
このコードを実行すると、

![messageImage_1615002419349.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/3d25af0f-8211-7900-6c14-c9030247f612.jpeg)

このように、

![messageImage_1615002384682.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/ca0c9c88-4056-cb76-18b7-89822181bb0a.jpeg)

球に従った形が出来ます。(上図は立面図です)この中をプレイヤーに動いてもらうことで迷路にしようという考えです。

ただ、これだけでは機械的すぎるので、randomから**正規分布**に従ったランダムさを生成してくれる**random.normalvariate**を使用して、有機的にします。

```python
#各直方体(島)の高さに平均0、標準偏差(σ)1のランダムさを与える
height=[[height[Y][X]+round(random.normalvariate(0,1)) for X in range(num_of_blocks)] for Y in range(num_of_blocks)]
```

この処理をすると、
![messageImage_1615021893993.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/c568a706-c0bf-58af-4cb1-b2a6c07a75e5.jpeg)
ランダムさが出てきてそれらしさが増します。

そしてこの各島の間を移動してもらうために橋や階段を掛けていきます。
具体的には、隣り合う島同士の高さの差が、

* 0m違いならば、橋を
* 1m違いならば、階段を
* 2m違いならば、スロープを

かける、と言う風にしています。
![messageImage_1616316465448.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/50b8ac11-3e78-c918-4b64-b598b9b89f9d.jpeg "プレハブ一覧")

作業途中はこんな感じで、プロトタイプ感あふれています。
![messageImage_1615109316907.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/c442418a-3851-f73f-5ac4-2dfa0956836c.jpeg)

## Step2 Pythonで経路探索

Step1で完成したものの一部を上から見た、以下の図をご覧ください。
![messageImage_1616329932271.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/826c21c0-a543-20e3-e93d-d8e989fe7711.jpeg "繋がっていない迷路")

……。よーく見ると、全然繋がっていないですね。基本的に中央の島から出発して四隅のいずれかに行ってもらう予定だったのですが、これではどこにも行けません。そもそも中央の直方体が絶海の孤島です。ここをスタートにしては一歩すら無理です。
それもそのはず、これではまだ高さの情報をもとに適当に橋などを繋いだにすぎません。これではダメダメです。

そもそも、迷路作成と言えば、**棒倒し法**、**穴掘り法**、**壁伸ばし法**などが有名なのですが(これらの方法が分かりやすく解説されたサイトのリンクを記事最後に貼っています。興味があれば是非)、これらの方法は前提としてスタートからゴールまで行ける事を保証しています。

ただ、今回は既に経路を作成してしまっていて、実際にゴールできるかの保証はどこにもありません。

そこで、ランダムかつ大量に経路を作成した上で、ゴールできるかを経路探索し、可能ならばそれを採用するという方針で行きます。

### Dijkstra法とは

今回はDijkstra(ダイクストラ)法と言う方法を用いてその判定を行いました。(最終的にはその情報を利用しなかったのですが)スタートからゴールまでの最短経路も合わせて算出しようと思い、この方法を採用しました。

[Dijkstra法](https://ja.wikipedia.org/wiki/%E3%83%80%E3%82%A4%E3%82%AF%E3%82%B9%E3%83%88%E3%83%A9%E6%B3%95)というのは最短経路問題を解くためのアルゴリズムで、競技プログラミングなどで比較的よく出てきます。

このアルゴリズムは、一般的には優先度付きキュー(heapq)などを用いて実装するのですが、Pythonの場合**scipy**というライブラリを使うと簡単にDijkstra法を実行してくれます。

### scipyのDijkstra法を走らせてみる

それでは実際に走らせてみましょう。(scipyに関するより詳しい説明は[scipyの公式ドキュメント](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html)や[nkmkさんによるサイト](https://note.nkmk.me/python-scipy-shortest-path/)をご覧ください。)
二次元行列をそのまま渡すことは出来ないので、それぞれの島に対してindex_for_dijkstraという関数で番号を割り振った上で、実行していきます。

```python
row_np=np.array(row)
col_np=np.array(col)
data_np=np.array(data)
graph=csr_matrix((data_np, (row_np, col_np)), shape=(num_of_blocks**2, num_of_blocks**2)).toarray()
distance=dijkstra(graph, directed=False, indices=[index_for_dijkstra(x,y) for x,y in [(0,0),(0,num_of_blocks-1),(num_of_blocks-1,0),(num_of_blocks-1,num_of_blocks-1)]])
```

実行結果(の一部)がこちらです。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/c911faec-014c-1caa-5c9a-c32f360ebddc.png)
infとは無限大、つまり到達不可能であることを示しています。下のケース(左下の島からの最短経路距離を示したもの)はinfだらけなので、孤立していることが分かります。
一方、上のケース(左上の島からの最短経路距離を示したもの)は、数字が多く書き込まれています。これは橋や階段に対して事前に与えた移動距離の総和を示していると共に、「**数字が書き込まれいる⇔到達可能である**」ということも示しています。

これを使えば、生成された迷路がゲームに適しているか分かりますね! 今回は四隅から中央地点までの距離が全てinfでない、つまり到達可能であるならば合格としました。

### 最終的な実行

この条件をもとに試行を繰り返していきます。
ループが1000回を超えて試行されたケースはありませんでした。体感ですが長くて5秒で一個の迷路が完成していきます。
![messageImage_1616204002984.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/b3bf4baa-3fa0-0239-a515-ffb6256bf5e2.jpeg)

出来上がったものがこちらです。
![messageImage_1616329933963.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/5253e29b-dbd8-aee7-a457-fb22bf55efe6.jpeg)

……。全部つながっていますね! それもいい感じに! 万歳!
これで程よくプレイヤーが迷ってくれそうな迷路が完成しました。さらにコードは完成しているので、大量生産もお手軽です。

(ただ、公平な情報発信の為に記しておくと、この方法はあまりお勧めできるものではありません。何故ならば条件を満たす迷路が必ず生成されるという理論的保証がないからです。この方法が5秒(実質的にはBlenderの処理がメインなので1秒以下)で迷路を作れているのは、橋や階段がある程度の数かかっているという前提が必要です。もしもその数が少なければ計算は10分経っても終わることはないでしょう。製作方法としては**先述の穴掘り法などの方が遥かに優秀です**。)

以上がStep2でした。

### Step1,2のおまけ

二つに分けています。どちらもそこそこ長いです。

<details><summary>最終的に使用したコード全文</summary><div>

一応注意書きですが、このコードをそのまま実行してもエラーしか出ません。理由は三つあり、一つ目がパス名(偽名入れてますし、私の場合のパス名です)、二つ目がimport scipy(理由はおまけに)、そして三つ目がコレクションの存在を前提としていることです。具体的に言うとScene Collection直下のDONT DELETEという名前のコレクション、そしてそれに属するBRIDGE,DIAGONAL STAIRS,SLOPE,STAIRS,TREASURE CHESTという五つのオブジェクトの存在が前提です。またデバッグに用いたprint文なども、消すべきかもしれませんが作業の上ではかなり本質な要素だったのであえてそのままにしています。そしてbpyはBlenderをscriptから操作する上でのAPIとなっています。これらの点を頭に入れながらお読み下さい。

```python
import bpy
import math
import random
import datetime
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path,dijkstra
print("----------------------------------------------------------------------")

#数値決め
#今回は試行錯誤が出来る様、やや過剰に数値に名前を与えています。 pep-8破っているところも多いですが、多めに見て頂ければ……
num_of_blocks=9 #奇数
num_of_height_variation=6+0 #0を元々の高さとしてこの数分だけマイナスの差分がある
cuboid_sidelength=3 #直方体の短い方の一辺の長さ
foundation_height=60 #>=max(2*negative_length)
HEIGHT_OF_EACH_STEP=4 #直方体同士のデフォルトの高さの差 固定値
scale_factor=region=9 #直方体同士の間隔に等しい ≒math.sqrt(2)*HEIGHT_OF_EACH_STEP*num_of_height_variation/(num_of_blocks*(math.sqrt(2)-1))
#print(math.sqrt(2)*HEIGHT_OF_EACH_STEP*num_of_height_variation/(num_of_blocks*(math.sqrt(2)-1)))
entire_cube_sidelength=region*num_of_blocks #球に内接する立方体の一辺の長さ
entire_sphere_radius=entire_cube_sidelength*math.sqrt(3/4) #直方体たちが形成する球の半径
last_adjustment=2 #計算をミスってしまっていたので、最後の調整用の数値です。
isfinal=True

########################################################################

def func_z(X,Y): #XYはマス目の番号 (X:-(num_of_blocks-1)//2～+(num_of_blocks-1)//2 Y:-(num_of_blocks-1)//2～+(num_of_blocks-1)//2)
    x=abs(X)+0.5 #xyは使用する座標の絶対値
    y=abs(Y)+0.5
    initial_height=math.sqrt(num_of_blocks**2-x**2-y**2)-num_of_blocks/math.sqrt(2)
    negative_height=math.floor((num_of_height_variation/(num_of_blocks-num_of_blocks/math.sqrt(2)-0.1))*initial_height)*last_adjustment
    individual_height=foundation_height-HEIGHT_OF_EACH_STEP*negative_height//last_adjustment #土台を用意し、negative分だけ削る
    return individual_height
def isinside(x,y): #list index out of range避け
    return True if (0<=x<num_of_blocks) and (0<=y<num_of_blocks) else False
def index_for_dijkstra(x,y):
    index=x+y*num_of_blocks
    return index
def reverse_index_for_dijkstra(index,is_for_direction=False):
    x=index%num_of_blocks
    y=index//num_of_blocks
    if is_for_direction:
        x=(x if x!=num_of_blocks-1 else -1) 
        y=(index-x)//num_of_blocks
    return (x,y)

is_good_maze=False

for highest_counter in range(1000 if isfinal else 1):
    #球に従うように各直方体の高さを仮置きする
    height=[[func_z(X,Y) for X in range(-(num_of_blocks-1)//2,(num_of_blocks-1)//2+1)] for Y in range(-(num_of_blocks-1)//2,(num_of_blocks-1)//2+1)]

    #各直方体の高さに平均0、標準偏差(σ)1のランダムさ(*last_adjustment)を与える
    special_cells=[(0,0),(0,num_of_blocks-1),(num_of_blocks-1,0),(num_of_blocks-1,num_of_blocks-1),((num_of_blocks-1)//2,(num_of_blocks-1)//2)]
    height=[[height[Y][X] if (X,Y) in special_cells else height[Y][X]+round(random.normalvariate(0,1))*last_adjustment for X in range(num_of_blocks)] for Y in range(num_of_blocks)]

    #角に隣接する直方体について、高さが1*last_adjustmentの差分しかないようにする（つまり、ゴールしやすくする）
    for X,Y in special_cells[:4]:
        if height[Y][1 if X==0 else (num_of_blocks-1)-1]!=foundation_height-1*last_adjustment and height[1 if Y==0 else (num_of_blocks-1)-1][X]!=foundation_height-1*last_adjustment:
            height[Y][1 if X==0 else (num_of_blocks-1)-1]=foundation_height-1*last_adjustment

    row=[] #dijkstra用の辺の情報を表すリスト
    col=[]
    data=[]

    #橋や階段などのオブジェクトを3次元空間上にどう配置するかのデータを定める
    #ここから先4回同じ構造のコードが続きます。関数とか定義すれば良かったのですが、
    #それぞれの相違を反映させるのが少し面倒なのでこうしました。
    deleting_rate=0.3
    
    dif0=[]#BRIDGE
    dif0_deleted=0
    for X in range(num_of_blocks):
        for Y in range(num_of_blocks):
            for x,y,angle in [(1,0,0),(0,1,-math.pi/2)]: #rotationより、DONT DELETE内のオブジェクトは全てx軸正方向を向くことが要請される
                if isinside(X+x,Y+y) and height[Y+y][X+x]==height[Y][X]:
                    if (num_of_blocks//3<=X<2*num_of_blocks//3) and (num_of_blocks//3<=Y<2*num_of_blocks//3) and random.random()<deleting_rate:
                        dif0_deleted+=1
                        continue
                    dif0.append((-(num_of_blocks-1)//2+X+x/2,-(num_of_blocks-1)//2+Y+y/2,height[Y][X],angle))
                    row.append(index_for_dijkstra(X,Y))
                    col.append(index_for_dijkstra(X+x,Y+y))
                    data.append(600) #辺の重み(つまり移動コスト) 長さをcm単位で計測しました
    dif0=[(x*scale_factor,y*scale_factor,z,-angle) for x,y,z,angle in dif0] #angleにマイナスが付いている理由はおまけで。角度関連はかなり苦肉の策が多いです。

    dif1=[]#STAIRS
    dif1_deleted=0
    for X in range(num_of_blocks):
        for Y in range(num_of_blocks):
            for x,y,angle in [(1,0,0),(0,1,-math.pi/2)]:
                if isinside(X+x,Y+y) and height[Y+y][X+x]-height[Y][X]==1*last_adjustment:
                    if (num_of_blocks//3<=X<2*num_of_blocks//3) and (num_of_blocks//3<=Y<2*num_of_blocks//3) and random.random()<deleting_rate:
                        dif1_deleted+=1
                        continue
                    dif1.append((-(num_of_blocks-1)//2+X+x/2,-(num_of_blocks-1)//2+Y+y/2,(height[Y+y][X+x]+height[Y][X])/2,angle))
                    row.append(index_for_dijkstra(X,Y))
                    col.append(index_for_dijkstra(X+x,Y+y))
                    data.append(683)
                elif isinside(X+x,Y+y) and height[Y+y][X+x]-height[Y][X]==-1*last_adjustment:
                    dif1.append((-(num_of_blocks-1)//2+X+x/2,-(num_of_blocks-1)//2+Y+y/2,(height[Y+y][X+x]+height[Y][X])/2,angle+math.pi))
                    row.append(index_for_dijkstra(X,Y))
                    col.append(index_for_dijkstra(X+x,Y+y))
                    data.append(683)
    dif1=[(x*scale_factor,y*scale_factor,z,-angle) for x,y,z,angle in dif1]

    dif1_diag=[]#DIAGONAL STAIRS
    for X in range(num_of_blocks):
        for Y in range(num_of_blocks):
            for x,y,angle in [(1,1,-math.pi/4),(1,-1,math.pi/4)]:
                if ((num_of_blocks-1)//2,(num_of_blocks-1)//2) in ((X,Y),(X+x,Y+y)):
                    continue #中央地点から対角線上に経路が伸びてほしくないので
                if isinside(X+x,Y+y) and height[Y+y][X+x]-height[Y][X]==1*last_adjustment:
                    dif1_diag.append((-(num_of_blocks-1)//2+X+x/2,-(num_of_blocks-1)//2+Y+y/2,(height[Y+y][X+x]+height[Y][X])/2,angle))
                    row.append(index_for_dijkstra(X,Y))
                    col.append(index_for_dijkstra(X+x,Y+y))
                    data.append(969)
                elif isinside(X+x,Y+y) and height[Y+y][X+x]-height[Y][X]==-1*last_adjustment:
                    dif1_diag.append((-(num_of_blocks-1)//2+X+x/2,-(num_of_blocks-1)//2+Y+y/2,(height[Y+y][X+x]+height[Y][X])/2,angle+math.pi))
                    row.append(index_for_dijkstra(X,Y))
                    col.append(index_for_dijkstra(X+x,Y+y))
                    data.append(969)
    dif1_diag=[(x*scale_factor,y*scale_factor,z,-angle) for x,y,z,angle in dif1_diag]
    temp_dif1_diag_len=len(dif1_diag)
    #https://note.nkmk.me/python-list-unique-duplicate/ 参考
    dif1_diag_seen=[] #二つの階段が交差してしまっている場合、片方を取り除く
    dif1_diag=[(x,y,z,angle) for x,y,z,angle in dif1_diag if (x,y) not in dif1_diag_seen and not dif1_diag_seen.append((x,y))]

    dif2=[]#SLOPE
    for X in (0,1,num_of_blocks-3,num_of_blocks-2): #元々の範囲がnum_of_blocksまでのため-1,さらにx,yの値が正だからさらに-1,つまり-2
        for Y in (0,1,num_of_blocks-3,num_of_blocks-2): #num_of_blocks=9の時用にX,Yはそれぞれ4個までにしている。場合によっては増減させる
            for x,y,angle in [(1,0,0),(0,1,-math.pi/2)]:
                if isinside(X+x,Y+y) and height[Y+y][X+x]-height[Y][X]==2*last_adjustment:
                    dif2.append((-(num_of_blocks-1)//2+X+x/2,-(num_of_blocks-1)//2+Y+y/2,(height[Y+y][X+x]+height[Y][X])/2,angle))
                    row.append(index_for_dijkstra(X,Y))
                    col.append(index_for_dijkstra(X+x,Y+y))
                    data.append(721)
                elif isinside(X+x,Y+y) and height[Y+y][X+x]-height[Y][X]==-2*last_adjustment:
                    dif2.append((-(num_of_blocks-1)//2+X+x/2,-(num_of_blocks-1)//2+Y+y/2,(height[Y+y][X+x]+height[Y][X])/2,angle+math.pi))
                    row.append(index_for_dijkstra(X,Y))
                    col.append(index_for_dijkstra(X+x,Y+y))
                    data.append(721)
    dif2=[(x*scale_factor,y*scale_factor,z,-angle) for x,y,z,angle in dif2]


    #####dijkstra#####
    row_np=np.array(row)
    col_np=np.array(col)
    data_np=np.array(data)
    graph=csr_matrix((data_np, (row_np, col_np)), shape=(num_of_blocks**2, num_of_blocks**2)).toarray()
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
    #https://note.nkmk.me/python-scipy-shortest-path/ 参考
    distance=dijkstra(graph, directed=False, indices=[index_for_dijkstra(x,y) for x,y in [(0,0),(0,num_of_blocks-1),(num_of_blocks-1,0),(num_of_blocks-1,num_of_blocks-1)]])
    distance_mid=[distance[i][index_for_dijkstra((num_of_blocks-1)//2,(num_of_blocks-1)//2)] for i in range(4)]
    
    #中央地点に到達可能か
    print("highest_counter:",highest_counter,"  number of reachable corners:",4-distance_mid.count(float('inf')))
    if 4-distance_mid.count(float('inf'))==4:
        print("congratulations!!!!!")
        is_good_maze=True
        break
#以上までがhighest_counterによるループ

if not is_good_maze:
    print("There was not any good mazes.\nTRY AGAIN")
    #当たり前ですが、ここでsys.exitを使うとこのスクリプトのみならずblender自体が終了します。
    #私は何も考えずにそれをやらかして!?!?となりました。
    #以下elseで分岐してもいいですが、インデントが嫌なので今回は続行しています。

#print("height:",height,"\n")
#print("dif0:",dif0)
#print("len(dif0)=",len(dif0),"(deleted=",dif0_deleted,")\n")
#print("dif1:",dif1)
#print("len(dif1)=",len(dif1),"(deleted=",dif1_deleted,")\n")
#print("dif1_diag:",dif1_diag)
#print("len(dif1_diag)=",len(dif1_diag),"(deleted=",temp_dif1_diag_len-len(dif1_diag),")\n")
#print("dif2:",dif2)
#print("len(dif2)=",len(dif2),"\n")
#print("row:",row)
#print("col:",col)
#print("data:",data)

rowcol=[[row[i],col[i]] for i in range(len(row))]
#print("(row,col)-->\n",rowcol,"\n")
rowcol_flatten=sum(rowcol,[])

def isconnected(i):
    for j in range(4):
        if distance[j][i]!=float('inf'):
            return True
    return False


#####宝箱の場所決めなど#####
dead_end_points=[i for i in range(num_of_blocks**2) if rowcol_flatten.count(i)==1 and isconnected(i)]
#スタート地点にもゴール地点にも近くない場所の行き止まりのみに宝箱を設置します
valid_dead_end_points=[point for point in dead_end_points \
    if (num_of_blocks//3<=reverse_index_for_dijkstra(point)[0]<2*num_of_blocks//3 or num_of_blocks//3<=reverse_index_for_dijkstra(point)[1]<2*num_of_blocks//3) \
    and (not (num_of_blocks//3<=reverse_index_for_dijkstra(point)[0]<2*num_of_blocks//3 and num_of_blocks//3<=reverse_index_for_dijkstra(point)[1]<2*num_of_blocks//3))]    

try:
    treasure_chest=random.choice(valid_dead_end_points)
except IndexError:
    treasure_chest=random.choice(dead_end_points)
    print("WARNING!!! This is not desirable. You chose an invalid dead end point as treasure chest location")

print("treasure_chest",reverse_index_for_dijkstra(treasure_chest))
before_treasure_chest=rowcol_flatten[rowcol_flatten.index(treasure_chest)+1] if rowcol_flatten.index(treasure_chest)%2==0 else rowcol_flatten[rowcol_flatten.index(treasure_chest)-1]
print("before",reverse_index_for_dijkstra(before_treasure_chest))
direction=reverse_index_for_dijkstra(before_treasure_chest-treasure_chest,True)
print("direction",direction)
treasure_chest_angle=direction[1]*(2-direction[0])*math.pi/4 if direction[1]!=0 else (1-direction[0])*math.pi/2
#print("treasure_chest_angle",treasure_chest_angle)
treasure_x,treasure_y=reverse_index_for_dijkstra(treasure_chest)
treasure_chest_data=[((-(num_of_blocks-1)//2+treasure_x)*scale_factor,(-(num_of_blocks-1)//2+treasure_y)*scale_factor,height[treasure_y][treasure_x],treasure_chest_angle)]

#print("distance-->\n",distance,"\n")
print("X:0 Y:0-->",distance_mid[0])
print("X:0 Y:{}-->".format(num_of_blocks-1),distance_mid[1])
print("X:{} Y:0-->".format(num_of_blocks-1),distance_mid[2])
print("X:{0} Y:{0}-->".format(num_of_blocks-1),distance_mid[3])


#####(Unityで使うための)データを保存#####
dt_now=str(datetime.datetime.now()).replace(":","_").replace("-","_").replace(".","") #ファイル名として使えない文字などを取り除く
dt_now=dt_now[-11:-6] #最終的に用いるには日時だと長すぎるので、分秒だけを取り出します。

def conversion_for_unity(mydata): #Unityの形式に合うようデータを整形します。
    return [[x,y,z-foundation_height-entire_cube_sidelength/2,(180*angle/math.pi)] for x,y,z,angle in mydata]
def write_txt_file(name:str,mylist:list): #C#の形式に合うようデータを出力します。
    leny=len(mylist)
    txt_file.write("\tpublic static readonly float[,] {0} = \n".format(name+"_side_"+dt_now))
    txt_file.write("\t{\n")
    temp_txt_list=["\t\t{"+"f,".join([str(n) for n in mylist[i]])+"f}," for i in range(leny)] #fはfloatへのキャスト
    txt_file.write("\n".join(temp_txt_list)+"\n")
    txt_file.write("\t};\n\n")

height_for_txt=[[height[j][i]-foundation_height-entire_cube_sidelength/2 for i in range(num_of_blocks)]for j in range(num_of_blocks)]
dif0_for_txt=conversion_for_unity(dif0)
dif1_for_txt=conversion_for_unity(dif1)
dif1_diag_for_txt=conversion_for_unity(dif1_diag)
dif2_for_txt=conversion_for_unity(dif2)
treasure_chest_for_txt=conversion_for_unity(treasure_chest_data)
distance_for_txt=[[[distance[k][index_for_dijkstra(i,j)] for i in range(num_of_blocks)] for j in range(num_of_blocks)] for k in range(4)]

#1048576==2**20 C#はint型にinfがないそうなので、この数で代用しました。桁あふれが怖いので、少し小さめです。
distance_for_txt=[[[distance_for_txt[k][j][i] if distance_for_txt[k][j][i]!=float('inf') else 1048576 for i in range(num_of_blocks)] for j in range(num_of_blocks)] for k in range(4)]
with open("C:\\Users\\hari64\\OneDrive\\ドキュメント\\Blender\\blender script\\"+"maze_data_"+dt_now+".txt","x") as txt_file: #txtを日付付きで新規作成
    write_txt_file("height",height_for_txt)
    write_txt_file("dif0",dif0_for_txt) #unityとblenderで軸などが異なりますが、ここでは数値を変換せずblenderの値をそのまま出力します。
    write_txt_file("dif1",dif1_for_txt) #ちなみに書いておくと、blenderでのz軸がunityでのy軸になります。
    write_txt_file("dif1_diag",dif1_diag_for_txt)
    write_txt_file("dif2",dif2_for_txt)
    write_txt_file("treasure_chest",treasure_chest_for_txt)

with open("C:\\Users\\hari64\\OneDrive\\ドキュメント\\Blender\\blender script\\"+"maze_dijkstra_"+dt_now+".txt","x") as txt_file:
    txt_file.write("\tint[,,] distance_side_"+dt_now+" = new int[4,{0},{0}]\n".format(num_of_blocks))
    txt_file.write("\t{\n")
    for k in range(4):
        txt_file.write("\t\t{\n")
        for j in range(num_of_blocks): #intのためfは不要
            txt_file.write("\t\t\t{"+",".join(map(lambda x: str(int(x)), distance_for_txt[k][j]))+"},\n")
        txt_file.write("\t\t},\n")
    txt_file.write("\t};\n\n")
    

########################################################################
#ここからbpyで実際にblender上へオブジェクトを配置していきます


#####全削除#####
for COLLECTION in bpy.context.scene.collection.children:
    if COLLECTION.name=="DONT DELETE":
        continue
    bpy.context.scene.collection.children.unlink(COLLECTION)
#for item in bpy.context.scene.collection.objects: #Scene Collectionに直接属しているオブジェクトを削除
#    bpy.context.scene.collection.objects.unlink(item)
#今回は最後までそれが発生しなかったのでコメントアウトしたままです
#for item in bpy.data.objects: #これだとDONT DELETE内のオブジェクトもすべて削除されてしまいます
#    bpy.data.objects.remove(item) #全削除コマンドとしてこれが一番有名な気がしますが、今回は使えません
for _ in range(6): #6回繰り返しているのはpurgeがネスト内のものに対して有効に働かないからです
#system consoleを見る限り、恐らく今回は5回でも大丈夫ですが、たとえ回数が多くとも
#Info: No orphaned data-blocks to purgeを吐くだけなので問題はありません。
#今回はemptyからcollection instanceを作成しているので回数が増えています。
    bpy.ops.outliner.orphans_purge() #orphansを消去しないと、命名などの邪魔になります。

#####originial collectionの作成#####
original_collection = bpy.data.collections.new("ORIGINAL"+dt_now)
bpy.context.scene.collection.children.link(original_collection)
original_collection = bpy.context.view_layer.layer_collection.children[original_collection.name]
bpy.context.view_layer.active_layer_collection = original_collection 

for x in range(-(num_of_blocks-1)//2,(num_of_blocks-1)//2+1):
    for y in range(-(num_of_blocks-1)//2,(num_of_blocks-1)//2+1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
        bpy.ops.transform.resize(value=(cuboid_sidelength, cuboid_sidelength, 1))
        bpy.ops.transform.translate(value=(region*x ,region*y , 0))
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.transform.resize(value=(1, 1, height[y+(num_of_blocks-1)//2][x+(num_of_blocks-1)//2]))

bpy.data.collections["DONT DELETE"].hide_select=True #一部を選択させない
bpy.ops.object.select_all(action='SELECT') #当たり前ですが、select allを書くときは本当に全てを選択してよいのか確かめましょう。
bpy.ops.transform.translate(value=(0, 0, -foundation_height-entire_cube_sidelength/2))
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.select_all(action='DESELECT') #そしてdeselectもお忘れなく。私は二つとも失念して惨敗しました。
bpy.data.collections["DONT DELETE"].hide_select=False


#途中まで利用していました。
#####instance collectionの作成#####
if not isfinal:
    instance_collection = bpy.data.collections.new("INSTANCE")
    bpy.context.scene.collection.children.link(instance_collection)
    instance_collection = bpy.context.view_layer.layer_collection.children[instance_collection.name]
    bpy.context.view_layer.active_layer_collection = instance_collection 

    for i in range(5):
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.transform.rotate(value=math.pi/2 if i!=4 else math.pi, orient_axis='X')
        bpy.ops.transform.rotate(value=i*math.pi/2 if i!=4 else 0, orient_axis='Z')
        bpy.context.object.instance_type = 'COLLECTION' #emptyのインスタンス機能を使う
        bpy.context.object.instance_collection = bpy.data.collections[original_collection.name] #インスタンスコレクションとしてORIGINALを選択
    bpy.ops.object.select_all(action='DESELECT')



#####橋や階段の建設#####
def construction(target_object:str,dif_data):
    bpy.context.view_layer.objects.active = bpy.data.objects[target_object]
    bpy.data.collections[original_collection.name].objects.link(bpy.context.view_layer.objects.active)
    bpy.data.collections['DONT DELETE'].objects.unlink(bpy.context.view_layer.objects.active)
    for x,y,z,angle in dif_data:
        bpy.context.view_layer.objects.active = bpy.data.objects[target_object]
        bpy.context.view_layer.objects.active.select_set(True)
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'},TRANSFORM_OT_translate={"value":(x,y,z-foundation_height-entire_cube_sidelength/2)})
        bpy.ops.transform.rotate(value=angle, orient_axis='Z',constraint_axis=(False,False,True))
        bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[target_object]
    bpy.data.collections['DONT DELETE'].objects.link(bpy.context.view_layer.objects.active)
    bpy.data.collections[original_collection.name].objects.unlink(bpy.context.view_layer.objects.active)

construction("BRIDGE",dif0)
construction("STAIRS",dif1)
construction("DIAGONAL STAIRS",dif1_diag)
construction("SLOPE",dif2)
construction("TREASURE CHEST",treasure_chest_data)


#####FBX(3DCG用のファイル形式)のエクスポート#####
if isfinal: #これを実行するとBlocksの回転がblender上ではおかしくなります
    bpy.context.view_layer.objects.active = bpy.data.objects['Cube']
    bpy.context.view_layer.objects.active.select_set(True)
    bpy.context.view_layer.objects.active.name="Blocks_"+dt_now
    for i in range(num_of_blocks**2-1): #添え字がついていないものが必ず一つできるので、それを除くための-1
        bpy.data.objects['Cube.{:0=3}'.format(i+1)].select_set(True)
    bpy.ops.object.join() #扱いやすいように結合しておく
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.transform.rotate(value=math.pi, orient_axis='Z',constraint_axis=(False,False,True))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.export_scene.fbx(filepath='C:\\Users\\hari64\\OneDrive\\ドキュメント\\Blender\\blender script\\FBX_side_Blocks_'+dt_now+'.fbx', use_selection=True, bake_space_transform=True, object_types={'MESH'})
    bpy.ops.transform.rotate(value=-math.pi, orient_axis='Z',constraint_axis=(False,False,True))
```

以上、"最終的に使用したコード全文"のプルダウンでした。

</div></details>

<details><summary>おまけ(Blenderを使っている人向け) </summary><div>

#### おまけ その1

もしかしたら知っている方も多いかも知れませんが、プロパティシェルフ(nキーで出てくるもの)→View(3番目)→View(先頭)→**Focal Length**で、画角を変えられます。私はここを滅多に触らないので見づらいのを我慢しながら途中まで作業していました。こういう「広角で全体をちゃんと見たい!」、という時にとても便利ですね。また **Walk Navigation** でwasd操作が出来るので、お手軽ゲーム体験ができます。こっちもUnityにわざわざ持って行かなくともゲームの雰囲気が分かるので便利です。

#### おまけ その2

```python
bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
```

がR→Z→**90**と打った時、つまり、z軸に90度回転した時のInfo欄の表示なんですが、これでは冗長です。なので、関数の引数を省略すればデフォルト値が使われることを利用して

```python
bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
```

と、大事そうかなと思う部分だけを残して他の部分を消して普段私はコードを書いていました。
しかし、なんとびっくり、このコードだと **-90度** 回転になります。
私は全くこのことを知りませんでした。今回の作業中にも何か角度が合わないなという時は計算ミスかと思っていましたが、どうやらそもそもコードが間違っていたようです。
本当に必要なのは

```python
bpy.ops.transform.rotate(value=1.5708,constraint_axis=(False, False, True))
```

とconstraint_axisでした。これを消してしまうと意図しない動作をするようです。(※orient_axisがzでない場合などは他の要素も必要になります。)ちゃんと公式のドキュメント見て何がデフォルト値なのか気を付ける必要がありますね。。。

#### おまけ その3

select_all関連の惨敗(コードのコメントにも書いたもの)の様子
![messageImage_1615098205998.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/3b422aab-4283-82e1-50c0-bd639854b701.jpeg)

#### おまけ その4

以下に今回採用した、オブジェクトを削除する為のコードを示します。

```python
import bpy
for COLLECTION in bpy.context.scene.collection.children:
    if COLLECTION.name=="DONT DELETE":
        continue
    bpy.context.scene.collection.children.unlink(COLLECTION)
for _ in range(6):
    bpy.ops.outliner.orphans_purge()
```

多くのBlenderでscriptを使う方が、何かしら削除系のコードを冒頭に付けているかと思います。これは何回もコードを実行するときに、前の実行結果を消去して元の状態に戻してくれるからです。
ただ、簡単な削除のみだと、collectionがそのまま残ったり、(unlinkしているだけなので)orphan dataが残って命名の邪魔をしたりと不都合が多いです。それを解決してくれたのが、この7行です。さらに削除の例外コレクションも置いておくことが出来ます。
(DONT DELETEという名前のコレクションにすれば、それが例外になります。)(詳しくは全文のコメントを参照してください。また、よりよい手段をご存じであればご教授ください。)

以上、"おまけ(Blenderを使っている人向け)"のプルダウンでした。

</div></details>

## Step3 Unity上でゲームを完成させる

最後に、ゲームとして完成させていきます。迷路の生成以外にもいろいろやりましたが、ここに書いてしまってはネタバレなので、大半は省略します。ただ、一点だけマテリアルについて軽く触れようと思います。

### MatCapについて

今回、マテリアルとしては**MatCap**と言う技術を採用しました。
私が3DCGの技術で何が一番好きかと言われたら多分MatCapを挙げると思います。**結構面白い技術**です。
そもそもMatCapとは、という話ですが、[Blenderのマニュアル](https://docs.blender.org/manual/en/latest/glossary/index.html?highlight=matcap)では次のようになっています。

>Stands for “material capture”, using an image to represent a complete material including lighting and reflections.
>(MatCapとは「マテリアル・キャプチャー」の略で、照明や反射の情報を含む完璧なマテリアルを画像で表現することである。(筆者訳))

以下が一例です。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/99d9d9db-69a8-b200-0f1a-abdc0e235f64.png)

↑このような画像群だけから
↓このような結果が得られます。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/8e18f4ea-a3f6-e831-77ca-61d9ef5fcd37.png)

特に下段中央の色が派手な猿を上の画像と見比べてもらえると、雰囲気がつかみやすいかも知れません。

ここまで書くと、「なるほど、で何が凄いの?」と思われる方も多いかも知れません。世間一般的にMatCapの長所は**時間計算量も空間計算量もどちらも非常に小さい**ということが言われています。なにせ光線の計算も何もせずに、ほぼ面の法線だけで色を決めているので、どの角度の面にどの色を振るかを決める写真一枚だけでほぼ計算は完結しています。しかも画像の数だけ結果が変わるので千変万化です。そして今回の場合では**一切のライトなし**にそれらしい絵が完成するというのも長所になります。あそこにもライトを設置してこちらにもライトを設置して……、とすると色々大変なことも多いのですが、その手間も省けるのは魅力的です。MatCapはメジャーな、しかもかなり古い技術ですが、それでもやはり凄いなとしみじみ感心します。CGに興味のあまりないプログラマの方にも、MatCapの良さが伝われば。

<details><summary>おまけ</summary><div>

#### おまけ その5

先述の通り、私はMatCapがかなり好きです。ただ、正直今回のようなシーンにそれを用いるのが最適かと問われると否な気がします。なにせ法線が同じ向きを向いている面が多すぎて、多くの面が同じ色になってしまい、のっぺりとした印象しか与えられません。それでもMatCapを用いているのは、プレハブをインスタンス化しているが為にライト情報を焼くに焼けないなどという消極的な理由がありました。

そしてやや残念なことに、どうやらUnityのMatCapはBlenderのMatCapと異なり同一面上の色が一色しかないようです。Blenderは恐らくある程度広い範囲の情報を計算に用いているのでMatcapでもかなりいい感じの仕上がりになります。(下図参照)
![messageImage_1616251127756.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/e8c2c261-c121-fe70-ed84-898614f1b9b9.jpeg)

この点をどう解決するかはかなり悩んだのですが、結局shader graphで補正をかけるような形に着地しました。

![messageImage_1616335732032.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/cda6b2a7-2c4f-5a14-06f2-3cd660134013.jpeg)

#### おまけ その6

Step2で作成したデータをどのように使ったかは示した方が良いかと思ったので、コードを一部書いておきます。

```c#
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

static class Constants
{
 public static readonly float[,] height_side_23_53 =
 {
  {-40.5f,-42.5f,-48.5f,-52.5f,-46.5f,-50.5f,-48.5f,-42.5f,-40.5f},
  {-44.5f,-48.5f,-54.5f,-58.5f,-56.5f,-56.5f,-50.5f,-48.5f,-44.5f},
  {-48.5f,-52.5f,-54.5f,-58.5f,-62.5f,-60.5f,-52.5f,-50.5f,-44.5f},
  {-50.5f,-56.5f,-58.5f,-64.5f,-60.5f,-62.5f,-60.5f,-54.5f,-52.5f},
  {-54.5f,-54.5f,-60.5f,-60.5f,-64.5f,-60.5f,-58.5f,-52.5f,-52.5f},
  {-50.5f,-56.5f,-60.5f,-60.5f,-62.5f,-62.5f,-60.5f,-54.5f,-52.5f},
  {-50.5f,-52.5f,-54.5f,-58.5f,-60.5f,-60.5f,-56.5f,-50.5f,-46.5f},
  {-44.5f,-48.5f,-54.5f,-52.5f,-54.5f,-58.5f,-54.5f,-44.5f,-44.5f},
  {-40.5f,-42.5f,-50.5f,-52.5f,-52.5f,-52.5f,-46.5f,-42.5f,-40.5f},
 };
        //中略 データが千行程
}

public class Maze_game_manager : MonoBehaviour
{
 public GameObject prefab_BRIDGE;
    public GameObject prefab_SLOPE;
    public GameObject prefab_STAIRS;
    public GameObject prefab_DIAGONAL_STAIRS;
 public GameObject prefab_TREASURE_CHEST;

 public GameObject[] list_of_prefab_BLOCKS = new GameObject[8];

 public GameObject[] list_of_empty_side = new GameObject[4];
 public GameObject[] list_of_empty_tobo = new GameObject[2]; //tobo-->top and bottom
 
 void Construction(GameObject prefab, float[,] mydata, GameObject parent)
    {
        for (int i = 0; i < mydata.GetLength(0); i++)
        {
            float x = mydata[i, 0];
            float y = mydata[i, 2]; //blenderでのz軸 blenderは右手座標系 unityは左手座標系です
            float z = mydata[i, 1]; //blenderでのy軸
            float degree = mydata[i, 3]; //blenderでのz軸回転 
   //右手座標系におけるz軸中心の正方向回転は左手座標系におけるy軸中心の負方向回転
   Instantiate(prefab, new Vector3(x,y,z), Quaternion.Euler(0,-degree,0), parent.transform);
        }
    }

    void Start()
 { 
  List<int> numbers = new List<int>() { 0, 1, 2, 3, 4, 5, 6, 7 };
  numbers = numbers.OrderBy(a => Guid.NewGuid()).ToList(); //使用されるデータに重複があってほしくないのでシャッフルの方式をとりました

  System.Random random = new System.Random();

  //bottom
  Debug.Log($"bottom number:{numbers[0]}");
  Instantiate(list_of_prefab_BLOCKS[numbers[0]], new Vector3(0, 0, 0), Quaternion.Euler(0, 0, 0),list_of_empty_tobo[0].transform);
  Construction(prefab_BRIDGE,          Constants.dif0s          [numbers[0]], list_of_empty_tobo[0]);
  Construction(prefab_STAIRS,          Constants.dif1s          [numbers[0]], list_of_empty_tobo[0]);
  Construction(prefab_DIAGONAL_STAIRS, Constants.dif1_diags     [numbers[0]], list_of_empty_tobo[0]);
  Construction(prefab_SLOPE,           Constants.dif2s          [numbers[0]], list_of_empty_tobo[0]);
  Construction(prefab_TREASURE_CHEST,  Constants.treasure_chests[numbers[0]], list_of_empty_tobo[0]); 
  list_of_empty_tobo[0].transform.rotation = Quaternion.Euler(0, 0, 0); //game startしてすぐ崖は望ましくないのでランダム回転はさせない

  //side
  for (int i = 1; i < 5; i++)
        {
            Debug.Log($"side number:{numbers[i]}");
   Instantiate(list_of_prefab_BLOCKS[numbers[i]], new Vector3(0, 0, 0), Quaternion.Euler(0, 0, 0), list_of_empty_side[i-1].transform);
   Construction(prefab_BRIDGE,          Constants.dif0s          [numbers[i]], list_of_empty_side[i-1]);
            Construction(prefab_STAIRS,          Constants.dif1s          [numbers[i]], list_of_empty_side[i-1]);
            Construction(prefab_DIAGONAL_STAIRS, Constants.dif1_diags     [numbers[i]], list_of_empty_side[i-1]);
   Construction(prefab_SLOPE,           Constants.dif2s          [numbers[i]], list_of_empty_side[i-1]);
   Construction(prefab_TREASURE_CHEST,  Constants.treasure_chests[numbers[i]], list_of_empty_side[i-1]);
   list_of_empty_side[i-1].transform.rotation=Quaternion.Euler(90, (i-1) * 90, 0); //sideの四面それぞれに、当該オブジェクトを振り当てる
   list_of_empty_side[i-1].transform.Rotate(Vector3.up, random.Next(0, 4) * 90);     //ランダマイズの為の回転
  }

  //top
  Debug.Log($"top number:{numbers[5]}");
  Instantiate(list_of_prefab_BLOCKS[numbers[5]], new Vector3(0, 0, 0), Quaternion.Euler(0, 0, 0), list_of_empty_tobo[1].transform);
  Construction(prefab_BRIDGE,          Constants.dif0s          [numbers[5]], list_of_empty_tobo[1]);
  Construction(prefab_STAIRS,          Constants.dif1s          [numbers[5]], list_of_empty_tobo[1]);
  Construction(prefab_DIAGONAL_STAIRS, Constants.dif1_diags     [numbers[5]], list_of_empty_tobo[1]);
  Construction(prefab_SLOPE,           Constants.dif2s          [numbers[5]], list_of_empty_tobo[1]);
  Construction(prefab_TREASURE_CHEST,  Constants.treasure_chests[numbers[5]], list_of_empty_tobo[1]);
  list_of_empty_tobo[1].transform.rotation = Quaternion.Euler(180, random.Next(0, 4) * 90, 0);
 }
}

```

以上"おまけ"のプルダウンでした。

</div></details>

## 最後に

以上でゲームは完成となります。是非遊んで下さい。この記事で語ったことは半分程度です。残り半分はゲームを通して想像していただければ。

また、身の上話で恐縮ですが、私は今までしてきたゲームと言うのが片手で数えられるほどにはゲームに対して興味がない人間でした。ただ、絵や3DCG、そして数学(≒プログラミング)に時間を捧げてきた自分には、割とあっている趣味かなと思っています。作っていて非常に楽しかったです。

私はゲームの定石(なんならWASD操作すらおぼろげでしたが……)をあまり知らない為、至らぬ点も多々あるかも知れません。ただ、おまけまで見てくれた方には分かると思いますが、Blenderを扱う上での落とし穴と、Unityを扱う上での落とし穴と、Blender→Unityへの翻訳作業における落とし穴という三つの落とし穴にはまりまくった3週間の産物がこの作品です。遊んで頂けると報われます。

最後までお読みいただきありがとうございました。

## 参考文献、リンク先

穴掘り法など

https://algoful.com/Archive/Algorithm/MazeDig#:~:text=%E7%A9%B4%E6%8E%98%E3%82%8A%E6%B3%95%E3%81%AF%E6%96%87%E5%AD%97%E9%80%9A%E3%82%8A,%E5%AF%BE%E7%85%A7%E7%9A%84%E3%81%AA%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0%E3%81%A7%E3%81%99%E3%80%82

ゲームのリンク先

https://unityroom.com/games/hari_kagiyanomusume_maze

WASDで操作、Spaceでジャンプ、Tでタイトル画面に戻ります。PCからお遊びください。

※※注意※※
本ゲームはマウスカーソルを消した状態で遊んでもらうことを前提としています。本来自動で消えるはずですが、場合によっては画面を一度クリックして頂く必要があります。挙動がおかしいと思った方は一度お試しください。
