import re


class PrePro:
    @staticmethod
    def filter(code):
        filtered = re.sub('//.*?$', '', code, flags=re.MULTILINE)
        return filtered+"\n"
