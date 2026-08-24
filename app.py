
import streamlit as st
import sqlite3
import pandas as pd
import json
from datetime import date


# ==================================================
# 基本設定
# ==================================================

st.set_page_config(
    page_title="たびログ",
    page_icon="✈️",
    layout="centered"
)


# ==================================================
# デザイン設定
# ==================================================

st.markdown("""
<style>

/* 全体 */
.block-container {
    max-width: 820px;
    padding-top: 1.2rem;
    padding-left: 1.4rem;
    padding-right: 1.4rem;
    padding-bottom: 4rem;
}

/* 背景 */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg,
        #F8FBFF 0%,
        #F2F7FD 55%,
        #EDF5FC 100%
    );
}

/* 上部バー */
[data-testid="stHeader"] {
    background: rgba(248, 251, 255, 0.92);
}

/* サイドバー */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #EAF4FF 0%,
        #F3F8FD 100%
    );
    border-right: 1px solid #D8E8F6;
}

/* タイトル */
h1 {
    color: #104F83 !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
}

h2 {
    color: #17629B !important;
    font-weight: 750 !important;
}

h3 {
    color: #246B9E !important;
    font-weight: 700 !important;
}

/* 本文 */
p {
    line-height: 1.7;
}

/* キャプション */
[data-testid="stCaptionContainer"] {
    color: #71889D;
}

/* 通常ボタン */
.stButton > button {
    width: 100%;
    min-height: 54px;
    border-radius: 15px;
    border: 1px solid #C9DFF1;
    background: linear-gradient(
        180deg,
        #FFFFFF 0%,
        #F5FAFF 100%
    );
    color: #15578B;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 4px 14px rgba(31, 93, 145, 0.07);
}

/* ボタンhover */
.stButton > button:hover {
    border-color: #78AFE0;
    color: #0D5A97;
    box-shadow: 0 7px 18px rgba(47, 128, 237, 0.14);
}

/* フォーム送信ボタン */
.stFormSubmitButton > button {
    width: 100%;
    min-height: 58px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(
        135deg,
        #1769AA 0%,
        #2F80ED 55%,
        #4BA5ED 100%
    );
    color: white;
    font-size: 16px;
    font-weight: 800;
    box-shadow: 0 8px 20px rgba(47, 128, 237, 0.23);
}

/* 入力欄 */
input,
textarea {
    border-radius: 12px !important;
}

[data-baseweb="input"] > div {
    border-radius: 12px !important;
}

[data-baseweb="select"] > div {
    border-radius: 12px !important;
}

/* カード */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
    border: 1px solid #D7E5F2 !important;
    background: rgba(255,255,255,0.9) !important;
    box-shadow: 0 5px 18px rgba(35, 91, 140, 0.055);
    overflow: hidden;
}

/* metric */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.9);
    border: 1px solid #DAE7F2;
    border-radius: 16px;
    padding: 14px 16px;
    box-shadow: 0 4px 15px rgba(33, 86, 130, 0.05);
}

[data-testid="stMetricValue"] {
    color: #155A91;
    font-weight: 750;
}

/* expander */
[data-testid="stExpander"] {
    border-radius: 14px;
    border: 1px solid #D8E5F0;
    background: rgba(255,255,255,0.75);
}

/* divider */
hr {
    border-color: #D8E5F0 !important;
}

/* スマホ */
@media (max-width: 600px) {

    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 3rem;
    }

    h1 {
        font-size: 2rem !important;
    }

    h2 {
        font-size: 1.4rem !important;
    }

    h3 {
        font-size: 1.1rem !important;
    }
}


/* ================================
   余白を広げる
   ================================ */

.block-container {
    max-width: 860px;
    padding-top: 2.2rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
    padding-bottom: 5rem;
}

h1 {
    margin-bottom: 1.2rem !important;
}

h2 {
    margin-top: 1.4rem !important;
    margin-bottom: 1rem !important;
}

h3 {
    margin-top: 1.1rem !important;
    margin-bottom: 0.8rem !important;
}

p {
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    margin-bottom: 1.4rem;
}

hr {
    margin-top: 2rem !important;
    margin-bottom: 2rem !important;
}

[data-testid="stMetric"] {
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}

@media (max-width: 600px) {

    .block-container {
        padding-top: 1.4rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 4rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        margin-bottom: 1rem;
    }
}


/* ================================
   左余白を増やす
   ================================ */

/* メイン全体の左余白を広げる */
.block-container {
    padding-left: 2.8rem !important;
    padding-right: 1.8rem !important;
}

/* カード内の文字の左余白を増やす */
[data-testid="stVerticalBlockBorderWrapper"] {
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
}

/* 段落やテキストも少し内側へ */
p {
    padding-left: 0.2rem;
}

/* スマホ用 */
@media (max-width: 600px) {
    .block-container {
        padding-left: 1.4rem !important;
        padding-right: 1rem !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
    }
}


/* =========================================
   明朝テーマ
   ホーム・サイドバー・見出しのみ
   ========================================= */

/* 明朝フォント候補 */
:root {
    --mincho-font:
        "Hannari Mincho",
        "Yu Mincho",
        "YuMincho",
        "Hiragino Mincho ProN",
        "Hiragino Mincho Pro",
        "MS PMincho",
        "MS Mincho",
        serif;
}

/* メインタイトル */
h1 {
    font-family: var(--mincho-font) !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
}

/* セクション見出し */
h2,
h3 {
    font-family: var(--mincho-font) !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
}

/* ホーム画面などの通常テキスト */
[data-testid="stMarkdownContainer"] p {
    font-family: var(--mincho-font);
    letter-spacing: 0.015em;
}

/* サイドバー全体 */
[data-testid="stSidebar"] {
    font-family: var(--mincho-font);
}

/* サイドバータイトル */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: var(--mincho-font) !important;
}

/* サイドバー内テキスト */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    font-family: var(--mincho-font);
}

/* radioメニュー */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    font-family: var(--mincho-font) !important;
    letter-spacing: 0.02em;
}

/* カード内見出し */
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3 {
    font-family: var(--mincho-font) !important;
}

/* カード内本文 */
[data-testid="stVerticalBlockBorderWrapper"] p {
    font-family: var(--mincho-font);
}

/* =========================================
   入力欄は今のフォントを維持
   ========================================= */

input,
textarea,
button,
[data-baseweb="select"],
[data-baseweb="input"],
[data-testid="stNumberInput"],
[data-testid="stDateInput"],
[data-testid="stTimeInput"],
[data-testid="stTextInput"],
[data-testid="stTextArea"],
[data-testid="stMultiSelect"],
[data-testid="stSlider"] {
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif !important;
}

/* 入力欄のラベルも読みやすいサンセリフ */
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stNumberInput"] label,
[data-testid="stDateInput"] label,
[data-testid="stTimeInput"] label,
[data-testid="stSlider"] label {
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif !important;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# データベース
# ==================================================

conn = sqlite3.connect(
    "travel.db",
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    departure TEXT,
    destination TEXT,
    start_date TEXT,
    end_date TEXT,
    companion TEXT,
    age_group TEXT,
    purpose TEXT,
    priorities TEXT,
    overall_rating INTEGER,
    cost_rating INTEGER,
    time_rating INTEGER,
    good_points TEXT,
    regrets TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS schedule_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER,
    day INTEGER,
    start_time TEXT,
    end_time TEXT,
    place TEXT,
    activity TEXT,
    transport TEXT
)
""")

