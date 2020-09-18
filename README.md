# morning.thechels.uk

Good Morning.

Morning, is a home page built daily at 5:00 UTC using github-actions, utilising some python to get the latest news, weather, sports fixtures, stocks, and other useful information.

## Prerequisites

In order for this solution to work you need to enter some secrets

![secrets](/secrets.png)

1. An open weather API key - you can register for a free account on their website.
2. Your city code and country code e.g London and UK - to work with the API
3. Update websites.json with your list of website rss feeds you care about.
4. Update stocks.json with the ticker ids for the stocks.
5. Update tournaments.json with the list of competition slugs used by the BBC in order to get the relevant fixtures (its only football at this stage, as that is I all I care about).

## Contributing

We welcome pull requests if you want to add more information to the homepage, then we might need to think about having some config to feature switch off certain elements depending on user needs.
