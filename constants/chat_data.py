"""
constants/chat_data.py — App constants, modes, moods, daily content
"""
import datetime
import os

APP_NAME    = "AYA AI"
APP_SLOGAN  = "مساعدتك الذكية الشخصية ✨"
APP_VERSION = "2.1.0"

GROQ_MODEL  = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_TOKENS  = int(os.getenv("MAX_TOKENS", "1500"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.75"))

MODES = ["💬 عام", "🇨🇳 صيني", "💻 برمجة", "📚 مذاكرة"]

MODE_META = {
    "💬 عام": {
        "bg":     "rgba(244,67,138,0.12)",
        "fg":     "#ff7eb6",
        "border": "rgba(244,67,138,0.3)",
        "shadow": "rgba(244,67,138,0.1)",
        "label":  "💬 وضع المحادثة العامة",
    },
    "🇨🇳 صيني": {
        "bg":     "rgba(167,139,250,0.12)",
        "fg":     "#c4b5fd",
        "border": "rgba(167,139,250,0.3)",
        "shadow": "rgba(124,58,237,0.1)",
        "label":  "🇨🇳 وضع اللغة الصينية",
    },
    "💻 برمجة": {
        "bg":     "rgba(124,58,237,0.12)",
        "fg":     "#a78bfa",
        "border": "rgba(124,58,237,0.3)",
        "shadow": "rgba(124,58,237,0.1)",
        "label":  "💻 وضع البرمجة — Python & C++",
    },
    "📚 مذاكرة": {
        "bg":     "rgba(244,67,138,0.1)",
        "fg":     "#fda4c8",
        "border": "rgba(244,67,138,0.25)",
        "shadow": "rgba(244,67,138,0.08)",
        "label":  "📚 وضع المذاكرة والتخطيط",
    },
}

MOODS = ["😊 سعيدة", "😴 تعبانة", "😣 متوترة", "🔥 متحمسة"]

MOOD_PROMPTS = {
    "😊 سعيدة":  "The user is happy and energetic. Match her energy — be upbeat and enthusiastic.",
    "😴 تعبانة": "The user is tired. Be extra gentle, keep answers short and encouraging.",
    "😣 متوترة": "The user is stressed. Be calm and reassuring, break everything into tiny steps.",
    "🔥 متحمسة": "The user is pumped! Be energetic and challenge her a bit.",
}

DAILY_CHINESE = [
    ("我喜欢编程",         "Wǒ xǐhuān biānchéng",          "أنا أحب البرمجة"),
    ("你好，今天怎么样？",  "Nǐ hǎo, jīntiān zěnme yàng?",  "مرحبا، كيف حالك اليوم؟"),
    ("我正在学习中文",      "Wǒ zhèngzài xuéxí zhōngwén",   "أنا أتعلم الصينية"),
    ("继续努力！",          "Jìxù nǔlì!",                   "استمري في المجهود!"),
    ("你很聪明！",          "Nǐ hěn cōngmíng!",             "أنتِ ذكية جداً!"),
    ("加油！",              "Jiā yóu!",                     "يالا يا آية، قدّي!"),
    ("梦想成真",            "Mèngxiǎng chéng zhēn",         "الأحلام تتحقق"),
    ("一步一步来",          "Yī bù yī bù lái",              "خطوة خطوة"),
    ("你做得很好",          "Nǐ zuò de hěn hǎo",            "أنتِ تؤدين عملاً رائعاً"),
    ("学无止境",            "Xué wú zhǐ jìng",              "التعلم لا نهاية له"),
    ("明天会更好",          "Míngtiān huì gèng hǎo",        "الغد سيكون أفضل"),
    ("我爱学习",            "Wǒ ài xuéxí",                  "أنا أحب التعلم"),
    ("坚持就是胜利",        "Jiānchí jiùshì shènglì",       "الاستمرار هو النصر"),
    ("每天进步一点点",      "Měitiān jìnbù yī diǎndiǎn",   "تقدمي قليلاً كل يوم"),
]

MOTIVATIONS = [
    "أنتِ أقوى مما تتخيلين، استمري! 💪",
    "كل سطر كود بتكتبيه هو خطوة للأمام ✨",
    "النجاح في كل لحظة بتحاولي فيها 💖",
    "أنتِ مبدعة ومميزة، لا تنسي ذلك أبداً 🌸",
    "الصينية + البرمجة = مستقبل لا حدود له 🚀",
    "كل يوم بتتعلمي فيه حاجة جديدة هو إنجاز 🎀",
    "أنتِ على الطريق الصح، ثقي بنفسك! 💜",
    "الصعوبة دليل على إنك بتكبري 🌺",
    "أحلامك أكبر من أي عقبة 💕",
    "روحي ببطء، بس متوقفيش! 🐢✨",
]

CODING_CHALLENGES = [
    "اكتبي دالة Python تعكس string بدون [::-1]",
    "اشرحي الفرق بين list و tuple في Python",
    "اكتبي binary search من الصفر",
    "ما الـ time complexity لـ bubble sort؟",
    "اكتبي دالة تتحقق إذا كانت الكلمة palindrome",
    "اشرحي الفرق بين == و is في Python",
    "اكتبي Fibonacci بـ recursion و iteration",
    "متى نستخدم dictionary بدل list؟",
    "اكتبي decorator بسيط في Python",
    "اشرحي ما هو OOP بمثال عملي",
]

REMINDERS = [
    "💧 اشربي مياه يا آية، جسمك محتاج!",
    "🧁 خدي بريك 10 دقائق واسترخي",
    "🌸 تنفسي عميق، أنتِ تعملي رائع",
    "👀 ابعدي عن الشاشة ثانية وغمضي عينيك",
    "🍎 كلي حاجة صحية لو كنتِ جعانة",
    "🎵 اسمعي أغنية بتحبيها كريوارد ليكِ",
    "🤸 قومي اتمدي شوية، جسمك شاكرك",
]

QUICK_PROMPTS = {
    "🇨🇳 صيني": [
        ("🗣️ محادثة",      "ابدئي معي محادثة بالصيني عن يومي، علميني كيف أرد"),
        ("📝 صحّحي جملة",  "صحّحي هذه الجملة الصينية واشرحي الخطأ: 我是去学校"),
        ("📖 كلمات جديدة", "علميني 5 كلمات صينية مفيدة جديدة مع Pinyin وجملة مثال"),
    ],
    "💻 برمجة": [
        ("🐛 Debug كودي",   "ساعديني في debug كودي وشرحي الخطأ"),
        ("📊 Binary Search", "اشرحي Binary Search بأسلوب بسيط مع كود Python"),
        ("🧪 تحدي اليوم",   None),
    ],
    "📚 مذاكرة": [
        ("📅 خطة مذاكرة",  "ساعديني أعمل خطة مذاكرة ليومي"),
        ("🧠 تقنيات حفظ",  "اقترحي علي أفضل تقنيات الحفظ والاستذكار"),
        ("💪 حمّسيني",     "أنا محتاجة تحفيز قوي عشان أبدأ المذاكرة دلوقتي"),
    ],
    "💬 عام": [
        ("💬 كيف حالك؟",   "كيف حالك يا AYA؟ 💕"),
        ("🌍 ترجمة",        "ساعديني في ترجمة نص"),
        ("✨ فكرة مشروع",   "اقترحي علي فكرة مشروع مبدعة في البرمجة"),
    ],
}


def get_today_index() -> int:
    return datetime.date.today().toordinal()