conn.commit()


# ==================================================
# 共通関数
# ==================================================

def stars(number):
    number = int(number)
    return "★" * number + "☆" * (5 - number)


def calculate_score(row):
    return (
        row["overall_rating"] * 0.5
        + row["time_rating"] * 0.3
        + row["cost_rating"] * 0.2
    )


# ==================================================
# サイドバー
# ==================================================

st.sidebar.title("✈️ たびログ")
st.sidebar.caption("REAL TRIP PLANS")

page = st.sidebar.radio(
    "メニュー",
    [
        "🏠 ホーム",
        "✍️ 旅を投稿",
        "🔍 旅を探す",
        "📖 みんなの旅行記"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "実際の旅行体験をもとに、"
    "次の旅をもっと計画しやすく。"
)


# ==================================================
# ホーム
# ==================================================

if page == "🏠 ホーム":

    st.title("✈️ たびログ")

    st.subheader(
        "実際の旅から、次の旅を見つけよう。"
    )

    st.write(
        "旅行者が実際にどこをどう回り、"
        "どのくらい満足したのか。"
        "リアルな旅行体験から、"
        "あなたの旅を考えるサービスです。"
    )

    st.divider()

    with st.container(border=True):

        st.subheader("🔍 旅を探す")

        st.write(
            "目的地・年代・同行者・"
            "重視したいポイントから、"
            "あなたに近い実際の旅行を探します。"
        )

    with st.container(border=True):

        st.subheader("✍️ 旅を投稿")

        st.write(
            "どこへ行き、何をして、"
            "どう移動したのか。"
            "実際の旅を時系列で残せます。"
        )

    with st.container(border=True):

        st.subheader("📊 リアルな評価")

        st.write(
            "総合満足度だけではなく、"
            "コスパ・タイパ・良かった点・"
            "反省点まで参考にできます。"
        )

    st.divider()

    cursor.execute(
        "SELECT COUNT(*) FROM trips"
    )

    trip_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM schedule_items"
    )

    schedule_count = cursor.fetchone()[0]

    st.subheader("たびログのデータ")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "旅行プラン",
            f"{trip_count}件"
        )

    with col2:
        st.metric(
            "登録された行程",
            f"{schedule_count}件"
        )


