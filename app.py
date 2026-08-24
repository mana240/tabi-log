
import json
import sqlite3
from datetime import date, time
from uuid import uuid4

import pandas as pd
import requests
import streamlit as st
from streamlit_searchbox import st_searchbox


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="たびログ",
    page_icon="✈️",
    layout="centered"
)


# ============================================================
# DESIGN
# ============================================================

st.markdown("""
<style>

/* ============================================================
   全体
============================================================ */

html,
body,
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(
            180deg,
            #F9FCFF 0%,
            #F1F7FC 100%
        );
}

.block-container {
    max-width: 920px;
    padding-top: 1.2rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    padding-bottom: 6rem;
}


/* ============================================================
   フォント
============================================================ */

:root {
    --mincho:
        "Yu Mincho",
        "YuMincho",
        "Hiragino Mincho ProN",
        "MS PMincho",
        serif;
}

h1,
h2,
h3 {
    font-family: var(--mincho) !important;
    color: #153F65 !important;
}

p,
label,
input,
textarea,
button,
[data-baseweb="select"] {
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        "Noto Sans JP",
        sans-serif !important;
}


/* ============================================================
   sidebar
============================================================ */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #EEF7FF 0%,
            #F8FBFE 100%
        );
}


/* ============================================================
   通常カード
============================================================ */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 20px !important;
    border: 1px solid #D5E2ED !important;
    background: rgba(255,255,255,0.97) !important;
    box-shadow:
        0 5px 18px
        rgba(43, 83, 120, 0.06);
}


/* ============================================================
   ヘッダー
============================================================ */

.app-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5px 2px 18px 2px;
    border-bottom: 1px solid #D9E5EF;
    margin-bottom: 18px;
}

.brand {
    font-family: var(--mincho);
    font-size: 2rem;
    font-weight: 700;
    color: #1D6EA5;
    letter-spacing: 0.04em;
}

.page-name {
    font-family: var(--mincho);
    font-size: 1.6rem;
    font-weight: 700;
    color: #173C60;
}


/* ============================================================
   旅程ルール
============================================================ */

.rule-card {
    background:
        linear-gradient(
            135deg,
            #FFF9E8,
            #FFFDF4
        );
    border: 1px solid #F1D26E;
    border-radius: 16px;
    padding: 15px 18px;
    margin-bottom: 18px;
}

.rule-title {
    font-weight: 800;
    color: #594615;
    margin-bottom: 4px;
}

.rule-text {
    color: #5F5848;
}


/* ============================================================
   スタート地点
============================================================ */

.start-card {
    background: white;
    border: 1px solid #D9E5EE;
    border-radius: 18px;
    padding: 16px 18px;
    margin-bottom: 18px;
    box-shadow:
        0 5px 14px
        rgba(30, 70, 110, 0.06);
}

.start-label {
    font-size: 0.95rem;
    font-weight: 700;
    color: #295B83;
}

.start-name {
    font-family: var(--mincho);
    font-size: 1.75rem;
    color: #123B60;
    font-weight: 700;
}


/* ============================================================
   行動カード
============================================================ */

.action-header {
    font-family: var(--mincho);
    font-size: 1.45rem;
    font-weight: 900;
    color: #173E61;
    margin-bottom: 12px;
    letter-spacing: 0.02em;
}


/* ============================================================
   移動
============================================================ */

.move-section {
    background:
        linear-gradient(
            180deg,
            #F7FBFF,
            #FFFFFF
        );
    border: 1px solid #BFD8EF;
    border-radius: 18px;
    padding: 0 15px 15px 15px;
    margin-bottom: 14px;
}

.move-section-title {
    margin-left: -15px;
    margin-right: -15px;
    margin-bottom: 14px;
    background: #EFF7FF;
    border-bottom: 1px solid #C7DBED;
    border-radius: 18px 18px 0 0;
    padding: 11px 15px;
    color: #1867A0;
    font-weight: 800;
    font-size: 1.15rem;
}


/* ============================================================
   目的地
============================================================ */

.destination-section {
    background:
        linear-gradient(
            180deg,
            #FAFDF8,
            #FFFFFF
        );
    border: 1px solid #CDE2BE;
    border-radius: 18px;
    padding: 0 15px 15px 15px;
}

.destination-section-title {
    margin-left: -15px;
    margin-right: -15px;
    margin-bottom: 14px;
    background: #F2F8ED;
    border-bottom: 1px solid #D2E3C5;
    border-radius: 18px 18px 0 0;
    padding: 11px 15px;
    color: #4F7C38;
    font-weight: 800;
    font-size: 1.15rem;
}


/* ============================================================
   Google選択結果
============================================================ */

.place-selected {
    background: #FFFFFF;
    border: 1px solid #D4E1EA;
    border-radius: 13px;
    padding: 11px 13px;
    margin-top: 6px;
    margin-bottom: 8px;
}

.place-name {
    font-weight: 700;
    color: #153D60;
}

.place-address {
    font-size: 0.82rem;
    color: #738596;
}


/* ============================================================
   ボタン
============================================================ */

.stButton > button {
    width: 100%;
    min-height: 44px;
    border-radius: 12px;
    border: 1px solid #CBDDEB;
    background: #FFFFFF;
    color: #164F7B;
    font-weight: 700;
}

.stButton > button:hover {
    background: #F4FAFF;
    border-color: #75AEDD;
}

button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #1767B0,
            #247FDB
        ) !important;

    color: white !important;
    border: none !important;
    min-height: 54px !important;
    font-size: 1.05rem !important;
}


/* ============================================================
   交通手段ボタン
============================================================ */

.transport-buttons {
    margin-top: 4px;
    margin-bottom: 8px;
}

/* 選択された交通手段 */
.transport-selected-label {
    background:
        linear-gradient(
            135deg,
            #1767B0,
            #2F83D8
        );
    color: #FFFFFF;
    border: 1px solid #1767B0;
    border-radius: 12px;
    padding: 10px 6px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    text-align: center;
}

/* 未選択 */
.transport-normal-label {
    background: #FFFFFF;
    color: #173F62;
    border: 1px solid #CBDDEB;
    border-radius: 12px;
    padding: 10px 6px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    text-align: center;
}


/* ============================================================
   時刻欄
============================================================ */

[data-testid="stTimeInput"] input {
    font-size: 1.05rem !important;
}


/* ============================================================
   スマホ
============================================================ */

@media (max-width: 600px) {

    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .brand {
        font-size: 1.6rem;
    }

    .page-name {
        font-size: 1.35rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# MASTERS
# ============================================================

PREFECTURES = [
    "北海道","青森県","岩手県","宮城県","秋田県","山形県",
    "福島県","茨城県","栃木県","群馬県","埼玉県","千葉県",
    "東京都","神奈川県","新潟県","富山県","石川県","福井県",
    "山梨県","長野県","岐阜県","静岡県","愛知県","三重県",
    "滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県",
    "鳥取県","島根県","岡山県","広島県","山口県","徳島県",
    "香川県","愛媛県","高知県","福岡県","佐賀県","長崎県",
    "熊本県","大分県","宮崎県","鹿児島県","沖縄県"
]


AREA_OPTIONS = {

    "北海道": [
        "札幌",
        "定山渓",
        "小樽・キロロ・積丹",
        "ニセコ・ルスツ",
        "洞爺・登別",
        "函館・大沼",
        "旭川・層雲峡",
        "富良野・美瑛・トマム",
        "帯広・十勝",
        "釧路・阿寒",
        "網走・北見・知床",
        "千歳・支笏湖"
    ],

    "東京都": [
        "東京駅・丸の内",
        "銀座・日本橋",
        "新宿",
        "渋谷・原宿",
        "池袋",
        "浅草・上野",
        "お台場"
    ],

    "神奈川県": [
        "横浜",
        "鎌倉",
        "湘南・江の島",
        "箱根",
        "小田原"
    ],

    "京都府": [
        "京都駅周辺",
        "祇園・東山",
        "嵐山",
        "宇治",
        "天橋立"
    ],

    "大阪府": [
        "梅田",
        "難波・心斎橋",
        "天王寺",
        "大阪ベイエリア"
    ],

    "福岡県": [
        "博多",
        "天神",
        "太宰府",
        "糸島",
        "北九州"
    ],

    "沖縄県": [
        "那覇",
        "南部",
        "中部",
        "北谷",
        "恩納村",
        "名護",
        "本部",
        "宮古島",
        "石垣島"
    ]
}


PURPOSES = [
    "定番観光",
    "記念日・誕生日",
    "カップル旅行",
    "家族旅行",
    "友人旅行",
    "一人旅",
    "卒業旅行",
    "新婚旅行",
    "推し活・聖地巡礼",
    "イベント・ライブ",
    "帰省・知人訪問",
    "ワーケーション",
    "出張＋観光",
    "その他"
]


PRIORITIES = [
    "グルメ",
    "自然・絶景",
    "温泉",
    "有名観光地を多く回る",
    "ゆっくり",
    "移動時間を少なく",
    "コスパ",
    "タイパ",
    "写真映え",
    "混雑回避",
    "子ども向け",
    "雨でも楽しめる",
    "アクティビティ",
    "買い物",
    "夜まで楽しむ"
]


TRANSPORTS = [
    ("🚶", "徒歩"),
    ("🚃", "JR"),
    ("🚆", "私鉄"),
    ("🚇", "地下鉄"),
    ("🚌", "バス"),
    ("🚕", "タクシー"),
    ("🚗", "車"),
    ("🚄", "新幹線"),
    ("✈️", "飛行機"),
    ("🚢", "船"),
    ("🚲", "自転車")
]


PUBLIC_TRANSPORTS = {
    "JR",
    "私鉄",
    "地下鉄",
    "バス",
    "新幹線",
    "飛行機",
    "船"
}


# ============================================================
# GOOGLE API
# ============================================================

def google_api_key():

    try:
        return st.secrets["GOOGLE_MAPS_API_KEY"]

    except Exception:
        return None


@st.cache_data(
    ttl=300,
    show_spinner=False
)
def google_autocomplete(
    searchterm,
    context=""
):

    key = google_api_key()


    if not key:
        return []


    term = (
        searchterm
        or
        ""
    ).strip()


    if len(term) < 2:
        return []


    query = term


    if context:

        query += " " + context


    url = (
        "https://places.googleapis.com/"
        "v1/places:autocomplete"
    )


    headers = {
        "Content-Type":
            "application/json",
        "X-Goog-Api-Key":
            key
    }


    body = {
        "input": query,
        "languageCode": "ja",
        "regionCode": "JP",
        "includedRegionCodes": ["jp"]
    }


    try:

        response = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=8
        )


        if response.status_code != 200:
            return []


        data = response.json()

        results = []


        for suggestion in data.get(
            "suggestions",
            []
        ):

            prediction = suggestion.get(
                "placePrediction"
            )


            if not prediction:
                continue


            place_id = prediction.get(
                "placeId",
                ""
            )


            label = (
                prediction
                .get("text", {})
                .get("text", "")
            )


            if place_id and label:

                results.append(
                    (
                        label,
                        {
                            "place_id": place_id,
                            "label": label
                        }
                    )
                )


        return results[:5]


    except Exception:

        return []


@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def google_place_details(
    place_id
):

    key = google_api_key()


    if not key or not place_id:
        return None


    url = (
        "https://places.googleapis.com/"
        f"v1/places/{place_id}"
    )


    headers = {
        "X-Goog-Api-Key":
            key,

        "X-Goog-FieldMask":
            (
                "id,"
                "displayName,"
                "formattedAddress,"
                "location,"
                "googleMapsUri"
            )
    }


    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=8
        )


        if response.status_code != 200:
            return None


        data = response.json()


        return {
            "place_id":
                data.get("id", ""),

            "name":
                data
                .get("displayName", {})
                .get("text", ""),

            "address":
                data.get(
                    "formattedAddress",
                    ""
                ),

            "latitude":
                data
                .get("location", {})
                .get("latitude"),

            "longitude":
                data
                .get("location", {})
                .get("longitude"),

            "maps_url":
                data.get(
                    "googleMapsUri",
                    ""
                )
        }


    except Exception:

        return None


def google_place_box(
    label,
    key,
    context=""
):

    if not google_api_key():

        manual = st.text_input(
            label,
            key=f"{key}_manual",
            placeholder="場所を入力"
        )


        if not manual:
            return None


        return {
            "place_id": "",
            "name": manual,
            "address": "",
            "latitude": None,
            "longitude": None,
            "maps_url": ""
        }


    def search_func(term):

        return google_autocomplete(
            term,
            context
        )


    selected = st_searchbox(
        search_function=search_func,
        key=key,
        label=label,
        placeholder=
            "2文字以上入力すると候補が出ます",
        debounce=300,
        clear_on_submit=False,
        edit_after_submit="option"
    )


    if not selected:
        return None


    if not isinstance(
        selected,
        dict
    ):

        return None


    details = google_place_details(
        selected.get(
            "place_id",
            ""
        )
    )


    if not details:
        return None


    st.markdown(
        f"""
        <div class="place-selected">
            <div class="place-name">
                📍 {details["name"]}
            </div>
            <div class="place-address">
                {details["address"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    return details


# ============================================================
# DB
# ============================================================

conn = sqlite3.connect(
    "travel_v4.db",
    check_same_thread=False
)

cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    departure_prefecture TEXT,
    departure_area TEXT,
    destination_prefecture TEXT,
    destination_areas TEXT,
    start_date TEXT,
    end_date TEXT,
    nights INTEGER,
    companion TEXT,
    age_group TEXT,
    purposes TEXT,
    priorities TEXT,
    start_place_name TEXT,
    start_place_id TEXT,
    start_place_maps_url TEXT,
    start_place_latitude REAL,
    start_place_longitude REAL,
    overall_rating INTEGER,
    cost_rating INTEGER,
    time_rating INTEGER,
    good_points TEXT,
    regrets TEXT
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER,
    action_order INTEGER,
    day INTEGER,
    move_departure_time TEXT,
    move_arrival_time TEXT,
    destination_arrival_time TEXT,
    destination_departure_time TEXT,
    destination_area TEXT,
    note TEXT
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS transport_legs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_id INTEGER,
    leg_order INTEGER,
    transport TEXT,
    departure_name TEXT,
    departure_place_id TEXT,
    departure_maps_url TEXT,
    departure_latitude REAL,
    departure_longitude REAL,
    arrival_name TEXT,
    arrival_place_id TEXT,
    arrival_maps_url TEXT,
    arrival_latitude REAL,
    arrival_longitude REAL
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS action_spots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_id INTEGER,
    spot_order INTEGER,
    name TEXT,
    place_id TEXT,
    maps_url TEXT,
    latitude REAL,
    longitude REAL
)
""")


conn.commit()


# ============================================================
# SESSION STATE
# ============================================================

if "actions_v4" not in st.session_state:

    st.session_state.actions_v4 = [
        str(uuid4())
    ]


if "legs_v4" not in st.session_state:

    st.session_state.legs_v4 = {}


if "spots_v4" not in st.session_state:

    st.session_state.spots_v4 = {}


def ensure_children(
    action_id
):

    if action_id not in st.session_state.legs_v4:

        st.session_state.legs_v4[
            action_id
        ] = [
            str(uuid4())
        ]


    if action_id not in st.session_state.spots_v4:

        st.session_state.spots_v4[
            action_id
        ] = []


def add_action():

    new_id = str(
        uuid4()
    )

    st.session_state.actions_v4.append(
        new_id
    )

    ensure_children(
        new_id
    )


def add_leg(
    action_id
):

    ensure_children(
        action_id
    )

    st.session_state.legs_v4[
        action_id
    ].append(
        str(uuid4())
    )


def add_spot(
    action_id
):

    ensure_children(
        action_id
    )

    st.session_state.spots_v4[
        action_id
    ].append(
        str(uuid4())
    )


def remove_leg(
    action_id,
    leg_id
):

    if len(
        st.session_state.legs_v4[
            action_id
        ]
    ) <= 1:

        return


    st.session_state.legs_v4[
        action_id
    ] = [
        x
        for x
        in st.session_state.legs_v4[
            action_id
        ]
        if x != leg_id
    ]


def remove_spot(
    action_id,
    spot_id
):

    st.session_state.spots_v4[
        action_id
    ] = [
        x
        for x
        in st.session_state.spots_v4[
            action_id
        ]
        if x != spot_id
    ]


# ============================================================
# TRANSPORT SELECTOR
# ============================================================


def set_transport(
    state_key,
    transport_name
):

    st.session_state[
        state_key
    ] = transport_name


def transport_selector(
    leg_id
):

    state_key = (
        f"transport_{leg_id}"
    )


    if state_key not in st.session_state:

        st.session_state[
            state_key
        ] = "徒歩"


    selected = st.session_state[
        state_key
    ]


    # --------------------------------------------------------
    # 1行目
    # --------------------------------------------------------

    first_row = TRANSPORTS[:5]

    cols1 = st.columns(
        len(first_row)
    )


    for i, (
        icon,
        name
    ) in enumerate(
        first_row
    ):

        with cols1[i]:

            st.button(
                f"{icon} {name}",
                key=
                    f"tr1_{leg_id}_{name}",
                type=(
                    "primary"
                    if selected == name
                    else "secondary"
                ),
                use_container_width=True,
                on_click=
                    set_transport,
                args=(
                    state_key,
                    name
                )
            )


    # --------------------------------------------------------
    # 2行目
    # --------------------------------------------------------

    second_row = TRANSPORTS[5:]

    cols2 = st.columns(
        len(second_row)
    )


    for i, (
        icon,
        name
    ) in enumerate(
        second_row
    ):

        with cols2[i]:

            st.button(
                f"{icon} {name}",
                key=
                    f"tr2_{leg_id}_{name}",
                type=(
                    "primary"
                    if selected == name
                    else "secondary"
                ),
                use_container_width=True,
                on_click=
                    set_transport,
                args=(
                    state_key,
                    name
                )
            )


    return st.session_state[
        state_key
    ]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "✈️ たびログ"
)


page = st.sidebar.radio(
    "メニュー",
    [
        "🏠 ホーム",
        "✍️ 旅を投稿",
        "🔍 旅を探す",
        "📖 旅行記"
    ]
)


# ============================================================
# HOME
# ============================================================

if page == "🏠 ホーム":

    st.markdown(
        """
        <div class="app-top">
            <div class="brand">たびログ</div>
            <div class="page-name">ホーム</div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.title(
        "実際の旅から、次の旅を。"
    )


    st.write(
        "実際に旅行した人の旅程を、"
        "移動・時間・目的地まで含めて参考にできます。"
    )


# ============================================================
# POST
# ============================================================

elif page == "✍️ 旅を投稿":

    st.markdown(
        """
        <div class="app-top">
            <div class="brand">たびログ</div>
            <div class="page-name">旅を投稿</div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # 基本情報
    # --------------------------------------------------------

    with st.expander(
        "旅行の基本情報",
        expanded=True
    ):

        title = st.text_input(
            "旅行タイトル",
            placeholder=
                "例：友人と北海道3泊4日"
        )


        departure_prefecture = (
            st.selectbox(
                "出発地の都道府県",
                PREFECTURES,
                index=None
            )
        )


        departure_area = st.text_input(
            "出発地の小地域",
            placeholder=
                "例：新宿、横浜駅周辺"
        )


        destination_prefecture = (
            st.selectbox(
                "目的地の都道府県",
                PREFECTURES,
                index=None
            )
        )


        destination_areas = []


        if destination_prefecture:

            destination_areas = (
                st.multiselect(
                    "旅行全体の小地域",
                    AREA_OPTIONS.get(
                        destination_prefecture,
                        []
                    )
                )
            )


        d1, d2 = st.columns(2)


        with d1:

            trip_start_date = (
                st.date_input(
                    "旅行開始日",
                    value=date.today()
                )
            )


        with d2:

            trip_end_date = (
                st.date_input(
                    "旅行終了日",
                    value=date.today()
                )
            )


        nights = max(
            0,
            (
                trip_end_date
                -
                trip_start_date
            ).days
        )


        companion = st.selectbox(
            "同行者",
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


        purposes = st.multiselect(
            "旅行目的",
            PURPOSES
        )


        priorities = st.multiselect(
            "重視したこと",
            PRIORITIES
        )


    # --------------------------------------------------------
    # RULE
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="rule-card">
            <div class="rule-title">
                🟡 旅程入力ルール
            </div>
            <div class="rule-text">
                観光対象の都道府県に入った時点から入力
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    start_place = None


    if destination_prefecture:

        st.markdown(
            """
            <div class="start-card">
                <div class="start-label">
                    📍 観光エリア最初の出発地
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        start_place = (
            google_place_box(
                "観光エリア最初の出発地",
                "start_place_v4",
                context=
                    destination_prefecture
            )
        )


        st.caption(
            "例：新千歳空港、東京駅、那覇空港、京都駅など。"
            "観光対象エリアに入った時点の最初の出発地点を入力します。"
        )


        if (
            start_place
            and
            start_place.get(
                "maps_url"
            )
        ):

            st.link_button(
                "📍 Google Mapsで確認",
                start_place[
                    "maps_url"
                ]
            )


    else:

        st.info(
            "目的地の都道府県を先に選択してください。"
        )


    # --------------------------------------------------------
    # SCHEDULE
    # --------------------------------------------------------

    schedule_data = []


    for (
        action_order,
        action_id
    ) in enumerate(
        st.session_state.actions_v4,
        start=1
    ):

        ensure_children(
            action_id
        )


        with st.container(
            border=True
        ):



            # =================================================
            # ① 移動
            # =================================================

            st.markdown(
                f"""
                <div class="move-section">
                    <div class="move-section-title">
                        移動 {action_order}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


            previous_time = time(
                9,
                0
            )


            if action_order > 1:

                previous_action_id = (
                    st.session_state.actions_v4[
                        action_order - 2
                    ]
                )


                previous_key = (
                    f"destination_departure_"
                    f"{previous_action_id}"
                )


                if previous_key in st.session_state:

                    previous_time = (
                        st.session_state[
                            previous_key
                        ]
                    )


            move_departure_time = (
                st.time_input(
                    "出発時刻",
                    value=
                        previous_time,
                    key=
                        f"move_departure_"
                        f"{action_id}"
                )
            )


            st.markdown(
                "**交通手段**"
            )


            legs_for_save = []


            for (
                leg_order,
                leg_id
            ) in enumerate(
                st.session_state.legs_v4[
                    action_id
                ],
                start=1
            ):

                transport = (
                    transport_selector(
                        leg_id
                    )
                )


                departure_place = None
                arrival_place = None


                if transport in PUBLIC_TRANSPORTS:

                    c1, arrow, c2 = (
                        st.columns(
                            [5, 1, 5]
                        )
                    )


                    with c1:

                        departure_place = (
                            google_place_box(
                                "出発駅・空港",
                                f"dep_{leg_id}",
                                context=
                                    destination_prefecture
                                    or
                                    ""
                            )
                        )


                    with arrow:

                        st.markdown(
                            "<div style='text-align:center;"
                            "font-size:1.5rem;"
                            "padding-top:2rem;'>→</div>",
                            unsafe_allow_html=True
                        )


                    with c2:

                        arrival_place = (
                            google_place_box(
                                "到着駅・空港",
                                f"arr_{leg_id}",
                                context=
                                    destination_prefecture
                                    or
                                    ""
                            )
                        )


                if (
                    len(
                        st.session_state.legs_v4[
                            action_id
                        ]
                    )
                    >
                    1
                ):

                    st.button(
                        "この交通手段を削除",
                        key=
                            f"delete_leg_"
                            f"{leg_id}",
                        on_click=
                            remove_leg,
                        args=(
                            action_id,
                            leg_id
                        )
                    )


                legs_for_save.append(
                    {
                        "transport":
                            transport,

                        "departure":
                            departure_place,

                        "arrival":
                            arrival_place
                    }
                )


            st.button(
                "＋ 交通手段を追加",
                key=
                    f"add_leg_{action_id}",
                use_container_width=True,
                on_click=
                    add_leg,
                args=(
                    action_id,
                )
            )


            move_arrival_time = (
                st.time_input(
                    "到着時刻",
                    value=
                        move_departure_time,
                    key=
                        f"move_arrival_"
                        f"{action_id}"
                )
            )


            st.divider()


            # =================================================
            # ② 目的地
            # =================================================

            st.markdown(
                f"""
                <div class="destination-section-title">
                    目的地 {action_order}
                    <span style="
                        float:right;
                        font-size:0.9rem;
                        font-weight:600;
                    ">
                    到着時刻
                    {move_arrival_time.strftime("%H:%M")}
                    （移動 {action_order} の到着時刻と連動）
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )


            # -------------------------------------------------
            # 目的地エリア
            # -------------------------------------------------

            destination_area = (
                st.text_input(
                    "目的地",
                    placeholder=
                        "例：札幌、小樽、函館駅周辺",
                    key=
                        f"destination_area_"
                        f"{action_id}"
                )
            )


            st.caption(
                "小地域名・観光エリア名を入力できます。自由記述OK。"
            )


            # -------------------------------------------------
            # スポット
            # -------------------------------------------------

            st.markdown(
                "**スポット**"
            )


            spots_for_save = []


            for (
                spot_order,
                spot_id
            ) in enumerate(
                st.session_state.spots_v4[
                    action_id
                ],
                start=1
            ):


                with st.container(
                    border=True
                ):

                    spot = (
                        google_place_box(
                            f"スポット {spot_order}",
                            f"spot_{spot_id}",
                            context=
                                (
                                    destination_area
                                    or
                                    destination_prefecture
                                    or
                                    ""
                                )
                        )
                    )


                    if spot:

                        spots_for_save.append(
                            spot
                        )


                    st.button(
                        "削除",
                        key=
                            f"delete_spot_"
                            f"{spot_id}",
                        on_click=
                            remove_spot,
                        args=(
                            action_id,
                            spot_id
                        )
                    )


            st.button(
                "＋ 目的地・スポットを追加",
                key=
                    f"add_spot_"
                    f"{action_id}",
                use_container_width=True,
                on_click=
                    add_spot,
                args=(
                    action_id,
                )
            )


            destination_departure_time = (
                st.time_input(
                    "出発時刻",
                    value=
                        move_arrival_time,
                    key=
                        f"destination_departure_"
                        f"{action_id}"
                )
            )


            note = st.text_area(
                "メモ（任意）",
                placeholder=
                    "例：ランチ後に周辺を散策",
                key=
                    f"note_"
                    f"{action_id}"
            )


            schedule_data.append(
                {
                    "action_order":
                        action_order,

                    "day":
                        1,

                    "move_departure_time":
                        move_departure_time,

                    "move_arrival_time":
                        move_arrival_time,

                    "destination_arrival_time":
                        move_arrival_time,

                    "destination_departure_time":
                        destination_departure_time,

                    "destination_area":
                        destination_area,

                    "legs":
                        legs_for_save,

                    "spots":
                        spots_for_save,

                    "note":
                        note
                }
            )


    # --------------------------------------------------------
    # ADD ACTION
    # --------------------------------------------------------

    st.button(
        "＋ 行動を追加",
        use_container_width=True,
        on_click=
            add_action
    )


    # --------------------------------------------------------
    # RATING
    # --------------------------------------------------------

    with st.expander(
        "旅行の評価",
        expanded=False
    ):

        overall_rating = st.slider(
            "総合満足度",
            1,
            5,
            4
        )


        cost_rating = st.slider(
            "コスパ",
            1,
            5,
            3
        )


        time_rating = st.slider(
            "タイパ",
            1,
            5,
            3
        )


        good_points = st.text_area(
            "良かった点"
        )


        regrets = st.text_area(
            "反省点"
        )


    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    if st.button(
        "✈ この旅行を投稿する",
        type="primary",
        use_container_width=True
    ):

        if not title.strip():

            st.error(
                "旅行タイトルを入力してください。"
            )


        elif not destination_prefecture:

            st.error(
                "目的地の都道府県を選択してください。"
            )


        elif not start_place:

            st.error(
                "旅程のスタート地点を入力してください。"
            )


        else:

            cur.execute("""
            INSERT INTO trips (
                title,
                departure_prefecture,
                departure_area,
                destination_prefecture,
                destination_areas,
                start_date,
                end_date,
                nights,
                companion,
                age_group,
                purposes,
                priorities,
                start_place_name,
                start_place_id,
                start_place_maps_url,
                start_place_latitude,
                start_place_longitude,
                overall_rating,
                cost_rating,
                time_rating,
                good_points,
                regrets
            )
            VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )
            """, (

                title.strip(),

                departure_prefecture,

                departure_area,

                destination_prefecture,

                json.dumps(
                    destination_areas,
                    ensure_ascii=False
                ),

                str(
                    trip_start_date
                ),

                str(
                    trip_end_date
                ),

                nights,

                companion,

                age_group,

                json.dumps(
                    purposes,
                    ensure_ascii=False
                ),

                json.dumps(
                    priorities,
                    ensure_ascii=False
                ),

                start_place.get(
                    "name",
                    ""
                ),

                start_place.get(
                    "place_id",
                    ""
                ),

                start_place.get(
                    "maps_url",
                    ""
                ),

                start_place.get(
                    "latitude"
                ),

                start_place.get(
                    "longitude"
                ),

                overall_rating,

                cost_rating,

                time_rating,

                good_points,

                regrets
            ))


            trip_id = (
                cur.lastrowid
            )


            for action in schedule_data:

                cur.execute("""
                INSERT INTO actions (
                    trip_id,
                    action_order,
                    day,
                    move_departure_time,
                    move_arrival_time,
                    destination_arrival_time,
                    destination_departure_time,
                    destination_area,
                    note
                )
                VALUES (
                    ?,?,?,?,?,?,?,?,?
                )
                """, (

                    trip_id,

                    action[
                        "action_order"
                    ],

                    action[
                        "day"
                    ],

                    str(
                        action[
                            "move_departure_time"
                        ]
                    ),

                    str(
                        action[
                            "move_arrival_time"
                        ]
                    ),

                    str(
                        action[
                            "destination_arrival_time"
                        ]
                    ),

                    str(
                        action[
                            "destination_departure_time"
                        ]
                    ),

                    action[
                        "destination_area"
                    ],

                    action[
                        "note"
                    ]
                ))


                action_db_id = (
                    cur.lastrowid
                )


                for (
                    leg_order,
                    leg
                ) in enumerate(
                    action[
                        "legs"
                    ],
                    start=1
                ):

                    dep = leg[
                        "departure"
                    ]

                    arr = leg[
                        "arrival"
                    ]


                    cur.execute("""
                    INSERT INTO transport_legs (
                        action_id,
                        leg_order,
                        transport,
                        departure_name,
                        departure_place_id,
                        departure_maps_url,
                        departure_latitude,
                        departure_longitude,
                        arrival_name,
                        arrival_place_id,
                        arrival_maps_url,
                        arrival_latitude,
                        arrival_longitude
                    )
                    VALUES (
                        ?,?,?,?,?,?,?,?,?,?,?,?,?
                    )
                    """, (

                        action_db_id,

                        leg_order,

                        leg[
                            "transport"
                        ],

                        (
                            dep.get("name", "")
                            if dep else ""
                        ),

                        (
                            dep.get("place_id", "")
                            if dep else ""
                        ),

                        (
                            dep.get("maps_url", "")
                            if dep else ""
                        ),

                        (
                            dep.get("latitude")
                            if dep else None
                        ),

                        (
                            dep.get("longitude")
                            if dep else None
                        ),

                        (
                            arr.get("name", "")
                            if arr else ""
                        ),

                        (
                            arr.get("place_id", "")
                            if arr else ""
                        ),

                        (
                            arr.get("maps_url", "")
                            if arr else ""
                        ),

                        (
                            arr.get("latitude")
                            if arr else None
                        ),

                        (
                            arr.get("longitude")
                            if arr else None
                        )
                    ))


                for (
                    spot_order,
                    spot
                ) in enumerate(
                    action[
                        "spots"
                    ],
                    start=1
                ):

                    cur.execute("""
                    INSERT INTO action_spots (
                        action_id,
                        spot_order,
                        name,
                        place_id,
                        maps_url,
                        latitude,
                        longitude
                    )
                    VALUES (
                        ?,?,?,?,?,?,?
                    )
                    """, (

                        action_db_id,

                        spot_order,

                        spot.get(
                            "name",
                            ""
                        ),

                        spot.get(
                            "place_id",
                            ""
                        ),

                        spot.get(
                            "maps_url",
                            ""
                        ),

                        spot.get(
                            "latitude"
                        ),

                        spot.get(
                            "longitude"
                        )
                    ))


            conn.commit()


            st.success(
                "旅行を投稿しました。"
            )


# ============================================================
# SEARCH
# ============================================================

elif page == "🔍 旅を探す":

    st.markdown(
        """
        <div class="app-top">
            <div class="brand">
                たびログ
            </div>
            <div class="page-name">
                旅を探す
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div style="
            color:#5D7183;
            margin-bottom:18px;
        ">
        実際に投稿された旅行から、
        あなたの条件に近い旅程を探します。
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # 検索条件
    # ========================================================

    with st.container(
        border=True
    ):

        st.markdown(
            "### 📍 行きたい場所"
        )


        search_prefecture = (
            st.selectbox(
                "都道府県",
                PREFECTURES,
                index=None,
                placeholder=
                    "都道府県を選択",
                key=
                    "search_prefecture_v4"
            )
        )


        search_areas = []


        if search_prefecture:

            search_areas = (
                st.multiselect(
                    "小地域・観光エリア",
                    AREA_OPTIONS.get(
                        search_prefecture,
                        []
                    ),
                    placeholder=
                        "複数選択できます",
                    key=
                        "search_areas_v4"
                )
            )


        st.divider()


        st.markdown(
            "### 🗓 旅行日程"
        )


        date_col1, date_col2 = (
            st.columns(
                2
            )
        )


        with date_col1:

            search_start_date = (
                st.date_input(
                    "旅行開始日",
                    value=date.today(),
                    key=
                        "search_start_v4"
                )
            )


        with date_col2:

            search_end_date = (
                st.date_input(
                    "旅行終了日",
                    value=date.today(),
                    key=
                        "search_end_v4"
                )
            )


        search_nights = max(
            0,
            (
                search_end_date
                -
                search_start_date
            ).days
        )


        st.info(
            f"{search_nights}泊"
            f"{search_nights + 1}日"
        )


        st.divider()


        st.markdown(
            "### 👥 あなたの条件"
        )


        condition_col1, condition_col2 = (
            st.columns(
                2
            )
        )


        with condition_col1:

            search_companion = (
                st.selectbox(
                    "誰と行きますか？",
                    [
                        "ひとり",
                        "恋人",
                        "夫婦",
                        "友人",
                        "家族",
                        "子ども連れ",
                        "その他"
                    ],
                    key=
                        "search_companion_v4"
                )
            )


        with condition_col2:

            search_age = (
                st.selectbox(
                    "年代",
                    [
                        "10代",
                        "20代",
                        "30代",
                        "40代",
                        "50代",
                        "60代以上"
                    ],
                    key=
                        "search_age_v4"
                )
            )


        search_purposes = (
            st.multiselect(
                "旅行の目的",
                PURPOSES,
                key=
                    "search_purposes_v4"
            )
        )


        search_priorities = (
            st.multiselect(
                "重視したいこと",
                PRIORITIES,
                key=
                    "search_priorities_v4"
            )
        )


    # ========================================================
    # JSON helper
    # ========================================================

    def search_json_list(
        value
    ):

        if not value:
            return []


        try:

            parsed = json.loads(
                value
            )


            if isinstance(
                parsed,
                list
            ):

                return parsed


        except Exception:
            pass


        return []


    def overlap_count(
        stored,
        wanted
    ):

        if not wanted:
            return 0


        return len(
            set(
                search_json_list(
                    stored
                )
            )
            &
            set(
                wanted
            )
        )


    def rating_stars(
        value
    ):

        try:
            number = int(
                value
            )

        except Exception:
            number = 0


        number = max(
            0,
            min(
                number,
                5
            )
        )


        return (
            "★" * number
            +
            "☆" * (
                5 - number
            )
        )


    # ========================================================
    # 検索
    # ========================================================

    if st.button(
        "🔍 実際の旅程を探す",
        type="primary",
        use_container_width=True,
        key=
            "search_button_v4"
    ):


        if not search_prefecture:

            st.warning(
                "目的地の都道府県を選択してください。"
            )


        elif (
            search_end_date
            <
            search_start_date
        ):

            st.warning(
                "旅行終了日は開始日以降にしてください。"
            )


        else:


            results = (
                pd.read_sql_query(
                    """
                    SELECT *
                    FROM trips
                    WHERE
                        destination_prefecture = ?
                        AND nights = ?
                    """,
                    conn,
                    params=[
                        search_prefecture,
                        search_nights
                    ]
                )
            )


            # =================================================
            # 小地域
            #
            # 選択している場合だけ必須一致
            # =================================================

            if (
                not results.empty
                and
                search_areas
            ):

                results = results[
                    results[
                        "destination_areas"
                    ].apply(
                        lambda value:
                            set(
                                search_areas
                            ).issubset(
                                set(
                                    search_json_list(
                                        value
                                    )
                                )
                            )
                    )
                ]


            if results.empty:

                st.markdown(
                    """
                    <div style="
                        margin-top:20px;
                        padding:20px;
                        border:1px solid #D9E5EE;
                        border-radius:16px;
                        background:#FFFFFF;
                        text-align:center;
                        color:#63788A;
                    ">
                    条件に一致する旅行は
                    まだ投稿されていません。
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            else:


                # =================================================
                # ○×判定
                # =================================================

                results[
                    "companion_match"
                ] = (
                    results[
                        "companion"
                    ]
                    ==
                    search_companion
                )


                results[
                    "age_match"
                ] = (
                    results[
                        "age_group"
                    ]
                    ==
                    search_age
                )


                results[
                    "match_count"
                ] = (
                    results[
                        "companion_match"
                    ].astype(int)
                    +
                    results[
                        "age_match"
                    ].astype(int)
                )


                results[
                    "purpose_score"
                ] = (
                    results[
                        "purposes"
                    ].apply(
                        lambda value:
                            overlap_count(
                                value,
                                search_purposes
                            )
                    )
                )


                results[
                    "priority_score"
                ] = (
                    results[
                        "priorities"
                    ].apply(
                        lambda value:
                            overlap_count(
                                value,
                                search_priorities
                            )
                    )
                )


                results = (
                    results.sort_values(
                        [
                            "match_count",
                            "purpose_score",
                            "priority_score",
                            "overall_rating"
                        ],
                        ascending=[
                            False,
                            False,
                            False,
                            False
                        ]
                    )
                )


                st.markdown(
                    f"## {len(results)}件の旅程"
                )


                st.caption(
                    "目的地・宿泊数が一致する旅行を表示。"
                    "同行者・年代が近い旅行ほど上位になります。"
                )


                # =================================================
                # 各旅行
                # =================================================

                for (
                    rank,
                    (
                        _,
                        trip
                    )
                ) in enumerate(
                    results.iterrows(),
                    start=1
                ):


                    with st.container(
                        border=True
                    ):


                        st.markdown(
                            f"### {rank}. "
                            f"{trip['title']}"
                        )


                        trip_areas = (
                            search_json_list(
                                trip[
                                    "destination_areas"
                                ]
                            )
                        )


                        destination_text = (
                            trip[
                                "destination_prefecture"
                            ]
                        )


                        if trip_areas:

                            destination_text += (
                                " / "
                                +
                                "・".join(
                                    trip_areas
                                )
                            )


                        st.caption(
                            f"📍 {destination_text}　"
                            f"🌙 {int(trip['nights'])}泊"
                        )


                        match_col1, match_col2 = (
                            st.columns(
                                2
                            )
                        )


                        with match_col1:

                            if trip[
                                "companion_match"
                            ]:

                                st.success(
                                    "○ 同行者が一致"
                                )

                            else:

                                st.warning(
                                    "× 同行者は不一致"
                                )


                        with match_col2:

                            if trip[
                                "age_match"
                            ]:

                                st.success(
                                    "○ 年代が一致"
                                )

                            else:

                                st.warning(
                                    "× 年代は不一致"
                                )


                        st.markdown(
                            "**総合評価　"
                            +
                            rating_stars(
                                trip[
                                    "overall_rating"
                                ]
                            )
                            +
                            "**"
                        )


                        if search_purposes:

                            st.caption(
                                f"旅行目的の一致："
                                f"{int(trip['purpose_score'])}"
                                f" / {len(search_purposes)}"
                            )


                        if search_priorities:

                            st.caption(
                                f"重視ポイントの一致："
                                f"{int(trip['priority_score'])}"
                                f" / {len(search_priorities)}"
                            )


                        # =========================================
                        # 旅程詳細
                        # =========================================

                        with st.expander(
                            "旅程を見る"
                        ):


                            st.markdown(
                                f"""
                                <div class="start-card">
                                    <div class="start-label">
                                        📍 観光エリア最初の出発地
                                    </div>
                                    <div class="start-name">
                                        {trip['start_place_name']}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )


                            actions_df = (
                                pd.read_sql_query(
                                    """
                                    SELECT *
                                    FROM actions
                                    WHERE trip_id = ?
                                    ORDER BY action_order
                                    """,
                                    conn,
                                    params=[
                                        int(
                                            trip[
                                                "id"
                                            ]
                                        )
                                    ]
                                )
                            )


                            for (
                                _,
                                action
                            ) in actions_df.iterrows():


                                with st.container(
                                    border=True
                                ):




                                    # =========================
                                    # ① 移動
                                    # =========================

                                    st.markdown(
                                        f"""
                                        <div class="move-section-title">
                                            移動 {int(action['action_order'])}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )


                                    st.caption(
                                        f"出発 "
                                        f"{str(action['move_departure_time'])[:5]}"
                                        f"　→　"
                                        f"到着 "
                                        f"{str(action['move_arrival_time'])[:5]}"
                                    )


                                    legs_df = (
                                        pd.read_sql_query(
                                            """
                                            SELECT *
                                            FROM transport_legs
                                            WHERE action_id = ?
                                            ORDER BY leg_order
                                            """,
                                            conn,
                                            params=[
                                                int(
                                                    action[
                                                        "id"
                                                    ]
                                                )
                                            ]
                                        )
                                    )


                                    transport_icons = {
                                        "徒歩": "🚶",
                                        "JR": "🚃",
                                        "私鉄": "🚆",
                                        "地下鉄": "🚇",
                                        "バス": "🚌",
                                        "タクシー": "🚕",
                                        "車": "🚗",
                                        "新幹線": "🚄",
                                        "飛行機": "✈️",
                                        "船": "🚢",
                                        "自転車": "🚲"
                                    }


                                    for (
                                        _,
                                        leg
                                    ) in legs_df.iterrows():


                                        transport = (
                                            leg[
                                                "transport"
                                            ]
                                        )


                                        icon = (
                                            transport_icons.get(
                                                transport,
                                                "🚩"
                                            )
                                        )


                                        # ---------------------
                                        # 交通手段を先に
                                        # ---------------------

                                        st.markdown(
                                            f"**{icon} "
                                            f"{transport}**"
                                        )


                                        # ---------------------
                                        # 駅・空港はその下
                                        # ---------------------

                                        departure_name = (
                                            leg[
                                                "departure_name"
                                            ]
                                            or
                                            ""
                                        )


                                        arrival_name = (
                                            leg[
                                                "arrival_name"
                                            ]
                                            or
                                            ""
                                        )


                                        if (
                                            departure_name
                                            or
                                            arrival_name
                                        ):

                                            route_c1, route_c2, route_c3 = (
                                                st.columns(
                                                    [5, 1, 5]
                                                )
                                            )


                                            with route_c1:

                                                st.write(
                                                    departure_name
                                                )


                                            with route_c2:

                                                st.markdown(
                                                    "<div style='"
                                                    "text-align:center;"
                                                    "font-size:1.3rem;'>"
                                                    "→"
                                                    "</div>",
                                                    unsafe_allow_html=True
                                                )


                                            with route_c3:

                                                st.write(
                                                    arrival_name
                                                )


                                    st.divider()


                                    # =========================
                                    # ②目的地
                                    # =========================

                                    st.markdown(
                                        f"""
                                        <div class="destination-section-title">
                                            目的地 {int(action['action_order'])}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )


                                    st.caption(
                                        f"到着 "
                                        f"{str(action['destination_arrival_time'])[:5]}"
                                        f"　→　"
                                        f"出発 "
                                        f"{str(action['destination_departure_time'])[:5]}"
                                    )


                                    area_name = (
                                        action[
                                            "destination_area"
                                        ]
                                        or
                                        ""
                                    )


                                    if area_name:

                                        st.markdown(
                                            f"**目的地："
                                            f"{area_name}**"
                                        )


                                    spots_df = (
                                        pd.read_sql_query(
                                            """
                                            SELECT *
                                            FROM action_spots
                                            WHERE action_id = ?
                                            ORDER BY spot_order
                                            """,
                                            conn,
                                            params=[
                                                int(
                                                    action[
                                                        "id"
                                                    ]
                                                )
                                            ]
                                        )
                                    )


                                    for (
                                        _,
                                        spot
                                    ) in spots_df.iterrows():


                                        st.markdown(
                                            f"📍 **{spot['name']}**"
                                        )


                                        if spot[
                                            "maps_url"
                                        ]:

                                            try:

                                                st.link_button(
                                                    "Google Mapsで確認",
                                                    spot[
                                                        "maps_url"
                                                    ]
                                                )

                                            except Exception:

                                                pass


                                    if action[
                                        "note"
                                    ]:

                                        st.caption(
                                            "メモ："
                                            +
                                            action[
                                                "note"
                                            ]
                                        )



# ============================================================
# JOURNAL
# ============================================================

elif page == "📖 旅行記":

    st.markdown(
        """
        <div class="app-top">
            <div class="brand">たびログ</div>
            <div class="page-name">旅行記</div>
        </div>
        """,
        unsafe_allow_html=True
    )


    trips_df = pd.read_sql_query(
        """
        SELECT *
        FROM trips
        ORDER BY id DESC
        """,
        conn
    )


    if trips_df.empty:

        st.info(
            "まだ投稿がありません。"
        )


    else:

        for _, trip in trips_df.iterrows():

            with st.container(
                border=True
            ):

                st.subheader(
                    trip["title"]
                )

                st.caption(
                    trip[
                        "destination_prefecture"
                    ]
                )

                with st.expander(
                    "旅程を見る"
                ):

                    actions_df = (
                        pd.read_sql_query(
                            """
                            SELECT *
                            FROM actions
                            WHERE trip_id = ?
                            ORDER BY action_order
                            """,
                            conn,
                            params=[
                                int(
                                    trip[
                                        "id"
                                    ]
                                )
                            ]
                        )
                    )


                    for _, action in (
                        actions_df.iterrows()
                    ):



                        st.markdown(
                            f"**移動 {int(action['action_order'])}** "
                            f"{str(action['move_departure_time'])[:5]}"
                            f" → "
                            f"{str(action['move_arrival_time'])[:5]}"
                        )


                        legs = (
                            pd.read_sql_query(
                                """
                                SELECT *
                                FROM transport_legs
                                WHERE action_id = ?
                                ORDER BY leg_order
                                """,
                                conn,
                                params=[
                                    int(
                                        action[
                                            "id"
                                        ]
                                    )
                                ]
                            )
                        )


                        for _, leg in legs.iterrows():

                            st.write(
                                f"🚃 {leg['transport']}"
                            )


                            if (
                                leg["departure_name"]
                                or
                                leg["arrival_name"]
                            ):

                                st.write(
                                    f"{leg['departure_name']}"
                                    f" → "
                                    f"{leg['arrival_name']}"
                                )


                        st.markdown(
                            f"**目的地 {int(action['action_order'])}："
                            f"{action['destination_area']}**"
                        )


                        spots = (
                            pd.read_sql_query(
                                """
                                SELECT *
                                FROM action_spots
                                WHERE action_id = ?
                                ORDER BY spot_order
                                """,
                                conn,
                                params=[
                                    int(
                                        action[
                                            "id"
                                        ]
                                    )
                                ]
                            )
                        )


                        for _, spot in spots.iterrows():

                            st.write(
                                f"📍 {spot['name']}"
                            )


                        st.caption(
                            f"{str(action['destination_arrival_time'])[:5]}"
                            f"〜"
                            f"{str(action['destination_departure_time'])[:5]}"
                        )
