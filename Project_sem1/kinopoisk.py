import json
import os
import pickle
import time
import sys

class Movie:
    def __init__(self, name, director, actors, tags):
        self._name = name
        self._director = director
        self._actors = set(actors)
        self._tags = tags

    def __str__(self):
        return self._name + "  " + self._director + "  " + str(self._actors) + "  " + str(self._tags)

    def print(self):
        print('"' + self._name + '"' + "  " + self._director + "  ", end = "")
        print(self._actors, end = "\n")
        print(self._tags, end = "\n\n")

    def settag(self, tag):
        self._tags.add(tag)

    def get_dir(self):
        return self._director

    def get_actors(self):
        return self._actors

    def get_tags(self):
        return self._tags

    def get_name(self):
        return self._name



def find_word(String, pat):
    i = 0
    while(i < len(String)):
        if((String[i] == pat[0]) or (String[i] == pat[0].upper())):
            j = 1
            while ((j < len(pat)) and (i + j < len(String)) and (String[i + j] == pat[j])):
                j += 1
            if (j == len(pat)): return True
            i = i + j
        else:
            i += 1
    return False



def write_people():
    actors_id1 = {}
    directors_id1 = {}
    with open("C://Users/fomiu/Desktop/files_for_parsing/ml-latest/ActorsDirectorsNames_IMDB.txt") as f:
        # for i in range(0, 101):
        counter = 0
        flag = False
        while (not flag):
            try:
                tmp = f.readline()
            except UnicodeDecodeError:
                continue
            if (tmp == ""):
                flag = True
                continue
            CH = tmp.split("\t")
            try:
                if ("actor" in CH[4] or "actress" in CH[4]):
                    actors_id1[CH[0]] = CH[1]
                if ("director" in CH[4]):
                    directors_id1[CH[0]] = CH[1]
            except IndexError:
                continue
            if (counter % 10000 == 0):
                print(counter, CH[0], CH[1])
            counter += 1
    with open("C://Users/fomiu/Desktop/files_for_parsing/actors_id.json", 'w') as f:
        json.dump(actors_id1, f)
        f.close()
    with open("C://Users/fomiu/Desktop/files_for_parsing/directors_id.json", 'w') as f:
        json.dump(directors_id1, f)
        f.close()



def write_film():
    films = {}
    with open("C://Users/fomiu/Desktop/files_for_parsing/ml-latest/MovieCodes_IMDB.tsv") as f:
        flag = False
        prev = "tt0000001"
        # for i in range(0, 101):
        counter = 0
        while (not flag):
            try:
                tmp = f.readline()
            except UnicodeDecodeError:
                continue
            if (tmp == ""):
                flag = True
                continue
            CH = tmp.split("\t")
            try:
                if ((CH[3] == "US" or CH[3] == "GB") and (CH[0] != prev)):
                    films[CH[0]] = CH[2]
                    prev = CH[0]
            except IndexError:
                continue
            if (counter % 10000 == 0):
                print(counter, CH[0], CH[2])
            counter += 1
        f.close()
    with open("C://Users/fomiu/Desktop/files_for_parsing/films.json", 'w') as f:
        json.dump(films, f)
        f.close()



def films_dictionary(films, actors_id, directors_id):
    film_dict = {}
    with open("C://Users/fomiu/Desktop/files_for_parsing/ml-latest/ActorsDirectorsCodes_IMDB.tsv") as f:
        prev = "tt0000001"
        actors = set()
        director = ""
        name = ""
        flag = False
        counter = 0
        #for i in range(0, 101):
        while (not flag):
            try:
                tmp = f.readline()
            except UnicodeDecodeError:
                continue
            if (tmp == ""):
                flag = True
                continue
            CH = tmp.split("\t")
            if (prev != CH[0] and CH[0] in films):

                film_dict[name] = Movie(name, director, actors, set())
                actors.clear()
                director = ""
                name = films[CH[0]]

                try:
                    CH[3] = CH[3].replace("\n", "")
                    CH[3] = CH[3].replace(",", "")
                    CH[3] = CH[3].replace(" ", "")
                    CH[3] = CH[3].replace('"', "")
                    if (CH[3] == "director"):
                        director = directors_id[CH[2]]
                    if (CH[3] == "actor"):
                        actors.add(actors_id[CH[2]])
                except (KeyError, IndexError):
                    print(CH[0])
                except IndexError:
                    print(CH[0])
                prev = CH[0]
            if (prev == CH[0]):
                try:
                    CH[3] = CH[3].replace("\n", "")
                    CH[3] = CH[3].replace(",", "")
                    CH[3] = CH[3].replace(" ", "")
                    CH[3] = CH[3].replace('"', "")
                    if (CH[3] == "director"):
                        director = directors_id[CH[2]]
                    if (CH[3] == "actor"):
                        actors.add(actors_id[CH[2]])
                except KeyError:
                    print(CH[0])
                except IndexError:
                    print(CH[0])
            if (counter % 100000 == 0):
                print(counter, "000000000000000")
            counter += 1
        f.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/films_dict_temp.pkl', 'wb') as output:
        pickle.dump(film_dict, output, pickle.HIGHEST_PROTOCOL)
        output.close()