# ==================================================
# 投稿
# ==================================================

elif page == "✍️ 旅を投稿":

    st.title("✍️ 旅を投稿")

    st.caption(
        "あなたが実際に体験した旅行を、"
        "時系列で記録してください。"
    )


    with st.form("trip_form"):


        with st.container(border=True):

            st.subheader("1. 基本情報")

            title = st.text_input(
                "旅行タイトル",
                placeholder="例：初めての北海道3泊4日"
            )

            col1, col2 = st.columns(2)

            with col1:
                departure = st.text_input(
                    "出発地",
                    placeholder="例：東京"
                )

            with col2:
                destination = st.text_input(
                    "主な目的地",
                    placeholder="例：北海道"
                )

            col1, col2 = st.columns(2)

            with col1:
                start_date = st.date_input(
                    "旅行開始日",
                    value=date.today()
                )

            with col2:
                end_date = st.date_input(
                    "旅行終了日",
                    value=date.today()
                )


        with st.container(border=True):

            st.subheader("2. 旅行者について")

            companion = st.selectbox(
                "誰と行きましたか？",
                [
                    "ひとり",
                    "恋人",
                    "夫婦",
                    "友人",
                    "家族",
                    "子ども連れ",
                    "その他"
                ]
            )

            age_group = st.selectbox(
                "年代",
                [
                    "10代",
                    "20代",
                    "30代",
                    "40代",
                    "50代",
                    "60代以上"
                ]
            )

            purpose = st.multiselect(
                "旅行の目的",
                [
                    "観光",
                    "グルメ",
                    "自然",
                    "リラックス",
                    "温泉",
                    "写真",
                    "アクティビティ",
                    "記念日",
                    "イベント",
                    "その他"
                ]
            )


        with st.container(border=True):

            st.subheader("3. 旅行で重視したこと")

            priorities = st.multiselect(
                "重視ポイント",
                [
                    "自然",
                    "食事",
                    "リラックス",
                    "観光地周遊",
                    "コスパ",
                    "タイパ",
                    "写真映え",
                    "移動の少なさ",
                    "ホテル",
                    "アクティビティ"
                ]
            )


        with st.container(border=True):

            st.subheader("4. スケジュール")

            st.caption(
                "旅行中の行動を時系列で登録します。"
            )

            schedule_count = st.number_input(
                "登録する行動数",
                min_value=1,
                max_value=10,
                value=3,
                step=1
            )

            schedule_data = []

            for i in range(int(schedule_count)):

                st.markdown(
                    f"#### 行動 {i + 1}"
                )

                day = st.number_input(
                    "旅行何日目？",
                    min_value=1,
                    max_value=30,
                    value=1,
                    key=f"day_{i}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    start_time = st.time_input(
                        "開始時間",
                        key=f"start_time_{i}"
                    )

                with col2:
                    end_time = st.time_input(
                        "終了時間",
                        key=f"end_time_{i}"
                    )

                place = st.text_input(
                    "場所",
                    placeholder="例：小樽運河",
                    key=f"place_{i}"
                )

                activity = st.text_input(
                    "したこと",
                    placeholder="例：散策・ランチ",
                    key=f"activity_{i}"
                )

                transport = st.selectbox(
                    "移動手段",
                    [
                        "徒歩",
                        "電車",
                        "バス",
                        "車",
                        "タクシー",
                        "飛行機",
                        "船",
                        "自転車",
                        "その他"
                    ],
                    key=f"transport_{i}"
                )

                schedule_data.append({
                    "day": day,
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "place": place,
                    "activity": activity,
                    "transport": transport
                })

                if i < int(schedule_count) - 1:
                    st.divider()


        with st.container(border=True):

            st.subheader("5. 旅行の評価")

            overall_rating = st.slider(
                "旅行全体の満足度",
                1,
                5,
                4
            )

            cost_rating = st.slider(
                "コスパの良さ",
                1,
                5,
                3
            )

            time_rating = st.slider(
                "タイパの良さ",
                1,
                5,
                3
            )

            good_points = st.text_area(
                "良かった点",
                placeholder=(
                    "例：移動を札幌と小樽に絞ったので、"
                    "観光時間を多く取れた。"
                )
            )

            regrets = st.text_area(
                "反省点・改善したいところ",
                placeholder=(
                    "例：函館から札幌の移動が"
                    "思ったより長かった。"
                )
            )


        submit = st.form_submit_button(
            "この旅行を投稿する",
            use_container_width=True
        )


        if submit:

            if not title:
                st.error(
                    "旅行タイトルを入力してください。"
                )

            elif not departure:
                st.error(
                    "出発地を入力してください。"
                )

            elif not destination:
                st.error(
                    "目的地を入力してください。"
                )

            elif end_date < start_date:
                st.error(
                    "終了日は開始日以降にしてください。"
                )

            else:

                cursor.execute("""
                INSERT INTO trips (
                    title,
                    departure,
                    destination,
                    start_date,
                    end_date,
                    companion,
                    age_group,
                    purpose,
                    priorities,
                    overall_rating,
                    cost_rating,
                    time_rating,
                    good_points,
                    regrets
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    title,
                    departure,
                    destination,
                    str(start_date),
                    str(end_date),
                    companion,
                    age_group,
                    json.dumps(
                        purpose,
                        ensure_ascii=False
                    ),
                    json.dumps(
                        priorities,
                        ensure_ascii=False
                    ),
                    overall_rating,
                    cost_rating,
                    time_rating,
                    good_points,
                    regrets
                ))

                trip_id = cursor.lastrowid


                for item in schedule_data:

                    if item["place"]:

                        cursor.execute("""
                        INSERT INTO schedule_items (
                            trip_id,
                            day,
                            start_time,
                            end_time,
                            place,
                            activity,
                            transport
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            trip_id,
                            item["day"],
                            item["start_time"],
                            item["end_time"],
                            item["place"],
                            item["activity"],
                            item["transport"]
                        ))


                conn.commit()

                st.success(
                    "🎉 旅行を投稿しました！"
                )


