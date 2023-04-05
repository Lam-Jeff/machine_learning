import mkwikidata
from geopy.point import Point
from geopy.geocoders import Nominatim
import numpy as np
import datetime
import geopy.distance
import pandas as pd
from sklearn.model_selection import train_test_split

def get_city (latitude, longitude):
    """Retourne le nom de la ville s'il existe.

    :param latitude : coordonnée.
    :param longitude : coordonnée.
    :Return : le nom de la ville. NaN autrement.
    """
    geolocator = Nominatim(user_agent="test")
    try:
        location = geolocator.reverse(Point(latitude, longitude))
        if 'municipality' in location.raw['address'] :
            return location.raw['address']['municipality']
        elif 'city' in location.raw['address'] :
            return location.raw['address']['city']
        elif 'village' in location.raw['address'] :
            return location.raw['address']['village']
        else:
            return location.raw['address']['town']
    except:
        return np.nan
    

def get_population(local_name):
    """Retourne la population d'une ville si elle existe.

    :param local_name : le nom de la ville
    :Return : le nombre d'habitants. NaN autrement.
    """
    query = """
            SELECT ?population WHERE {
            SERVICE wikibase:mwapi {
                bd:serviceParam mwapi:search "$city" .    
                bd:serviceParam mwapi:language "en" .    
                bd:serviceParam wikibase:api "EntitySearch" .
                bd:serviceParam wikibase:endpoint "www.wikidata.org" .
                bd:serviceParam wikibase:limit 1 .
                ?item wikibase:apiOutputItem mwapi:item .
            }
            ?item wdt:P1082 ?population
            }
            """
    try:
        query_result = mkwikidata.run_query(query, params={'city': local_name })
        return float(query_result['results']['bindings'][0]['population']['value'])
    except : 
        return np.nan


def get_company_name (row, df_providers, companies):
    """Retourne le nom de la compagnie.

    :param row : le tuple qui stocke l'information.
    :param df_providers : le DataFrame qui possède les informations sur les providers.
    :param companies : le DataFrame qui contient le nom des compagnies.
    :Return : le tuple avec le nom de la compagnie ajoutée.
    """
    company_id =  df_providers[df_providers['id'] == row['company']].company_id.values[0]
    row['company'] = companies[companies['company_id'] == company_id].fullname.values[0]
    return row


def get_time_of_day (row, column):
    """Retourne le moment de la journée.

    :param row : le tuple qui stocke l'information.
    :param column : le nom de la colonne [arrival_ts / departure_ts]
    :Return : le tuple avec le moment de la journée ajouté.
    """
    str_time = row[column].strftime("%H:%M:%S")
    time = datetime.datetime.strptime(str_time, "%H:%M:%S")

    column_name = column + '_time_of_day'
    morning = "07:00:00"
    afternoon = "13:00:00"
    evening = "18:00:00"
    night = "00:00:00"
    morning_time = datetime.datetime.strptime(morning, "%H:%M:%S")
    afternoon_time = datetime.datetime.strptime(afternoon, "%H:%M:%S")
    evening_time = datetime.datetime.strptime(evening, "%H:%M:%S")
    night_time = datetime.datetime.strptime(night, "%H:%M:%S")
    if time > night_time and time < morning_time:
        row[column_name] = 'Nuit'
    elif time > morning_time and time < afternoon_time:
        row[column_name] = 'Matin'
    elif time > afternoon_time and time < evening_time:
        row[column_name] = 'Après-midi'
    else:
        row[column_name] = 'Soir'
    return row


def get_distance_between_cities (row, df_cities):
    """Retourne la distance entre la ville de départ et la ville d'arrivée.

    :param row : le tuple qui stocke l'information.
    :param df_cities : le DataFrame qui possède les informations sur les villes.
    :Return : le tuple avec la distance ajoutée.
    """
    coordinates_1 = df_cities[df_cities['id'] == row['o_city']].latitude.values[0], df_cities[df_cities['id'] == row['o_city']].longitude.values[0]
    coordinates_2 = df_cities[df_cities['id'] == row['d_city']].latitude.values[0], df_cities[df_cities['id'] == row['d_city']].longitude.values[0]  
    row['distance'] =  geopy.distance.geodesic(coordinates_1, coordinates_2).km
    return row


def get_info_providers (row, df_providers):
    """Retourne des informations liées au provider.

    :param row: le tuple qui stocke l'information
    :param df_providers: le DataFrame qui possède les informations.
    :Return : le tuple mis à jour.
    """
    row['has_wifi'] = df_providers[(df_providers['id'] == row['company'])]['has_wifi'].values[0]
    row['has_plug'] = df_providers[(df_providers['id'] == row['company'])]['has_plug'].values[0]
    row['has_adjustable_seats'] = df_providers[(df_providers['id'] == row['company'])]['has_adjustable_seats'].values[0]
    row['has_bicycle'] = df_providers[(df_providers['id'] == row['company'])]['has_bicycle'].values[0]
    row['transport_type'] = df_providers[(df_providers['id'] == row['company'])]['transport_type'].values[0]
    return row 


def count_number_middle_stations (row):
    """Retourne le nombre de stations intermédiaires sur un trajet.

    :param row: le tuple qui stocke l'information
    :Return : le tuple mis à jour.
    """
    middle_stations = row['middle_stations']
    if pd.notna(middle_stations):
        middle_stations = middle_stations.replace('{', '')
        middle_stations = middle_stations.replace('}', '')
        middle_stations = middle_stations.split(',')
        row['number_middle_stations'] = len(set(middle_stations))
    else :
        row['number_middle_stations'] = 0
    return row
    

def create_train_test_set(df):
    """Retourne un train et test set pour l'entrainement du modèle d'apprentissage.

    :param df : le DataFrame à diviser.
    :Return : retourne quatre Dataframes.
    """
    features = df.drop(columns=['price_in_cents'], axis=1)
    target = df['price_in_cents']

    X_train, X_test, Y_train, Y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    print(X_train.shape, X_test.shape)
    print(Y_train.shape, Y_test.shape)
    
    return X_train, X_test, Y_train, Y_test
