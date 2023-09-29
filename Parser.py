import re
from math import floor
from mutagen import File


class Lyric:

    def __init__(self, lrcPath: str):
        self._path = lrcPath
        self.dict = self.parseLrc()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: str):
        self._path = value
        self.dict = self.parseLrc()

    # def __setItem__(self, key, value):
    #     self.dict[key] = value
    # def __delItem__(self, key):
    #     del self.dict[key]

    def parseLrc(self):
        """parse the lyric"""
        if self._path == "":
            return {0: "暂无歌词"}
        dict = {}
        with open(self._path, "r", encoding="UTF-8") as f:
            lines = f.readlines()
        for line in lines:
            match = re.match(r"\[(\d+):(\d+\.\d+)\](.*)", line)
            if match:
                minutes = int(match.group(1))
                seconds = float(match.group(2))
                timestamp = (minutes * 60 + seconds) * 1000
                lyric = match.group(3).strip()
                if timestamp in dict:
                    # 换行，一般在双语歌词中
                    dict[timestamp] += f"\n{lyric}"
                    continue
                dict[timestamp] = lyric
        return dict

    def getLyric(self, time: float):
        """return the lryic in ms"""
        # 返回距离歌词最近且大于当前时间的时间戳（有点乱。。摆了。。）
        for timestamp in self.AllTime:
            if timestamp >= time :
                if self.indexOf(timestamp)-1 < 0:
                    return self.AllLyric[0]
                return self.AllLyric[self.indexOf(timestamp)-1]
            else:
                if self.AllTime.index(timestamp) == len(self.AllTime)-1:
                    return self.AllLyric[self.indexOf(timestamp)]
                continue

    @property
    def AllTime(self):
        return list(self.dict.keys())

    @property
    def AllLyric(self):
        return list(self.dict.values())

    def indexOf(self, timestamp: int | float):
        return self.AllTime.index(timestamp)

    # def updatePath(self, newPath: str):
    #     self.path = newPath
    #     self.dict = self.parseLrc()


class Music:

    def __init__(self, musicPath: str) -> None:
        self.path = musicPath
        self.id: dict = File(musicPath, easy=True)

    @property
    def Title(self) -> str:
        title = ""
        for item in self.id.get("title", "未知歌曲"):
            title += item
        return title

    @property
    def Artist(self) -> str:
        artist = ""
        for item in self.id.get("artist", "未知艺术家"):
            artist += item
        return artist

    @property
    def Album(self) -> str:
        album = ""
        for item in self.id.get("album", "未知专辑"):
            album += item
        return album

    @property
    def Genre(self) -> str:
        genre = ""
        for item in self.id.get("genre", "未知流派"):
            genre += item
        return genre

    @property
    def Track(self) -> str:
        track = ""
        for item in self.id.get("track", ""):
            track += item
        return track

    @property
    def Year(self) -> str:
        year = ""
        for item in self.id.get("date", "未知年代"):
            year += item
        return year

    @property
    def Length(self) -> str:
        min, sec = divmod(int(self.id.info.length), 60)
        return f"{min:02d}:{sec:02d}"

    @Title.setter
    def Title(self, value: str):
        self.id["title"] = value

    @Artist.setter
    def Artist(self, value: str):
        self.id["artist"] = value

    @Album.setter
    def Album(self, value: str):
        self.id["album"] = value

    @Genre.setter
    def Genre(self, value: str):
        self.id["genre"] = value

    @Track.setter
    def Track(self, value: str):
        self.id["track"] = value

    @Year.setter
    def Year(self, value: str):
        self.id["date"] = value


if __name__ == "__main__":
    # For testing
    parser = Lyric("resource\たぶん-YOASOBI.lrc")
    parser.path = (
        r"resource\So Far Away-Martin Garrix,David Guetta,Jamie Scott,Romy Dya.lrc")
    music = Music(r"resource\たぶん-YOASOBI.mp3")
    music.Title = "たぶん"
    music.id.save()
    print(music.id)
