import click
import calendar
import pandas as pd
import workalendar

from collections import defaultdict
from workalendar import europe, america, asia, oceania, africa, usa

default_weekends = [5, 6]

verbose = False

weekends = {
    'Albania': [5, 6],
    'Algeria': [4, 5],
    'Angola': [5, 6],
    'Argentina': [5, 6],
    'Armenia': [5, 6],
    'Azerbaijan': [5, 6],
    'Austria': [5, 6],
    'Australia': [5, 6],
    'Bahrain': [4, 5],
    'Benin': [5, 6],
    'Belarus': [5, 6],
    'Belgium': [5, 6],
    'Brazil': [5, 6],
    'Burundi': [5, 6],
    'Bulgaria': [5, 6],
    'Canada': [5, 6],
    'Cambodia': [5, 6],
    'Cameroon': [5, 6],
    'Chile': [5, 6],
    'China': [5, 6],
    'Croatia': [5, 6],
    'CostaRica': [5, 6],
    'CzechRepublic': [5, 6],
    'Denmark': [5, 6],
    'Djibouti': [4],
    'DominicanRepublic': [5, 6],
    'Egypt': [4, 5],
    'Ethiopia': [5, 6],
    'Estonia': [5, 6],
    'EquatorialGuinea': [6],
    'Finland': [5, 6],
    'France': [5, 6],
    'Gabon': [5, 6],
    'Gambia': [5, 6],
    'Germany': [5, 6],
    'Ghana': [5, 6],
    'Greece': [5, 6],
    'Hungary': [5, 6],
    'HongKong': [6],
    'India': [6],
    'Indonesia': [5, 6],
    'Iran': [3, 4],
    'Iraq': [4, 5],
    'Ireland': [5, 6],
    'Israel': [4, 5],
    'Italy': [5, 6],
    "Côted'Ivoire": [5, 6],
    'Japan': [5, 6],
    'Jordan': [4, 5],
    'Kazakhstan': [5, 6],
    'Kuwait': [4, 5],
    'Kenya': [5, 6],
    "LaoPeople'sDemocraticRepublic": [5, 6],
    'Latvia': [5, 6],
    'Lebanon': [5, 6],
    'Lesotho': [5, 6],
    'Libya': [4, 5],
    'Lithuania': [5, 6],
    'Luxembourg': [5, 6],
    'Madagascar': [5, 6],
    'Maldives': [4, 5],
    'Malawi': [5, 6],
    'Mali': [5, 6],
    'Malta': [5, 6],
    'Mauritania': [5, 6],
    'Malaysia': [4, 5],
    'Mexico': [5,6],
    'Mongolia': [5, 6],
    'Morocco': [5, 6],
    'Mozambique': [5, 6],
    'Myanmar': [5, 6],
    'Nepal': [5],
    'Netherlands': [5, 6],
    'NewZealand': [5, 6],
    'Nigeria': [5, 6],
    'Norway': [5, 6],
    'Oman': [4, 5],
    'Pakistan': [5, 6],
    'Philippines': [5, 6],
    'Poland': [5, 6],
    'Portugal': [5, 6],
    'Qatar': [4, 5],
    'Romania': [5, 6],
    'Russia': [5, 6],
    'Rwanda': [5, 6],
    'SaudiArabia': [4, 5],
    'Senegal': [5, 6],
    'Serbia': [5, 6],
    'Singapore': [5, 6],
    'Slovakia(SlovakRepublic)': [5, 6],
    'Spain': [5, 6],
    'SriLanka': [5, 6],
    'SouthAfrica': [5, 6],
    'SouthKorea': [5, 6],
    'Somalia': [4],
    'Sudan': [4, 5],
    'Suriname': [5, 6],
    'Swaziland': [5, 6],
    'Sweden': [5, 6],
    'Switzerland': [5, 6],
    'Syria': [4, 5],
    'Seychelles': [5, 6],
    'Taiwan': [5, 6],
    'Tanzania': [5, 6],
    'Togo': [5, 6],
    'Thailand': [5, 6],
    'TrinidadandTobago': [5, 6],
    'Tunisia': [5, 6],
    'Turkey': [5, 6],
    'Ukraine': [5, 6],
    'UnitedKingdom': [5, 6],
    'UnitedStates': [5, 6],
    'Uganda': [6],
    'Vietnam': [5, 6],
    'Yemen': [4, 5],
    'Congo,DemocraticRepublicof': [5, 6],
    'Zambia': [5, 6],
    'Zimbabwe': [5, 6]
}