def save_tags():
    tags = {}
    with open("C://Users/fomiu/Desktop/files_for_parsing/ml-latest/TagCodes_MovieLens.csv") as f:
        tmp = f.readline()
        counter = 0
        flag = False
        while (not flag):
            tmp = f.readline()
            if(tmp == ""):
                flag = True
                continue
            tmp = tmp.split(",")
            tags[tmp[0]] = tmp[1]
            if (counter % 25 == 0):
                print(tmp[0], tmp[1])
            counter += 1
    with open('C://Users/fomiu/Desktop/files_for_parsing/tags.json', 'wb') as f:
        json.dump(tags, f)
        f.close()


def moovie_convert():
    convert = {}
    with open("C://Users/fomiu/Desktop/files_for_parsing/ml-latest/links_IMDB_MovieLens.csv") as f:
        tmp = f.readline()
        counter = 0
        flag = False
        while (not flag):
            tmp = f.readline()
            if (tmp == ""):
                flag = True
                continue
            tmp = tmp.split(",")
            convert[tmp[0]] = "tt" + tmp[1].rstrip()
            if (counter % 500 == 0):
                print(tmp[0], convert[tmp[0]])
            counter += 1
        f.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/convert.json', 'w') as f:
        json.dump(convert, f)
        f.close()


def people_dictionary(film_dict, films):
    actors_dict = {}
    directors_dict = {}
    with open("C://Users/fomiu/Desktop/files_for_parsing/ml-latest/ActorsDirectorsNames_IMDB.txt") as f:
        counter = 0
        flag = False
        tmp = f.readline()
        while (not flag):
            try:
                tmp = f.readline()
            except UnicodeDecodeError:
                continue
            if (tmp == ""):
                flag = True
                continue
            CH = tmp.split("\t")
            try:
                fms = CH[5].split(",")
                fms1 = set()
                for i in range(0, len(fms)):
                    try:
                        fms[i] = fms[i].replace("\n", "")
                        lol1 = films[fms[i]]
                        lol = film_dict[lol1]
                        fms1.add(lol)
                    except KeyError:
                        pass
                if (find_word(CH[4], "actor") or find_word(CH[4], "actress")):
                    actors_dict[CH[1]] = fms1
                if (find_word(CH[4], "director")):
                    directors_dict[CH[1]] = fms1
            except IndexError:
                continue
            if (counter % 10000 == 0):
                print(counter, CH[1])
            counter += 1
    with open('C://Users/fomiu/Desktop/files_for_parsing/actors_dict.pkl', 'wb') as output:
        pickle.dump(actors_dict, output, pickle.HIGHEST_PROTOCOL)
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/directors_dict.pkl', 'wb') as output:
        pickle.dump(directors_dict, output, pickle.HIGHEST_PROTOCOL)
        output.close()


