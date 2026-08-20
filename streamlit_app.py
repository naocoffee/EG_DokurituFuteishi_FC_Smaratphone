import random
import streamlit as st

# =========================================================
# データ定義（独立不定詞）
# =========================================================
flashcards = [
    {
        "word": "to tell (you) the truth",
        "meaning": "「実を言うと」（←真実をあなたに話せば）",
    },
    {
        "word": "to be frank (with you)",
        "meaning": "「（君に）率直に言うと」（←あなたに対して率直になれば）",
    },
    {
        "word": "to be honest (with you)",
        "meaning": "「（君に）正直に言うと」（←あなたに対して正直になれば）",
    },
    {
        "word": "to begin with",
        "meaning": "「まずはじめに」（←それではじめれば）",
    },
    {
        "word": "to make matters worse",
        "meaning": "「さらに悪いことに」（←事をより悪くすれば）",
    },
    {
        "word": "to say nothing of ...",
        "meaning": "「…はもちろん」（←…については何も言わないで）",
    },
    {
        "word": "not to mention ...",
        "meaning": "「…は言うに及ばず」（←…のことを言わないで）",
    },
    {
        "word": "strange to say",
        "meaning": "「不思議なことだが」（←言うのは不思議だが）",
    },
    {
        "word": "needless to say",
        "meaning": "「言うまでもなく」（←言う必要はないが）",
    },
]

TOTAL = len(flashcards)

