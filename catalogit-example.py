import catalogit
url = 'https://hub.catalogit.app/4837/folder/1d330100-93ce-11eb-9bd8-bb7a6aa1a9bb'
metadataframe = catalogit.get_metadata(url)
metadataframe.to_csv('MOSTH-Beulah-Metadata.csv')