def tags_dictionary(film_dict, convert, films):
    TAGS_dict = {}
    for i in range(1, 1129):
        TAGS_dict[str(i)] = set()
    with open("C://Users/fomiu/Desktop/files_for_parsing/ml-latest/TagScores_MovieLens.csv") as f:
        C = 0
        tmp = f.readline()
        C += sys.getsizeof(tmp)
        counter = 0
        flag = False
        while (not flag):
            tmp = f.readline()
            C += sys.getsizeof(tmp)
            if (tmp == ""):
                flag = True
                continue
            tmp1 = tmp.split(",")
            tmp1[2] = tmp1[2].replace("\n", "")
            if(float(tmp1[2]) >= 0.5):
                try:
                    lol = convert[tmp1[0]]
                    lol2 = films[lol]
                    TAGS_dict[tmp1[1]].add(lol2)
                except KeyError:
                    pass

                try:
                    film_dict[films[convert[tmp1[0]]]].settag(tmp1[1])

                except KeyError:
                    pass
            if(counter%10000 == 0):
                try:
                    print(counter, films[convert[tmp1[0]]])
                except KeyError:
                    print(counter)
            counter += 1
        print("\n" + str(int(C/8192)) + "KB")
        f.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/films_dict.pkl', 'wb') as output:
        pickle.dump(film_dict, output, pickle.HIGHEST_PROTOCOL)
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/tags_dict.pkl', 'wb') as output:
        pickle.dump(TAGS_dict, output, pickle.HIGHEST_PROTOCOL)
        output.close()



def find_similar(filename, film_dict, actors_dict, directors_dict, tags_dict):
    similar = {}
    films = set()
    try:
        film = film_dict[filename]
    except KeyError:
        print("sorry there's no such film in dataset :(")
        return ["#$#"]

    director = film.get_dir()
    try:
        films = directors_dict[director]
        for i in films:
            D = 1
            try:
                A = len(film.get_actors() & i.get_actors()) / len(film.get_actors())
            except ZeroDivisionError:
                A = 0

            try:
                T = len(film.get_tags() & i.get_tags()) / len(film.get_tags())
            except ZeroDivisionError:
                T = 0
            S = 0.2*D + 0.3*A + 0.5*(T**(0.25))
            similar[i.get_name()] = S
        films = set()
    except KeyError: pass


    actors = film.get_actors()
    for i in actors:
        try:
            films = actors_dict[i]
            for j in films:
                if(film.get_dir() == j.get_dir()):
                    D = 1
                else: D = 0

                try:
                    A = len(film.get_actors() & j.get_actors()) / len(film.get_actors())
                except ZeroDivisionError:
                    A = 0

                try:
                    T = len(film.get_tags() & j.get_tags()) / len(film.get_tags())
                except ZeroDivisionError:
                    T = 0

                S = 0.2*D + 0.3*A + 0.5*(T**(0.25))
                similar[j.get_name()] = S
            films = set()
        except KeyError: pass

    tags = film.get_tags()
    for i in tags:
        try:
            films = tags_dict[i]
            for j in films:
                try:
                    obj = film_dict[j]
                except KeyError: continue

                if (film.get_dir() == obj.get_dir()):
                    D = 1
                else:
                    D = 0

                try:
                    print(film.get_name(), obj.get_name(), str(film.get_actors() & obj.get_actors()))
                    A = len(film.get_actors() & obj.get_actors()) / len(film.get_actors())
                except ZeroDivisionError:
                    A = 0

                try:
                    T = len(film.get_tags() & obj.get_tags()) / len(film.get_tags())
                except ZeroDivisionError:
                    T = 0

                S = 0.2*D + 0.3*A + 0.5*(T**(0.25))
                similar[obj.get_name()] = S
            films = set()
        except KeyError: pass

    best_ind = [-1]*5
    best_fit = ["-1"]*5
    flag = False
    try:
        similar.pop(filename)
    except KeyError:
        pass
    for i in similar:
        for k in range(0, 5):
            if ((similar[i] > best_ind[k]) and (not flag)):
                for j in range(0, 4 - k):
                    best_ind[4 - j] = best_ind[3 - j]
                    best_fit[4 - j] = best_fit[3 - j]
                best_ind[k] = similar[i]
                best_fit[k] = i
                flag = True
        flag = False
    return best_fit


