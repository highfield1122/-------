#スクレイピングして、サイトのもっとも使われている単語を top 1 2 3 で回数をまとめて　スクレイピング結果を画像にして保存するプログラム。
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

def scrape_and_analyze(url):
    # サイトのHTMLを取得
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # サイト内のテキストを抽出
    text_content = ' '.join(element.getText() for element in soup.find_all(['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']))

    # 単語のカウント
    words = text_content.split()
    word_count = {}
    for word in words:
        word = word.lower()
        if word.isalpha():
            word_count[word] = word_count.get(word, 0) + 1

    # カウントが多い順にソート
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # トップ1〜3の単語とその回数を表示
    top_words_info = []
    for i in range(3):
        word = sorted_word_count[i][0]
        count = sorted_word_count[i][1]
        top_words_info.append(f"No{i + 1} {word} → {count}回")
        print(f"トップ{i + 1}: {word}, 出現回数: {count}回")

    # 日本語フォントを指定
    font_path = "C:\\Windows\\Fonts\\meiryo.ttc"  # あなたの環境に合わせてフォントパスを指定してください
    font_prop = FontProperties(fname=font_path)

    # サイトのURLを画像に追加
    top_words_info.insert(0, f"スクレイピング対象サイト: {url}")

    # トップ1〜3の情報を一つのPNGファイルにまとめて保存
    file_count = 1
    while True:
        file_name = f'top_words_summary{file_count}.png'
        if not os.path.exists(file_name):
            break
        file_count += 1

    plt.figure(figsize=(10, 5))
    plt.text(0.1, 0.5, '\n'.join(top_words_info), fontproperties=font_prop, fontsize=12)
    plt.axis('off')
    plt.savefig(file_name, bbox_inches='tight')

if __name__ == "__main__":
    # スクレイピング対象のサイトURL
    site_url = "https://www.o-hara.ac.jp/"
    scrape_and_analyze(site_url)