# =========================================================
# ページ設定 & CSS
# =========================================================
st.set_page_config(page_title="独立不定詞フラッシュカード", layout="centered")

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Yu Gothic", "游ゴシック", "Yu Gothic Medium", "游ゴシック体", sans-serif !important;
        font-weight: 700 !important;
    }

    .stApp {
        background-color: #ffffff;
    }

    h1, h2, h3, .stCaption, p, span, div, label {
        font-family: "Yu Gothic", "游ゴシック", "Yu Gothic Medium", "游ゴシック体", sans-serif !important;
        font-weight: 700 !important;
    }

    h1 {
        color: #4a3f2a !important;
        transform: rotate(-1deg);
    }

    /* --- フラッシュカード本体：手書きノート風（アスペクト比 9:15） --- */
    .flash-card {
        position: relative;
        border-radius: 10px 14px 12px 16px / 14px 10px 16px 12px;
        padding: 32px 24px;
        width: 100%;
        max-width: 340px;
        aspect-ratio: 9 / 15;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin: 0 auto 24px auto;
        transform: rotate(-0.6deg);
        box-shadow: 6px 8px 0px rgba(74, 63, 42, 0.15);
    }

    .front-card {
        background: #ffffff;
        color: #000000;
        border: 3px solid #4a3f2a;
        transform: rotate(0.8deg);
    }

    .back-card {
        background: #ffffff;
        color: #000000;
        border: 3px solid #b5762c;
        transform: rotate(-0.8deg);
    }

    .card-label {
        font-size: 13px;
        letter-spacing: 3px;
        opacity: 0.6;
        margin-bottom: 10px;
        text-transform: uppercase;
        font-weight: 700;
        border-bottom: 2px dashed #4a3f2a;
        padding-bottom: 6px;
    }

    .card-word {
        font-size: clamp(24px, 8vw, 42px);
        font-weight: 700;
        margin-bottom: 18px;
        line-height: 1.3;
        color: #000000;
        word-break: break-word;
    }

    .card-meaning {
        font-size: clamp(18px, 6vw, 32px);
        font-weight: 700;
        margin-bottom: 16px;
        line-height: 1.6;
        color: #000000;
        word-break: break-word;
    }

    .stat-box {
        text-align: center;
        border-radius: 12px 16px 14px 18px / 16px 12px 18px 14px;
        padding: 20px 10px;
        font-weight: 700;
        border: 3px solid #4a3f2a;
        transform: rotate(-1deg);
    }

    /* --- ボタン：手描き風の枠線 --- */
    .stButton > button {
        font-family: "Yu Gothic", "游ゴシック", "Yu Gothic Medium", "游ゴシック体", sans-serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 10px 14px 12px 16px / 14px 10px 16px 12px !important;
        border: 3px solid #4a3f2a !important;
        background: #fffdf6 !important;
        color: #2e2a20 !important;
        box-shadow: 3px 4px 0px rgba(74, 63, 42, 0.25);
        transition: transform 0.1s ease-in-out;
    }
    .stButton > button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 5px 6px 0px rgba(74, 63, 42, 0.25);
        color: #b5762c !important;
        border-color: #b5762c !important;
    }
    .stButton > button[kind="primary"] {
        background: #ffe3b3 !important;
        color: #7a4a12 !important;
    }

    /* --- 進捗バー --- */
    .stProgress > div > div {
        background-color: #b5762c !important;
    }

    /* --- チェックボックス文字 --- */
    .stCheckbox label {
        font-family: "Yu Gothic", "游ゴシック", "Yu Gothic Medium", "游ゴシック体", sans-serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #4a3f2a !important;
    }

    /* --- キャプション文字 --- */
    .stCaption, [data-testid="stCaptionContainer"] {
        font-family: "Yu Gothic", "游ゴシック", "Yu Gothic Medium", "游ゴシック体", sans-serif !important;
        font-weight: 700 !important;
        color: #4a3f2a !important;
    }

    /* --- 「全◯枚のカードが登録されています」等の基準テキスト --- */
    .base-text {
        font-family: "Yu Gothic", "游ゴシック", "Yu Gothic Medium", "游ゴシック体", sans-serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #000000;
    }

    /* --- st.metric の数値・ラベル --- */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        font-family: "Yu Gothic", "游ゴシック", "Yu Gothic Medium", "游ゴシック体", sans-serif !important;
        font-weight: 700 !important;
        color: #4a3f2a !important;
    }
    /* --- サブタイトル文字（小さめ） --- */
    .subtitle-text {
        font-family: "Yu Gothic", "游ゴシック", "Yu Gothic Medium", "游ゴシック体", sans-serif !important;
        font-weight: 700 !important;
        color: #4a3f2a !important;
        opacity: 0.8;
        margin-top: -8px;
        margin-bottom: 12px;
    }

    /* --- スマートフォン向け調整 --- */
    @media (max-width: 480px) {
        .flash-card {
            max-width: 260px;
            padding: 20px 16px;
            transform: rotate(0deg) !important;
            border-radius: 8px !important;
        }
        .front-card, .back-card {
            transform: rotate(0deg) !important;
        }
        .card-label {
            font-size: 11px;
            margin-bottom: 6px;
        }
        .stButton > button {
            font-size: 14px !important;
            padding: 6px 4px !important;
        }
        /* 「表面に戻す・覚えた・まだ不安」の3ボタンを縦積みに */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# セッション状態の初期化
# =========================================================
def init_session():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "order" not in st.session_state:
        st.session_state.order = list(range(TOTAL))
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "flipped" not in st.session_state:
        st.session_state.flipped = False
    if "good_count" not in st.session_state:
        st.session_state.good_count = 0
    if "review_count" not in st.session_state:
        st.session_state.review_count = 0
    if "review_words" not in st.session_state:
        st.session_state.review_words = []
    if "finished" not in st.session_state:
        st.session_state.finished = False


def reset_all():
    st.session_state.started = False
    st.session_state.order = list(range(TOTAL))
    st.session_state.index = 0
    st.session_state.flipped = False
    st.session_state.good_count = 0
    st.session_state.review_count = 0
    st.session_state.review_words = []
    st.session_state.finished = False


init_session()

st.title("独立不定詞フラッシュカード")
st.markdown(
    '<p class="subtitle-text">頻出の慣用的独立不定詞をマスターしよう</p>',
    unsafe_allow_html=True,
)

# =========================================================
# スタート画面
# =========================================================
if not st.session_state.started:
    st.write("")
    st.subheader("学習を始めましょう")
    st.markdown(
        f'<p class="base-text">全 <strong>{TOTAL}</strong> 枚のカードが登録されています。</p>',
        unsafe_allow_html=True,
    )
    shuffle_option = st.checkbox("カードの順番をシャッフルする", value=True)

    if st.button("学習をスタート", type="primary", use_container_width=True):
        order = list(range(TOTAL))
        if shuffle_option:
            random.shuffle(order)
        st.session_state.order = order
        st.session_state.index = 0
        st.session_state.flipped = False
        st.session_state.good_count = 0
        st.session_state.review_count = 0
        st.session_state.review_words = []
        st.session_state.finished = False
        st.session_state.started = True
        st.rerun()

# =========================================================
# 結果画面
# =========================================================
elif st.session_state.finished:
    st.success("全カードを学習しました！お疲れさまでした。")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="stat-box" style="background:#eef7e6; color:#3d6b1f; border-color:#6b8f3f;">
                <div style="font-size:36px; font-weight:700;">{st.session_state.good_count}</div>
                <div>覚えた (Good)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="stat-box" style="background:#fdeee0; color:#a5471f; border-color:#c0602c;">
                <div style="font-size:36px; font-weight:700;">{st.session_state.review_count}</div>
                <div>まだ不安 (Review)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    if st.session_state.review_words:
        st.subheader("復習が必要なカード一覧")
        for item in st.session_state.review_words:
            st.markdown(f"- **{item['word']}** ： {item['meaning']}")
    else:
        st.info("復習が必要なカードはありません。素晴らしい！")

    st.write("")
    if st.button("最初からやり直す", type="primary", use_container_width=True):
        reset_all()
        st.rerun()

# =========================================================
# 学習画面
# =========================================================
else:
    current_idx = st.session_state.order[st.session_state.index]
    card = flashcards[current_idx]

    # 進捗バー
    progress_num = st.session_state.index + 1
    st.progress(progress_num / TOTAL)
    st.caption(f"{progress_num} / {TOTAL} 問目")

    st.write("")

    # カード表示
    if not st.session_state.flipped:
        st.markdown(
            f"""
            <div class="flash-card front-card">
                <div class="card-label">Question</div>
                <div class="card-word">{card['word']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # 「」と（）の間で改行する
        meaning_with_break = card["meaning"].replace("」（", "」<br>（")
        st.markdown(
            f"""
            <div class="flash-card back-card">
                <div class="card-label">Answer</div>
                <div class="card-meaning">{meaning_with_break}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # コントロールボタン
    if not st.session_state.flipped:
        if st.button("カードをめくる（裏返す）", type="primary", use_container_width=True):
            st.session_state.flipped = True
            st.rerun()
    else:
        st.write("この独立不定詞の意味、覚えていましたか？")

        col_flip, col_good, col_review = st.columns(3)

        def go_to_next(is_good):
            if is_good:
                st.session_state.good_count += 1
            else:
                st.session_state.review_count += 1
                st.session_state.review_words.append(card)

            st.session_state.index += 1
            st.session_state.flipped = False

            if st.session_state.index >= TOTAL:
                st.session_state.finished = True

        with col_flip:
            if st.button("🔄 表面に戻す", use_container_width=True):
                st.session_state.flipped = False
                st.rerun()
        with col_good:
            if st.button("覚えた (Good)", use_container_width=True):
                go_to_next(True)
                st.rerun()
        with col_review:
            if st.button("まだ不安 (Review)", use_container_width=True):
                go_to_next(False)
                st.rerun()

    st.write("")
    st.divider()
    stat_col1, stat_col2 = st.columns(2)
    stat_col1.metric("覚えた", st.session_state.good_count)
    stat_col2.metric("まだ不安", st.session_state.review_count)

    st.write("")
    if st.button("終了する", use_container_width=True):
        reset_all()
        st.rerun()