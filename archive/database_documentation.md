# Database Documentation

The books database for datascience is a PostgreSQL instance hosted on Amazon Web Services RDS.

## Tables schemata

### Table: "authors": 733,0339 rows
Primary key: AuthorID

| Label    	| Type       	|
|----------	|------------	|
| Name     	| text       	|
| Works    	| text array 	|
| key      	| text       	|
| AuthorID 	| serial     	|

### Table: "editions": 26,574,661 rows
Primary key: EditionID

| Label            	| Type       	|
|------------------	|------------	|
| EditionTitle     	| text       	|
| Authors          	| text array 	|
| Genre            	| text array 	|
| Subjects         	| text array 	|
| PublishedYear    	| text       	|
| Publisher        	| text       	|
| Pages            	| integer    	|
| Ratings          	| integer    	|
| Popularity       	| integer    	|
| Reviews          	| text array 	|
| OriginalLanguage 	| text array 	|
| Nationality      	| text       	|
| Translators      	| text array 	|
| WorkTitles        | text array  |
| Works             | text array  |
| Languages         | text array  |
| ISBN13            | text        |
| EditionID         | serial      |

### Table: "works": 18,572,829 rows
Primary key: WorkID

| Label            	| Type       	|
|------------------	|------------	|
| WorkTitle        	| text       	|
| Authors          	| text array 	|
| Subjects         	| text array 	|
| Description      	| text       	|
| FirstPublishDate 	| text       	|
| Editions         	| text array 	|
| OtherTitles      	| text array 	|
| TranslatedTitles 	| text array 	|
| WorkID           	| serial     	|


## Important information

This database is from [the OpenLibrary Data Dump.](https://openlibrary.org/developers/dumps)

This database data is largely unusable for the following reason: the works and editions contain entries that are not informative / are garbage data. This is caused by bots creating duplicate 'works' and 'editions' entries in the original OpenLibrary data that have mostly null values except for small changes, such as a different publisher or description. However, there is a solution to this issue. The editions data entries contain the text array labeled 'Works' which has a link/key to the work that the edition is supposed to be associated with.
