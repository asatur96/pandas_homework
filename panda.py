import pandas as pd
import explanations
import matplotlib.pyplot

def clean_data(frame):
    frame.dropna(axis=1, how='all', thresh=None, subset=None, inplace=True)
    export_csv = frame.to_csv('clean_data.csv')

#první úkol
def accident_count(frame):
    ac = len(frame.index)
    print(f'V roce 2018 PČR zaznamenala {ac} nehod')
    return ac

#druhý úkol 
def fatal_accident_percent(frame, ac):
    usmrceno_osob = frame['usmrceno_osob']
    fa = len(usmrceno_osob[usmrceno_osob > 0])
    percent = (fa / ac) * 100
    print(f'{percent} procent zaznamenaných nehod byli smrtelnými.')

#třetí úkol
def killed_people_count(frame):
    kp = frame[(frame['druh_pevne_prekazky'] == 3) & (frame['usmrceno_osob'] > 0)]
    kpc = kp['usmrceno_osob'].sum()
    print(f'{kpc} lidí zemřelo při srážce s odrazníkem, patníkem, sloupkem dopravní značky apod.')

#čtvrtý úkol
def tram_fatal_station(frame):
    tram = frame['situovani_nehody_na_komunikaci']
    tram_accidents_count = len(tram[tram == 7])
    tram_fatal = len(frame[(frame['usmrceno_osob'] > 0) & (frame['situovani_nehody_na_komunikaci'] == 7)])
    percent = (tram_fatal / tram_accidents_count) * 100
    print(f'{percent} procent zaznamenaných nehod, které se staly na kolejích tramvaje, byli smrtelnými.')
    
#pátý úkol
def car_brands_graph(frame):
    x_list = []
    y_list = []

    brands_unique = frame['vyrobni_znacka_motoroveho_vozidla'].unique()
    count = 0
    for brand in brands_unique:
        if brand == 0:
            continue
        size = len(frame[(frame['vyrobni_znacka_motoroveho_vozidla'] == brand)])
        if size > 50:
            zatacka = len(frame[(frame['vyrobni_znacka_motoroveho_vozidla'] == brand) & (frame['smerove_pomery'] == 3)])
            brand_name = explanations.decode_key['vyrobni_znacka_motoroveho_vozidla'][brand]
            percent = (zatacka / size) * 100
            x_list.append(brand_name)
            y_list.append(percent)
            count += 1
    x = list(range(count))

    matplotlib.pyplot.scatter(x_list, y_list, s=10)
    matplotlib.pyplot.xticks(x, x_list, rotation='vertical')
    matplotlib.pyplot.xlabel("Brand")
    matplotlib.pyplot.ylabel("Percent")
    matplotlib.pyplot.savefig('graph.png')


def proces_data():
    list_of_frames = []
    for key in explanations.file_names:
        df = pd.read_csv('data/' + key, encoding='iso-8859-2', sep=';', header=None)
        df.columns = explanations.main_columns
        df['kraj'] = explanations.file_names[key]
        list_of_frames.append(df)

    frame = pd.concat(list_of_frames, axis=0, ignore_index=True)

    clean_data(frame)

    ac = accident_count(frame)
    fatal_accident_percent(frame, ac)
    killed_people_count(frame)
    tram_fatal_station(frame)
    car_brands_graph(frame)

if __name__ == '__main__':
    proces_data()