This program is a python web app that implements Flask to create a map of a businesses clients. The program requires an excel spreadsheet or csv that contains an address, name of the client, and the salesman that corresponds with the client. The sheet will be read and processed through a geocoder, which takes in the address and returns a set of coordinates corresponding with the address. Each valid pair of coordinates will reciveve a pin on the map that is color coded to its corresponding salesman. Each pin is interactive and will display the name of the client, and the salesman who owns the client when the pin is clicked on. 

The geocoder I used for this program was the googleV3 API. I experimented with nominatim and bing, but googleV3 was easily the most efficient.

I completed this project for some volunteer work and am currently working to get the full 800+ client list uploaded to a live server for the company and for public access.

The Project requires a personal API key from the google cloud servers
