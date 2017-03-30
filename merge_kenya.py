import os.path
import pandas as pd

from resources import constants

# TODO: wh other funding vs needs data can be merged acros a common dimension?

def child_protection_budget_per_child():
    """
    Given the 2017 Kenya budget for child protection (as part of Security from Violence and Exploitation) from UNHCR
    and the demographic data for refugees and asylum-seekers from the UNHCR proGres registration system,
    compute the budget per child for child protection (with children defined as age < 18).
    """
    # TODO: double checkthese csv files to make sure the numbers are ccorrect and comparable
    base_dir = os.path.join(constants.LATEST_RAW_DATA_PATH, constants.UNHCR_DIR)

    # Get budget for child protection
    budget = pd.read_csv(os.path.join(base_dir, 'budget_kenya_2017.csv'), encoding='utf-8', header=1)
    budget.set_index('Subsector', inplace=True)
    budget_child_protection = budget.get_value('Child protection', 'Total')

    # Get percentage of refugee population that are children (defined as age < 18)
    perc_demographics = pd.read_csv(os.path.join(base_dir, 'refugee_demographics_kenya_Feb2017.csv'), encoding='utf-8', header=1)
    perc_age = perc_demographics.groupby('Age').agg({'Percentage of Refugees and Asylum Seekers': 'sum'}).to_dict()['Percentage of Refugees and Asylum Seekers']
    perc_children = perc_age['0-4'] + perc_age['5-11'] + perc_age['12-17']

    # Calculate the amount in USD budgeted per child for child protection
    pop = pd.read_csv(os.path.join(base_dir, 'refugee_populations_kenya_Feb2017.csv'), encoding='utf-8', header=1)
    pop_total = pop['Refugees'].sum() + pop['Asylum Seekers'].sum()
    pop_children = pop_total * perc_children
    print 'pop_children: %s' % pop_children
    return budget_child_protection /pop_children


def main():
    budget_per_child = child_protection_budget_per_child()
    print 'budget per child: %s' % budget_per_child
    # Roughly $21.84 / child for child protection for refugees and asylum-seekers in Kenya in 2017


if __name__ == '__main__':
    main()
