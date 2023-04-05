import pytest
from data_exploratory.process import *

@pytest.mark.parametrize(
    'latitude, longitude, expected',
    [
        [48.866667, 2.333333, 'Paris']
    ],
)
def test_get_city(latitude, longitude, expected):
    assert get_city (latitude, longitude) == expected


@pytest.mark.parametrize(
    'local_name, expected',
    [
        ['Paris', 2145906]
    ],
)
def test_get_population(local_name, expected):
    assert get_population(local_name) == expected


def test_get_company_name():
    row_data = {'company' : ['1']
                , 'has_wifi' : ['']
                , 'has_plug' : ['']
                , 'has_adjustable_seats' : ['']
                , 'has_bicycle' : ['']
                , 'transport_type' : ['']
    }

    providers_data = {'id':['1']
                , 'company_id' : ['1']
                , 'has_wifi' : [True]
                , 'has_plug' : [True]
                , 'has_adjustable_seats' : [False]
                , 'has_bicycle' : [False]
                , 'transport_type' : ['bus']
    }
    companies_data = {'company_id' : ['1']
                , 'fullname': ['Ouibus']
    }
    row = pd.DataFrame(row_data)
    df_providers = pd.DataFrame(providers_data)
    companies = pd.DataFrame(companies_data)

    row[row['company'] == '1'] = get_company_name (row, df_providers, companies)

    assert row.iloc[0]['company'] == 'Ouibus'


def test_get_time_of_day():
    row_data = {'company' : ['1']
                , 'has_wifi' : ['']
                , 'has_plug' : ['']
                , 'has_adjustable_seats' : ['']
                , 'has_bicycle' : ['']
                , 'transport_type' : ['']
                , 'arrival_ts' : [datetime.datetime(2022, 12, 28, 13, 30, 0, 342380)]
    }

    row = pd.DataFrame(row_data)
    row = row.apply (lambda x: get_time_of_day(x, 'arrival_ts'), axis=1)
    assert row.iloc[0]['arrival_ts_time_of_day'] == 'Après-midi'


def test_get_company_name():
    row_data = {'company' : ['1']
                , 'has_wifi' : ['']
                , 'has_plug' : ['']
                , 'has_adjustable_seats' : ['']
                , 'has_bicycle' : ['']
                , 'transport_type' : ['']
                , 'arrival_ts' : [datetime.datetime(2022, 12, 28, 13, 30, 0, 342380)]
                , 'o_city' : ['542']
                , 'd_city' : ['611']
                , 'distance' : [1000]
    }

    cities_data = {'id' : ['542', '611', '11']
                    , 'latitude' : [48.866667, 48.866667, 11.222]
                    , 'longitude' : [2.333333, 2.333333, 0]
    }

    row = pd.DataFrame(row_data)
    df_cities = pd.DataFrame(cities_data)
    row = row.apply (lambda x: get_distance_between_cities(x, df_cities), axis=1)
    assert row.iloc[0]['distance'] == 0


def test_get_info_providers():

    row_data = {'company' : ['1']
                , 'has_wifi' : ['']
                , 'has_plug' : ['']
                , 'has_adjustable_seats' : ['']
                , 'has_bicycle' : ['']
                , 'transport_type' : ['']
    }

    providers_data = {'id' : ['1']
                , 'has_wifi' : [True]
                , 'has_plug' : [True]
                , 'has_adjustable_seats' : [False]
                , 'has_bicycle' : [False]
                , 'transport_type' : ['bus']
    }
    row = pd.DataFrame(row_data)
    df_providers = pd.DataFrame(providers_data)

    row[row['company'] == '1'] = get_info_providers (row, df_providers)
    assert (row.iloc[0]['has_wifi'] == True) & \
            (row.iloc[0]['has_plug'] == True) & \
            (row.iloc[0]['has_adjustable_seats'] == False) & \
            (row.iloc[0]['has_bicycle'] == False) & \
            (row.iloc[0]['transport_type'] == 'bus')
    

def test_count_number_middle_stations():
    row_data = {'company' : ['1']
                , 'has_wifi' : ['']
                , 'has_plug' : ['']
                , 'has_adjustable_seats' : ['']
                , 'has_bicycle' : ['']
                , 'transport_type' : ['']
                , 'arrival_ts' : [datetime.datetime(2022, 12, 28, 13, 30, 0, 342380)]
                , 'o_city' : ['542']
                , 'd_city' : ['611']
                , 'distance' : [1000]
                , 'middle_stations' : ['{111,234,11,111}']
                , 'number_middle_staions' : [0]
    }

    row = pd.DataFrame(row_data)
    row = row.apply (lambda x: count_number_middle_stations(x), axis=1)
    assert row.iloc[0]['number_middle_stations'] == 3