def main():
    with open('C://Users/fomiu/Desktop/files_for_parsing/films_dict_temp.pkl', 'wb') as output:
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/films_dict.pkl', 'wb') as output:
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/tags_dict.pkl', 'wb') as output:
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/actors_dict.pkl', 'wb') as output:
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/directors_dict.pkl', 'wb') as output:
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/convert.json', 'wb') as output:
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/films.json', 'wb') as output:
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/tags.json', 'wb') as output:
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/actors_id.json', 'wb') as output:
        output.close()
    with open('C://Users/fomiu/Desktop/files_for_parsing/directors_id.json', 'wb') as output:
        output.close()



    if ((os.stat("C://Users/fomiu/Desktop/files_for_parsing/actors_id.json").st_size == 0) and
            (os.stat("C://Users/fomiu/Desktop/files_for_parsing/directors_id.json").st_size == 0)):
        write_people()
    if (((os.stat("C://Users/fomiu/Desktop/files_for_parsing/films.json").st_size == 0))):
        write_film()
    if (os.stat('C://Users/fomiu/Desktop/files_for_parsing/tags.json').st_size == 0):
        save_tags()
    if (os.stat('C://Users/fomiu/Desktop/files_for_parsing/convert.json').st_size == 0):
        moovie_convert()

    film_dict = {}
    if(os.stat("C://Users/fomiu/Desktop/files_for_parsing/films_dict_temp.pkl").st_size == 0):
        with open("C://Users/fomiu/Desktop/files_for_parsing/actors_id.json") as f:
            actors_id = json.load(f)
        with open("C://Users/fomiu/Desktop/files_for_parsing/directors_id.json") as f:
            directors_id = json.load(f)
        with open("C://Users/fomiu/Desktop/files_for_parsing/films.json") as f:
            films = json.load(f)
        print("gooooo")
        films_dictionary(films, actors_id, directors_id)

    convert = {}
    if (os.stat('C://Users/fomiu/Desktop/files_for_parsing/tags_dict.pkl').st_size == 0):
        with open("C://Users/fomiu/Desktop/files_for_parsing/convert.json") as f:
            convert = json.load(f)
        with open("C://Users/fomiu/Desktop/files_for_parsing/films.json") as f:
            films = json.load(f)
        with open("C://Users/fomiu/Desktop/files_for_parsing/films_dict_temp.pkl", 'rb') as f:
            film_dict = pickle.load(f)
        tags_dictionary(film_dict, convert, films)

    with open("C://Users/fomiu/Desktop/files_for_parsing/films_dict_temp.pkl", 'rb') as f:
        film_dict = pickle.load(f)
    if((os.stat("C://Users/fomiu/Desktop/files_for_parsing/actors_dict.pkl").st_size == 0) or
            os.stat("C://Users/fomiu/Desktop/files_for_parsing/directors_dict.pkl").st_size == 0):
        with open("C://Users/fomiu/Desktop/files_for_parsing/films.json") as f:
            films = json.load(f)
        people_dictionary(film_dict, films)


    films_dict = {}
    print("loading films list")
    with open('C://Users/fomiu/Desktop/files_for_parsing/films_dict.pkl', 'rb') as Input:
        films_dict = pickle.load(Input)
    TAGS_dict = {}
    print("loading tags list")
    with open('C://Users/fomiu/Desktop/files_for_parsing/tags_dict.pkl', 'rb') as Input:
        TAGS_dict = pickle.load(Input)
    directors_dict = {}
    print("loading directors list")
    with open('C://Users/fomiu/Desktop/files_for_parsing/directors_dict.pkl', 'rb') as Input:
        directors_dict = pickle.load(Input)
    actors_dict = {}
    print("loading actors list")
    with open('C://Users/fomiu/Desktop/files_for_parsing/actors_dict.pkl', 'rb') as Input:
        actors_dict = pickle.load(Input)


    print("\n\n")
    flag = False
    while(not flag):
        Name = input("Enter the name of the film: ")
        if(Name == ""):
            flag = True
            continue
        same = find_similar(Name, film_dict, actors_dict, directors_dict, TAGS_dict)
        if(same[0] == "#$#"):
            continue
        Film = film_dict[Name]
        if(Film.get_dir() != ""):
            print("director: " + str(Film.get_dir()))
        if(Film.get_actors() != ""):
            acts = Film.get_actors()
            print("actors:   ", end = "")
            for i in acts:
                print(i, end = ";  ")
        print("\n")

        print("\nyou could like:")
        for i in same:
            if(i != "-1"):
                print(i)
        print("\n")



if __name__ == "__main__": main()