instances = {
    'Algeria': africa.Algeria(),
    'Angola': africa.Angola(),
    'Benin': africa.Benin(),
    'IvoryCoast': africa.IvoryCoast(),
    'Kenya': africa.Kenya(),
    'Madagascar': africa.Madagascar(),
    'SaoTomeAndPrincipe': africa.SaoTomeAndPrincipe(),
    'SouthAfrica': africa.SouthAfrica(),
    'Argentina': america.Argentina(),
    'Brazil': america.Brazil(),
    'Canada': america.Canada(),
    'Chile': america.Chile(),
    'Colombia': america.Colombia(),
    'Mexico': america.Mexico(),
    'Panama': america.Panama(),
    'Paraguay': america.Paraguay(),
    'China': asia.China(),
    'HongKong': asia.HongKong(),
    'Israel': asia.Israel(),
    'Japan': asia.Japan(),
    'Malaysia': asia.Malaysia(),
    'Qatar': asia.Qatar(),
    'Singapore': asia.Singapore(),
    'SouthKorea': asia.SouthKorea(),
    'Taiwan': asia.Taiwan(),
    'Austria': europe.Austria(),
    'Belgium': europe.Belgium(),
    'Belarus': europe.Belarus(),
    'Bulgaria': europe.Bulgaria(),
    'Croatia': europe.Croatia(),
    'Cyprus': europe.Cyprus(),
    'CzechRepublic': europe.CzechRepublic(),
    'Denmark': europe.Denmark(),
    'Estonia': europe.Estonia(),
    'Finland': europe.Finland(),
    'France': europe.France(),
    'Germany': europe.Germany(),
    'Greece': europe.Greece(),
    'Hungary': europe.Hungary(),
    'Iceland': europe.Iceland(),
    'Ireland': europe.Ireland(),
    'Italy': europe.Italy(),
    'Latvia': europe.Latvia(),
    'Lithuania': europe.Lithuania(),
    'Luxembourg': europe.Luxembourg(),
    'Malta': europe.Malta(),
    'Netherlands': europe.Netherlands(),
    'Norway': europe.Norway(),
    'Poland': europe.Poland(),
    'Portugal': europe.Portugal(),
    'Romania': europe.Romania(),
    'Russia': europe.Russia(),
    'Scotland': europe.Scotland(),
    'Serbia': europe.Serbia(),
    'Slovakia': europe.Slovakia(),
    'Slovenia': europe.Slovenia(),
    'Spain': europe.Spain(),
    'Sweden': europe.Sweden(),
    'Switzerland': europe.Switzerland(),
    'Turkey': europe.Turkey(),
    'Ukraine': europe.Ukraine(),
    'UnitedKingdom': europe.UnitedKingdom(),
    'Australia': oceania.Australia(),
    'NewZealand': oceania.NewZealand(),
    'UnitedStates': usa.UnitedStates(),  # New selected countries after > 3.2.1
    'Mozambique': africa.Mozambique(),
}


african_countries = [country for country in dir(africa) if country[0].isupper() and country in instances.keys()]
america_countries = [country for country in dir(america) if country[0].isupper() and country in instances.keys()]
asian_countries = [country for country in dir(asia) if country[0].isupper() and country in instances.keys()]
european_countries = [country for country in dir(europe) if country[0].isupper() and country in instances.keys()]
oceania_countries = [country for country in dir(oceania) if country[0].isupper() and country in instances.keys()]
usa_countries = [country for country in dir(usa) if country[0].isupper() and country in instances.keys()]


country_mapping = {
    'africa': african_countries,
    'america': america_countries,
    'asia': asian_countries,
    'europe': european_countries,
    'oceania': oceania_countries,
    'usa': usa_countries,
}


def gather_holidays(country_name, year):
    cal = instances[country_name.replace(' ', '')]
    holidays = defaultdict(list)
    for month, day in [(item[0].month, item[0].day) for item in cal.holidays(year)]:
        holidays[month].append(day)
    return holidays


@click.command()
@click.argument('filename')
@click.option('--years', '-y', multiple=True, help='Required years (if void will generate 2008 to 2030).')
@click.option('--zones', '-z', multiple=True, help='Zone name [europe|africa|asia|america|oceania|usa] (default: europe)')
def generate_workdays(filename, years, zones):
    working_days_items = [('country', 'year', 'month', 'workdays_nb')]
    if len(years) == 0:
        years = range(2008, 2030 + 1)
    if len(zones) == 0:
        zones = ['europe', ]
    countries = []
    for zone in zones:
        countries += country_mapping[zone]
    for selected_country in countries:
        try:
            country_weekends = weekends.get(selected_country, default_weekends)
            print("Getting data for {}".format(selected_country))
            for year in years:
                try:
                    country_holidays = gather_holidays(selected_country, year)
                    for month in range(1, 13):
                        working_days = 0
                        for day in range(1, calendar.monthrange(year, month)[-1] + 1):
                            day_of_week = calendar.weekday(year, month, int(day))
                            if day_of_week not in country_weekends:
                                if day not in country_holidays[month]:
                                    working_days += 1
                        working_days_items.append([selected_country, year, month, working_days])
                except workalendar.exceptions.CalendarError:
                    print("  >>> Missing data for {} / {}".format(selected_country, year))

        except KeyError:
            if verbose is True:
                print("  >>> Country {} is not available.".format(selected_country))

        workdays_df = pd.DataFrame(working_days_items[1:], columns=working_days_items[0])
        workdays_df.to_excel(filename, index=False)


if __name__ == '__main__':
    generate_workdays()
