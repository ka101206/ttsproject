# formatter.py
import pykakasi

class TextFormatter:
    def __init__(self):
        self.kks = pykakasi.kakasi()

    def process(self, text, lang, mode):
        if lang != "Japanese" or mode == "なし":
            return text

        result = self.kks.convert(text)
        formatted_text = ""

        override_dict = {
            "入っ": "はいっ",
            "入る": "はいる",
            "厚": "あつ",
            "切り": "ぎり",
            "辛い": "からい",
            "辛": "から"
        }

        for item in result:
            orig = item['orig']
            hira = item['hira']
            kana = item['kana']
            
            if orig in override_dict:
                hira = override_dict[orig]
                kana = override_dict[orig]

            if mode == "ふりがな":
                # Check if it's already Hiragana/Katakana
                is_kana_already = (orig == hira or orig == kana)
                if not is_kana_already and hira.strip():
                    formatted_text += f"{orig}({hira})"
                else:
                    formatted_text += orig
            
            elif mode == "かなのみ":
                # Keep Katakana, convert others to Hiragana
                is_katakana = (orig == kana and orig != hira)
                formatted_text += orig if is_katakana else hira

        return formatted_text