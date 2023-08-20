import re


class LyricDict():
    def __init__(self, lrcPath: str):
        self.path = lrcPath
        self.dict = self.parseLrc()

    def parseLrc(self):
        ''' parse the lyric '''
        if self.path == "":
            return {0: "暂无歌词"}
        dict = {}
        with open(self.path, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
        for line in lines:
            match = re.match(r'\[(\d+):(\d+\.\d+)\](.*)', line)
            if match:
                minutes = int(match.group(1))
                seconds = float(match.group(2))
                timestamp = (minutes * 60 + seconds) * 1000
                lyrics = match.group(3).strip()
                if timestamp in dict:
                    # 换行，一般在双语歌词中
                    dict[timestamp] += f"\n{lyrics}"
                    continue
                dict[timestamp] = lyrics
        return dict

    def getLyric(self, timestamp: float):
        '''return the lryic in ms'''
        for time in list(self.dict.keys()):
            if int(time) <= timestamp:
                continue
            else:
                index = list(self.dict.keys()).index(time)-1
                if index < 0:
                    return ""
                lyric = list(self.dict.values())[index]
                return lyric

    def updatePath(self, newPath: str):
        self.path = newPath
        self.dict = self.parseLrc()


if __name__ == "__main__":
    parser = LyricDict("resource\たぶん-YOASOBI.lrc")
    print(parser.getLyric(40000))