# ==================================================
# 検索
# ==================================================

elif page == "🔍 旅を探す":

    st.title("🔍 旅を探す")

    st.caption(
        "あなたの条件に近い、"
        "実際の旅行体験を探します。"
    )


    with st.container(border=True):

        st.subheader("1. 行き先")

        destination_search = st.text_input(
            "行きたい場所",
            placeholder="例：北海道"
        )


    with st.container(border=True):

        st.subheader("2. 旅行者条件")

        companion_search = st.selectbox(
            "誰と行きますか？",
            [
                "指定なし",
                "ひとり",
                "恋人",
                "夫婦",
                "友人",
                "家族",
                "子ども連れ",
                "その他"
            ]
        )

        age_search = st.selectbox(
            "年代",
            [
                "指定なし",
                "10代",
                "20代",
                "30代",
                "40代",
                "50代",
                "60代以上"
            ]
        )


    with st.container(border=True):

        st.subheader("3. 重視したいこと")

        priority_search = st.multiselect(
            "重視ポイント",
            [
                "自然",
                "食事",
                "リラックス",
                "観光地周遊",
                "コスパ",
                "タイパ",
                "写真映え",
                "移動の少なさ",
                "ホテル",
                "アクティビティ"
            ]
        )


    search_button = st.button(
        "おすすめを探す",
        use_container_width=True
    )


    if search_button:

        query = """
        SELECT *
        FROM trips
        WHERE destination LIKE ?
        """

        params = [
            f"%{destination_search}%"
        ]


        if companion_search != "指定なし":

            query += " AND companion = ?"

            params.append(
                companion_search
            )


        if age_search != "指定なし":

            query += " AND age_group = ?"

            params.append(
                age_search
            )


        df = pd.read_sql_query(
            query,
            conn,
            params=params
        )


        if not df.empty and priority_search:

            def priority_match(x):

                try:
                    stored = json.loads(x)

                    return any(
                        p in stored
                        for p in priority_search
                    )

                except:
                    return False


            df = df[
                df["priorities"].apply(
                    priority_match
                )
            ]


        if df.empty:

            st.warning(
                "条件に合う旅行がまだありません。"
            )

        else:

            df["recommend_score"] = df.apply(
                calculate_score,
                axis=1
            )

            df = df.sort_values(
                "recommend_score",
                ascending=False
            )

            best_trip = df.iloc[0]


            st.divider()

            st.subheader(
                "✨ おすすめの参考プラン"
            )


            with st.container(border=True):

                st.markdown(
                    f"### {best_trip['title']}"
                )

                st.write(
                    f"総合評価："
                    f"{stars(best_trip['overall_rating'])}"
                )

                st.write(
                    f"おすすめスコア："
                    f"{best_trip['recommend_score']:.1f} / 5"
                )

                st.caption(
                    f"{best_trip['departure']} → "
                    f"{best_trip['destination']}"
                )


            schedule_df = pd.read_sql_query(
                """
                SELECT *
                FROM schedule_items
                WHERE trip_id = ?
                ORDER BY day, start_time
                """,
                conn,
                params=[
                    int(best_trip["id"])
                ]
            )


            if not schedule_df.empty:

                for day_number in sorted(
                    schedule_df["day"].unique()
                ):

                    st.markdown(
                        f"### DAY {day_number}"
                    )

                    day_df = schedule_df[
                        schedule_df["day"]
                        == day_number
                    ]


                    for _, item in day_df.iterrows():

                        with st.container(border=True):

                            st.markdown(
                                f"**{item['start_time'][:5]}〜"
                                f"{item['end_time'][:5]}**"
                            )

                            st.markdown(
                                f"📍 **{item['place']}**"
                            )

                            st.write(
                                item["activity"]
                            )

                            st.caption(
                                f"🚃 {item['transport']}"
                            )


            st.subheader(
                "📊 このおすすめの根拠"
            )


            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "満足度",
                    f'{df["overall_rating"].mean():.1f}'
                )

            with col2:
                st.metric(
                    "タイパ",
                    f'{df["time_rating"].mean():.1f}'
                )

            with col3:
                st.metric(
                    "コスパ",
                    f'{df["cost_rating"].mean():.1f}'
                )


            st.caption(
                f"{len(df)}件の実際の旅行投稿を"
                "参考にしています。"
            )


