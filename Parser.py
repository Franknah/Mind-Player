import re
from mutagen import File

class Lyric():
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
                index = self.indexOf(time)-1
                if index < 0:
                    return ""
                lyric = list(self.dict.values())[index]
                return lyric

    def getAllTime(self):
        return list(self.dict.keys())

    def getAllLyric(self):
        return list(self.dict.values())

    def indexOf(self, timestamp: int | float):
        return self.getAllTime().index(timestamp)

    def updatePath(self, newPath: str):
        self.path = newPath
        self.dict = self.parseLrc()
    
class Music():
    def __init__(self,musicPath:str) -> None:
        self.path=musicPath
        self.id:dict=File(musicPath,easy=True)
    @property
    def Title(self) -> str:
        title = ""
        for item in self.id.get("title","未知歌曲"):
            title += item
        return  title
    @property
    def Artist(self) -> str:
        artist = ""
        for item in self.id.get("artist","未知艺术家"):
            artist += item
        return artist
    @property
    def Album(self) -> str:
        album = ""
        for item in self.id.get("album","未知专辑"):
            album += item
        return album
    @property
    def Genre(self) -> str:
        genre = ""
        for item in self.id.get("genre","未知流派"):
            genre += item
        return genre
    @property
    def Track(self) -> str:
        track = ""
        for item in self.id.get("track",""):
            track += item
        return track
    @property
    def Year(self) -> str:
        year = ""
        for item in self.id.get("date","未知年代"):
            year += item
        return year
    @property
    def Length(self) -> str:
        min, sec = divmod(int(self.id.info.length),60)
        return f"{min:02d}:{sec:02d}"

    

if __name__ == "__main__":
    # For testing
    parser = Lyric("resource\たぶん-YOASOBI.lrc")
    print(parser.getLyric(40000))
    music=Music(r"resource\たぶん-YOASOBI.mp3")
    print(music.Length)