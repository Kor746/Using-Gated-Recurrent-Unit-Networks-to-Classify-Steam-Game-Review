from sqlalchemy import create_engine
from langdetect import detect
import pandas as pd


def main():
	engine = create_engine('mysql://root:@localhost:3306/steam')
 #  FROM latest_review 
	# WHERE (content IS NOT NULL 
	# OR content != ''
	# OR content != ' ')"""

	# df = pd.read_sql(steam_data_query, engine)
	df = pd.read_csv('best/pre_processed_steam_reviews_final3.csv')
	for k, v in df.iterrows():
		url = v[1]
		lang  = v[6]

		steam_data_query = "UPDATE latest_review SET lang = '{}' WHERE url = '{}'".format(lang, url)
		# print(steam_data_query)
		with engine.begin() as conn:
			conn.execute(steam_data_query)

if __name__ == '__main__':
	main()