# ==================================================
# 旅行記
# ==================================================

elif page == "📖 みんなの旅行記":

    st.title(
        "📖 みんなの旅行記"
    )

    st.caption(
        "実際に投稿された旅行を一覧で見られます。"
    )


    df = pd.read_sql_query(
        """
        SELECT *
        FROM trips
        ORDER BY id DESC
        """,
        conn
    )


    if df.empty:

        st.info(
            "まだ旅行投稿がありません。"
        )

    else:

        for _, trip in df.iterrows():

            with st.container(border=True):

                st.subheader(
                    trip["title"]
                )

                st.caption(
                    f"📍 {trip['departure']} → "
                    f"{trip['destination']}"
                )

                st.write(
                    f"総合評価："
                    f"{stars(trip['overall_rating'])}"
                )

                st.write(
                    f"👥 {trip['companion']}・"
                    f"{trip['age_group']}"
                )


                with st.expander(
                    "この旅行の詳細を見る"
                ):

                    st.markdown(
                        "### 👍 良かった点"
                    )

                    st.write(
                        trip["good_points"]
                    )

                    st.markdown(
                        "### 🤔 反省点"
                    )

                    st.write(
                        trip["regrets"]
                    )


                    schedule = pd.read_sql_query(
                        """
                        SELECT *
                        FROM schedule_items
                        WHERE trip_id = ?
                        ORDER BY day, start_time
                        """,
                        conn,
                        params=[
                            int(trip["id"])
                        ]
                    )


                    if not schedule.empty:

                        st.markdown(
                            "### 🗓 スケジュール"
                        )


                        for day_number in sorted(
                            schedule["day"].unique()
                        ):

                            st.markdown(
                                f"#### DAY {day_number}"
                            )

                            day_df = schedule[
                                schedule["day"]
                                == day_number
                            ]


                            for _, item in day_df.iterrows():

                                st.markdown(
                                    f"**{item['start_time'][:5]}"
                                    f"〜{item['end_time'][:5]}**"
                                )

                                st.markdown(
                                    f"📍 **{item['place']}**"
                                )

                                st.write(
                                    item["activity"]
                                )

                                st.caption(
                                    f"🚃 {item['transport']}"
                                )

                                st.divider()
